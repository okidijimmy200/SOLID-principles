import unittest
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
from db import PhoneBookSystem, MemorySystem, DatabaseSystem, ImageStore

# test creating file
def test_createContact():
    _sut = PhoneBookSystem(MemorySystem())
    name = 'test'
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    k = _sut.createContact({"name": name, "phone": str(tfile.name)})
    result = f'Data created successfully in location {tfile.name}'
    assert result == k

# test reading from file
def test_readContact():
    _sut = PhoneBookSystem(MemorySystem())
    phone = '0788926712'
    name = 'test'
    config = {"name": name, "phone": phone}
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(config, tfile)
    tfile.flush()
    result = {"name": name, "phone": phone}
    k = _sut.readContact(tfile.name)
    assert result == k

# test updating file
def test_updateContact():
    _sut = PhoneBookSystem(MemorySystem())
    phone = '0788926712.json'
    name = 'test'
    id = 1
    # write data to a particular location
    config = {"id": id, "name": name, "phone": phone}
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(config, tfile)
    tfile.flush()
    name_2 = 'jimmyjones'
    k = _sut.updateContact({"id": str(tfile.name), "name": name_2, "phone": phone})
    result = 'Data updated successfully in location'
    assert result == k

# test deleting file
def test_deleteContact():
    _sut = PhoneBookSystem(MemorySystem())
    phone = '0788926712.json'
    name = 'test'
    id = 1
    # write data to a particular location
    config = {"id": id, "name": name, "phone": phone}
    tfile = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(config, tfile)
    tfile.flush()
    k = _sut.deleteContact({"id": str(tfile.name)})
    result = f"JSON {tfile.name} removed"
    assert result == k

# test database storage of image
@pytest.fixture(scope='function')
def db_session():
    """Session for SQLAlchemy."""
    Base = declarative_base()  
    meta = Base.metadata
    engine = create_engine('sqlite://')
    Table('image', meta, Column('id',Integer, primary_key=True, index=True), Column('body',String(100), index=True))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def image_store(db_session):
    """Test user fixture."""
    data = "jimmyjones"

    db = db_session
    new_data = ImageStore(body=data)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    yield db_session

def test_database(image_store):
    session = image_store

    # Do some basic checking
    assert len(session.query(ImageStore).all()) == 1

# test creating contact
def test_createContact(image_store):
    k = PhoneBookSystem(DatabaseSystem()).createContact({"name": 'jimmyjones', "phone": '0788926712'}, test_db=image_store)
    result = 'Data stored succesfully at 0788926712'
    assert result == k

# test reading contact
def test_readContact(image_store):
    k = PhoneBookSystem(DatabaseSystem()).readContact('jimmyjones', test_db=image_store)
    result = 'id: 1, body: jimmyjones'
    assert result == f"{k[0]}"

# test update contact
def test_updateContact(image_store):
    k = PhoneBookSystem(DatabaseSystem()).updateContact({"id": 1, "phone": 'okidi'}, test_db=image_store)
    result = 'id: 1, body: okidi'
    assert result == f"{k}"

# test delete contact
def test_deleteContact(image_store):
    k = PhoneBookSystem(DatabaseSystem()).deleteContact({"id": 1}, test_db=image_store)
    result = 'Data with id 1 has been deleted from database'
    assert result == k




