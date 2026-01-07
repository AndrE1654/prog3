import pytest

import pz2
from pz2 import User, Administrator, RegularUser, GuestUser, AccessControl


# -------------------------
# User._hash_password (2 тести)
# -------------------------
def test_hash_password_is_deterministic():
    u1 = User("u1", "pass123")
    h1 = u1._hash_password("pass123")
    h2 = u1._hash_password("pass123")
    assert h1 == h2


def test_hash_password_changes_for_different_passwords():
    u1 = User("u1", "pass123")
    h1 = u1._hash_password("pass123")
    h2 = u1._hash_password("pass124")
    assert h1 != h2


# -------------------------
# User.verify_password (2 тести)
# -------------------------
def test_verify_password_true_for_correct_password():
    u = User("bob", "qwerty")
    assert u.verify_password("qwerty") is True


def test_verify_password_false_for_wrong_password():
    u = User("bob", "qwerty")
    assert u.verify_password("wrong") is False


# -------------------------
# AccessControl.add_user (2 тести)
# -------------------------
def test_add_user_stores_user_by_username():
    ac = AccessControl()
    u = User("alice", "123")
    ac.add_user(u)
    assert "alice" in ac.users
    assert ac.users["alice"] is u


def test_add_user_overwrites_same_username():
    ac = AccessControl()
    u1 = User("same", "111")
    u2 = User("same", "222")
    ac.add_user(u1)
    ac.add_user(u2)
    assert ac.users["same"] is u2


# -------------------------
# AccessControl.authenticate_user (мінімум 2 тести, я зробив більше)
# -------------------------
def test_authenticate_user_returns_none_if_user_not_found():
    ac = AccessControl()
    assert ac.authenticate_user("missing", "any") is None


def test_authenticate_user_returns_none_if_inactive():
    ac = AccessControl()
    u = RegularUser("tom", "secret")
    u.is_active = False
    ac.add_user(u)
    assert ac.authenticate_user("tom", "secret") is None


def test_authenticate_user_returns_user_for_correct_password():
    ac = AccessControl()
    u = Administrator("admin", "adminpass", permissions=["read", "write"])
    ac.add_user(u)
    result = ac.authenticate_user("admin", "adminpass")
    assert result is u


def test_authenticate_user_returns_none_for_wrong_password():
    ac = AccessControl()
    u = RegularUser("user", "rightpass")
    ac.add_user(u)
    assert ac.authenticate_user("user", "wrongpass") is None


def test_authenticate_user_guest_can_login_with_empty_password():
    ac = AccessControl()
    g = GuestUser("guest1")
    ac.add_user(g)
    result = ac.authenticate_user("guest1", "")
    assert result is g


def test_authenticate_user_guest_can_login_with_any_password():
    ac = AccessControl()
    g = GuestUser("guest2")
    ac.add_user(g)
    result = ac.authenticate_user("guest2", "anything")
    assert result is g
