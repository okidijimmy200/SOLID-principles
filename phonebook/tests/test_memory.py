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
from memory import MemorySystem
import json,tempfile
from interface import PhoneBookInterface


def test_create_contact(helpers):
        # table driven test case
    test_cases = [
        {
            "name": "pass",
            "input": "",
            "output": (True, 'Data created successfully in location test/output.json')
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, 'Failed to create data in location test/output.json')
        }
    ]
    for test_case in test_cases:
        db = mock.MagicMock()
        client, data = helpers.phone_book(db=db)
        client.db.create.return_value = test_case["output"]
        result = client.createContact(data)
        assert result == test_case["output"]


def test_read_contact(helpers):
    test_cases = [
        {
            "name": "pass",
            "input": "{'name': 'jones' }",
            "output": (True, "Data read from test/output.json'", "{'name': 'jones' }")
        },
        {
            "name": "fail",
            "input": "",
            "output": (False, 'Unexpected failed to read', None )
        }
    ]
    for test_case in test_cases:
        db = mock.MagicMock()
        client, data = helpers.phone_book(db=db)
        client.db.read.return_value = test_case["output"]
        result = client.readContact(test_case["input"])
        assert result == test_case["output"]

def test_update_contact(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "id": f"{str(tfile.name)}",
            "input": "jimmyjones",
            "output": (True, "Data updated successfully in location", '{"name": "jimmyjones"}')
        },
        {
            "name": "fail",
            "id": f"test/test.json",
            "input": "jimmyjones",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>", None)
        }
    ]
    for test_case in test_cases:
        db = mock.MagicMock()
        _sut, data = helpers.phone_book(db=MemorySystem())
        k, reason, y = _sut.updateContact({"id": test_case["id"], "name": test_case["input"], "phone": '0788926712.json'})
        n, result, p = test_case["output"]
        assert (n,result) == (k, reason)

def test_delete_contact(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "id": f"{str(tfile.name)}",
            "output": (True, f"JSON {tfile.name} removed")
        },
        {
            "name": "fail",
            "id": f"test/test.json",
            "output": (False, "File doesnot exist")
        }
    ]
    for test_case in test_cases:
        db = mock.MagicMock()
        _sut, data = helpers.phone_book(db=MemorySystem())
        k= _sut.deleteContact({"id": test_case["id"]})
        result = test_case["output"]
        assert result == k

def test_create(helpers):
    tfile = helpers.input_variables()
    data = {"id": 1, "name": 'test', "phone": '0788926712.json'}
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}",
            "output": f"Data created successfully in location {str(tfile.name)}"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "Failed to create data in location test/test.json, reason:FileNotFoundError [Errno 2] No such file or directory: 'test/test.json'"
        }
    ]
    for test_case in test_cases:
            # why do we have 3 args with self included as an arg
        k, result = MemorySystem.create(test_case["input-1"],test_case["input-2"], data)
        assert result == test_case["output"]

def test_read(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}",
            "output": f"Data read from {str(tfile.name)}"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>"
        }
    ]
    for test_case in test_cases:
        # why do we have 3 args with self included as an arg
        k, result, data = MemorySystem.read(test_case["input-1"],test_case["input-2"])
        assert result == test_case["output"]

def test_update(helpers):
    tfile = helpers.input_variables()
    name_2 = 'jimmyjones'
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}",
            "output": (True, "Data updated successfully in location")
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": (False, "Unexpected err=FileNotFoundError(2, 'No such file or directory'), type(err)=<class 'FileNotFoundError'>")
        }
    ]
    for test_case in test_cases:
        
        k, reason, data = MemorySystem.update(test_case["input-1"], test_case["input-2"], {"id": 1, "name": name_2, "phone": '0788926712.json'})
        assert (k, reason) == test_case["output"]

def test_delete(helpers):
    tfile = helpers.input_variables()
    test_cases = [
        {
            "name": "pass",
            "input-1": 'True',
            "input-2": f"{str(tfile.name)}",
            "output": f"JSON {str(tfile.name)} removed"
        },
        {
            "name": "fail",
            "input-1": 'True',
            "input-2": "test/test.json",
            "output": "File doesnot exist"
        }
    ]
    for test_case in test_cases:
        k, reason = MemorySystem.delete(test_case["input-1"],test_case["input-2"])
        assert reason == test_case["output"]


