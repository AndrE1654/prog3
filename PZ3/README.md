# Завдання Розширена робота з БД - Система логування подій (опціонально) 

**Умова:**  
1. За допомогою Python створіть БД sqlite3 та наступні таблиці:<br>
 a. EventSources (ДжерелаПодій). Структуратаблиці:<br>
  i.   id (PRIMARY KEY, INTEGER)<br>
  ii.  name (TEXT, UNIQUE) - Назва джерела (наприклад, "Firewall_A", "Web_Server_Logs", "IDS_Sensor_B")<br>
  iii. location (TEXT) - Місце розташування/IP джерела<br>
  iv.  type (TEXT) - Тип джерела (наприклад, "Firewall", "Web Server", "IDS")<br>
 b. EventTypes (ТипиПодій):<br>
  i.   id (PRIMARY KEY, INTEGER)<br>
  ii.  type_name (TEXT, UNIQUE) - Назва типу події (наприклад, "Login Success", "Login Failed", "Port Scan Detected", "Malware Alert")<br>
  iii. severity (TEXT) - Серйозність типу події (наприклад, "Informational", "Warning", "Critical")<br>
 c. SecurityEvents (ПодіїБезпеки):<br>
  <br>i.   id (PRIMARY KEY, INTEGER)<br>
  <br>ii.  timestamp (DATETIME) - Час події<br>
  <br>iii. source_id (INTEGER, FOREIGN KEY до EventSources.id)<br>
 <br> iv.  event_type_id (INTEGER, FOREIGN KEY до EventTypes.id)<br>
 <br> v.   message (TEXT) - Повний текст логу/повідомлення<br>
 <br> vi.  ip_address (TEXT, NULLABLE) - IP-адреса, пов'язана з подією (якщо є)<br>
 <br>vvi. username (TEXT, NULLABLE) - Ім'я користувача, пов'язане з подією (якщо є)<br>
2. Внесіть наступні дані до таблиці EventTypes:<br>

Event type_name
Event severity
Login Success
Informational
Login Failed
Warning
Port Scan Detected
Warning
Malware Alert
Critical

 
3. Внесіть декілька тестових значень у таблицю EventSources та  10+ тестових значеньдо таблиці SecurityEvents <br>
4. Розробіть програму на python, яка містить у собі наступні функції:<br>
a. Функція для реєстрації нового джерела подій.<br>
b. Функція для реєстрації нового типу подій.<br>
c. Функція для запису нової події безпеки (з автоматичним заповненням timestamp).<br>
d. Функції запиту даних:<br>
   i.   Отримати всі події "Login Failed" за останні 24 години.<br>
   ii.  Виявити IP-адреси, з яких було більше 5 невдалих спроб входу за 1 годину (потенційна атака підбору пароля).<br>
   iii. Отримати всі події з рівнем серйозності "Critical" за останній тиждень, згруповані за джерелом.<br>
   iv.  Знайти всі події, що містять певне ключове слово у повідомленні (message).<br>


## Рішення
- [task1.py](task1.py)
