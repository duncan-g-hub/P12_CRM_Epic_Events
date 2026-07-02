import pytest
from datetime import datetime, timedelta

import validators

# Date
def test_validate_date_valid():
    date = "24/12/2026"
    assert validators.validate_date(date) == datetime.strptime(date, "%d/%m/%Y")


def test_validate_date_invalid():
    date = "24/décembre/2026"
    with pytest.raises(ValueError):
        validators.validate_date(date)


def test_validate_future_date_valid():
    date = datetime.today() + timedelta(days=1)
    assert validators.validate_future_date(date) == date


def test_validate_future_date_in_past_invalid():
    date = "24/12/2000"
    with pytest.raises(ValueError):
        validators.validate_future_date(date)


def test_validate_date_end_valid():
    date_start = datetime.today() + timedelta(days=1)
    date_end = datetime.today() + timedelta(days=2)
    assert validators.validate_date_end(date_start, date_end) == date_end


def test_validate_date_end_before_start_invalid():
    date_start = datetime.today() + timedelta(days=2)
    date_end = datetime.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        validators.validate_date_end(date_start, date_end)


# Phone
def test_validate_phone_valid():
    phone = '0123456789'
    assert validators.validate_phone(phone) == phone


def test_validate_phone_invalid():
    phone = '01564'
    with pytest.raises(ValueError):
        validators.validate_phone(phone)


# Email
def test_validate_email_valid():
    email = 'email@email.com'
    assert validators.validate_email(email) == email


def test_validate_email_invalid():
    email = 'email.email.com'
    with pytest.raises(ValueError):
        validators.validate_email(email)


# Password
def test_validate_password_valid():
    password = 'Password01'
    assert validators.validate_password(password) == password


def test_validate_password_too_short():
    password = 'Pass01'
    with pytest.raises(ValueError):
        validators.validate_password(password)


def test_validate_password_no_uppercase():
    password = 'pass01'
    with pytest.raises(ValueError):
        validators.validate_password(password)


# Amount to pay
def test_validate_amount_to_pay_exceeds_total():
    amount = 100
    total = 80
    with pytest.raises(ValueError):
        validators.validate_amount_to_pay(amount, total)


def test_validate_amount_to_pay_valid():
    amount = 80
    total = 100
    assert validators.validate_amount_to_pay(amount, total) == amount


# Float
def test_validate_float_valid():
    number = '0.123'
    assert validators.validate_float(number) == float(number)


def test_validate_float_invalid():
    number = "three"
    with pytest.raises(ValueError):
        validators.validate_float(number)


# Int
def test_validate_integer_valid():
    number = '123'
    assert validators.validate_integer(number) == int(number)


def test_validate_integer_invalid():
    number = '0.123'
    with pytest.raises(ValueError):
        validators.validate_integer(number)
