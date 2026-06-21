import re
from datetime import date
import pytest
from models import UserRegistration
from pydantic import ValidationError

def test_phone_verification_none():
    user = UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                            birth_date='12 April 1988', phone_number=None)
    assert user.phone_number is None

def test_phone_verification_positive():
    user = UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                            birth_date='12 April 1988', phone_number='   +745567695     ')
    assert user.phone_number == '+745567695'

def test_phone_verification_negative():
    with pytest.raises(ValidationError, match=re.escape("Incorrect phone format: Expected international format (e.g., +1234567890).")):
        UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                         birth_date='12 April 1988', phone_number='   +7455676dd95     ')

def test_phone_verification_negative_too_long():
    with pytest.raises(ValidationError, match=re.escape("Incorrect phone format: Expected international format (e.g., +1234567890).")):
        UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                         birth_date='12 April 1988', phone_number='   +7455676959232345     ')

def test_phone_verification_negative_too_short():
    with pytest.raises(ValidationError, match=re.escape("Incorrect phone format: Expected international format (e.g., +1234567890).")):
        UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                         birth_date='12 April 1988', phone_number='   +745567     ')

def test_birth_date():
    user = UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                            birth_date='12 April 1988', phone_number='   +745567695     ')
    assert user.birth_date == date(1988, 4,12)

def test_password_same():
    user = UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='12345',
                            birth_date='12 April 1988', phone_number='   +745567695     ')
    assert user.password == user.password_confirm

def test_password_not_same():
    with pytest.raises(ValidationError, match=re.escape('Passwords are not the same!!')):
        UserRegistration(username='antony', email='yy@yahoo.com', password='12345', password_confirm='abcde',
                                birth_date='12 April 1988', phone_number='   +745567695     ')
