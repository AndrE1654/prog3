import sqlite3
from datetime import datetime, timedelta

DB = "security_events.db"

def setup_db(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS EventSources (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS EventTypes (
        id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE NOT NULL,
        severity TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS SecurityEvents (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME NOT NULL,
        source_id INTEGER NOT NULL,
        event_type_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        ip_address TEXT,
        username TEXT,
        FOREIGN KEY(source_id) REFERENCES EventSources(id),
        FOREIGN KEY(event_type_id) REFERENCES EventTypes(id)
    );
    """)
    conn.commit()

# універсальна: вставити або отримати id
def insert_or_get_id(conn, table, key_col, key_val, extra_cols=None, extra_vals=None):
    extra_cols = extra_cols or []
    extra_vals = extra_vals or []
    cols = [key_col] + extra_cols
    vals = [key_val] + extra_vals

    cur = conn.cursor()
    cur.execute(
        f"INSERT OR IGNORE INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})",
        vals
    )
    conn.commit()

    cur.execute(f"SELECT id FROM {table} WHERE {key_col} = ?", (key_val,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"Не вдалося отримати id: {table}.{key_col}={key_val}")
    return row[0]

# 4a
def register_source(conn, name, location, src_type):
    return insert_or_get_id(conn, "EventSources", "name", name, ["location", "type"], [location, src_type])

# 4b
def register_event_type(conn, type_name, severity):
    return insert_or_get_id(conn, "EventTypes", "type_name", type_name, ["severity"], [severity])

# 4c
def log_security_event(conn, source_id, event_type_id, message, ip_address=None, username=None, timestamp=None):
    ts = (timestamp or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ts, source_id, event_type_id, message, ip_address, username))
    conn.commit()

def main():
    conn = sqlite3.connect(DB)
    setup_db(conn)

    # EventTypes (як в умові) — коротко через список
    types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical"),
    ]
    type_id = {t: register_event_type(conn, t, s) for t, s in types}

    # EventSources — коротко через список
    sources = [
        ("Firewall_A", "10.0.0.1", "Firewall"),
        ("Web_Server_Logs", "10.0.1.10", "Web Server"),
        ("IDS_Sensor_B", "10.0.2.5", "IDS"),
    ]
    src_id = {n: register_source(conn, n, loc, tp) for n, loc, tp in sources}

    now = datetime.now()

    # 10+ подій (6 brute force + 7 інших = 13)
    for i in range(6):
        log_security_event(conn, src_id["Web_Server_Logs"], type_id["Login Failed"],
                           "Failed login attempt", "203.0.113.9", "admin",
                           now - timedelta(minutes=i * 7))

    events = [
        (now - timedelta(hours=2), src_id["Web_Server_Logs"], type_id["Login Success"], "User logged in successfully", "198.51.100.23", "olena"),
        (now - timedelta(hours=3), src_id["Web_Server_Logs"], type_id["Login Failed"], "Wrong password for user", "198.51.100.23", "olena"),
        (now - timedelta(hours=5), src_id["Firewall_A"], type_id["Port Scan Detected"], "Port scan detected on TCP ports 22, 80, 443", "192.0.2.44", None),
        (now - timedelta(days=2), src_id["IDS_Sensor_B"], type_id["Malware Alert"], "Malware signature matched: Trojan.XYZ", "203.0.113.77", None),
        (now - timedelta(days=6), src_id["Firewall_A"], type_id["Malware Alert"], "Outbound connection to known C2 domain blocked", "203.0.113.77", None),
        (now - timedelta(days=1, hours=1), src_id["IDS_Sensor_B"], type_id["Port Scan Detected"], "Multiple SYN packets detected (possible scan)", "192.0.2.44", None),
        (now - timedelta(hours=20), src_id["Web_Server_Logs"], type_id["Login Failed"], "Failed login attempt (user not found)", "203.0.113.55", "unknown"),
    ]
    for ts, sid, eid, msg, ip, user in events:
        log_security_event(conn, sid, eid, msg, ip, user, ts)

    cur = conn.cursor()

    print("\n1) Login Failed за останні 24 години:")
    cur.execute("""
    SELECT se.timestamp, es.name, se.ip_address, se.username, se.message
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id = se.event_type_id
    JOIN EventSources es ON es.id = se.source_id
    WHERE et.type_name = 'Login Failed'
      AND se.timestamp >= datetime('now', '-24 hours')
    ORDER BY se.timestamp DESC
    """)
    for row in cur.fetchall():
        print(row)

    print("\n2) IP з >5 невдалих входів за 1 годину:")
    cur.execute("""
    SELECT se.ip_address,
           strftime('%Y-%m-%d %H:00:00', se.timestamp) AS hour_bucket,
           COUNT(*) AS attempts
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id = se.event_type_id
    WHERE et.type_name = 'Login Failed'
      AND se.ip_address IS NOT NULL
      AND se.timestamp >= datetime('now', '-24 hours')
    GROUP BY se.ip_address, hour_bucket
    HAVING COUNT(*) > 5
    ORDER BY attempts DESC
    """)
    for row in cur.fetchall():
        print(row)

    print("\n3) Critical події за останній тиждень (група за джерелом):")
    cur.execute("""
    SELECT es.name, COUNT(*) AS critical_count
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id = se.event_type_id
    JOIN EventSources es ON es.id = se.source_id
    WHERE et.severity = 'Critical'
      AND se.timestamp >= datetime('now', '-7 days')
    GROUP BY es.name
    ORDER BY critical_count DESC
    """)
    for row in cur.fetchall():
        print(row)

    keyword = input("\n4) Введи ключове слово для пошуку у message: ").strip()
    print(f"\nРезультати пошуку для '{keyword}':")
    cur.execute("""
    SELECT se.timestamp, es.name, et.type_name, et.severity, se.ip_address, se.username, se.message
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id = se.event_type_id
    JOIN EventSources es ON es.id = se.source_id
    WHERE se.message LIKE ?
    ORDER BY se.timestamp DESC
    """, (f"%{keyword}%",))
    for row in cur.fetchall():
        print(row)

    conn.close()
    print("\nГотово ✅")

if __name__ == "__main__":
    main()

