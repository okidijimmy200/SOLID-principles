from unittest import mock
import pytest
import json,tempfile
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from db import PhoneBook, DatabaseSystem
from main import PhoneBookSystem

def test_create_contact(helpers):
    # table driven test case
    test_cases = [
        {
            "name": "pass",
            "input": "",
            "output": (True, 'Data created successfully in db')
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, 'Failed to create object in db')
        }
    ]
    
    for test_case in test_cases:
        db = mock.MagicMock()
        client, data = helpers.phone_book(db=db)
        client.db.create.return_value = test_case["output"]
        result = client.createContact(data)
        assert result == test_case["output"]


def test_read_contact(helpers):
    db = mock.MagicMock()
    test_cases = [
        {
            "name": "pass",
            "input": "",
            "output": (True, 'Data from MYSQL database', "{'name': 'jones' }")
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>", None)
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.read.return_value = test_case["output"]
        results = client.readContact(test_case["input"])
        assert results == test_case["output"]

def test_update_contect(helpers):
    db = mock.MagicMock()
    test_cases = [
        {
            "name": "pass",
            "input": "",
            "output": (True, 'Data updated from MYSQL database', "{'name': 'jimmyjones' }")
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>", None)
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.update.return_value = test_case['output']
        n, results, k = client.updateContact(data)
        assert results == test_case["output"][1]

def test_delete_contacts(helpers):
    db = mock.MagicMock()
    test_cases = [
        {
            "name": "pass",
            "input": "",
            "output": (True, 'Data with id has been deleted from database')
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>")
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.delete.return_value = test_case["output"]
        n, results= client.deleteContact(data)
        assert results == test_case["output"][-1]

# test database storage of phone
@pytest.fixture(scope='function')
def db_session():
    """Session for SQLAlchemy."""
    Base = declarative_base()  
    meta = Base.metadata
    engine = create_engine('sqlite://')
    Table('phonebook', meta, Column('id',Integer, primary_key=True, index=True), Column('body',String(100), index=True))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def phone_book(db_session):
    """Test user fixture."""
    data = "jimmyjones"

    db = db_session
    new_data = PhoneBook(body=data)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    yield db_session

def test_database(phone_book):
    session = phone_book

    # Do some basic checking
    assert len(session.query(PhoneBook).all()) == 1

def test_read(phone_book):
    session = phone_book
    result = session.query(PhoneBook).all()
    assert str(result) == "[id: 1, body: jimmyjones]"

def test_update(phone_book):
    session = phone_book
    result = session.query(PhoneBook).filter(PhoneBook.id == 1).first()
    result.body = 'okidi'
    session.commit()
    assert str(result) == "id: 1, body: okidi"

def test_delete(phone_book):
    session = phone_book
    result = session.query(PhoneBook).filter(PhoneBook.id == 1).delete()
    assert result == 1
