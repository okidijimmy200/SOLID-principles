from unittest import mock
import pytest
from typing import Dict, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from db import PhoneBook, DatabaseSystem
from interface import PhoneBookInterface
from main import PhoneBookSystem

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

def test_phone_book(db_session):
    data = "jimmyjones"
    location= 'to/path'
    data_2 = [1,2,3]
    test_cases = [
        {
            "name": "pass",
            "input_1": location,
            "input_2": data,
            "output": (True, f"Data created successfully in location {location}")
        },
        {
            "name": "fail",
            "input_1": location,
            "input_2": data_2,
            "output": (False, f"Failed to create data in location {location}")
        }
    ]    
    for test_case in test_cases:
        result = DatabaseSystem(db_session).create(test_case["input_1"], test_case["input_2"])
        assert result == test_case["output"]



def test_read(db_session):
    location = 'to/path'
    test_cases = [
    {
            "name": "pass",
            "input": location,
            "create": "jimmyjones",
            "output": (True, 'Data read from to/path', "[id: 1, body: jimmyjones]")
        },
        {
            "name": "fail",
            "input": location,
            "create": [1,2,3],
            "output": (False, '',f"Failed to read data from location {location}")
        }
    ]
    # create data in db
    for test_case in test_cases:
        DatabaseSystem(db_session).create('to/path', test_case["create"])
        Boolean,reason, result = DatabaseSystem(db_session).read(test_case["input"])
        assert (Boolean, reason, str(result) ) == test_case["output"]


def test_update(db_session):
    location = 'to/path'
    test_cases = [
    {
            "name": "pass",
            "input_1": location,
            "input_2": 1,
            "create": "jimmyjones",
            "update": "okidi",
            "output": (True, f'Data updated from MYSQL database at 1', "id: 1, body: okidi")
        },
        {
            "name": "fail",
            "input_1": location,
            "input_2": 4,
            "create": "jimmyjones",
             "update": "okidi",
            "output": (False, f"-Failed to update data in location 4", '')
        }
    ]
    for test_case in test_cases:
        DatabaseSystem(db_session).create('to/path', test_case["create"])
        Boolean,reason, result = DatabaseSystem(db_session).update(test_case["input_2"], test_case["update"])
        assert (Boolean, reason, str(result) ) == test_case["output"]

def test_delete(db_session):
    test_cases = [
    {
            "name": "pass",
            "input": 1,
            "create": "jimmyjones",
            "output": (True, f"Data with id 1 has been deleted from database")
        },
        {
            "name": "fail",
            "input": 4,
            "create": "jimmyjones",
            "output": f"Data with the id 4 is not available"
        }
    ]
    for test_case in test_cases:
        DatabaseSystem(db_session).create('to/path', test_case["create"])
        result = DatabaseSystem(db_session).delete(test_case["input"])
        assert result == test_case["output"]
