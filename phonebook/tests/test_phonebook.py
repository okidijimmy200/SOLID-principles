from unittest import mock
import pytest

@pytest.fixture
def db_name(request):
    db = request.config.getoption('--db')
    return db

@pytest.fixture
@mock.patch('db.DatabaseSystem')
@mock.patch('memory.MemorySystem')
def db(db_mock, memory_mock,db_name):
    print(db_name)
    if db_name == 'db':
        return db_mock
    elif db_name == 'inmemory':
        return memory_mock


def test_createContact(db, helpers):
    data = {"name": "Jimmy", "phone": "0788926713.json"}
    data_2 = {"name": [1,2,3,4], "phone": "/home/0788926713.json"}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data created successfully in location 0788926713.json")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to create data in location /home/0788926713.json")
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.create.return_value = test_case["output"]
        output = client.createContact(test_case["input"])
        expected = test_case["output"]
        assert output == expected


def test_readContact(db, helpers):
    data = "0788926713.json"
    data_2 = "/test/0788926713.json"
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data read from 0788926713.json", "Jimmy")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to read data from location /home/0788926734.json", None)
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.read.return_value = test_case["output"]
        output = client.readContact(test_case["input"])
        expected = test_case["output"]
        assert output == expected

def test_updateContact(db, helpers):
    data = {"id": 1,"name": "Jimmy", "phone": "0788926713"}
    data_2 = {"id": 1,"name": "Jimmy", "phone": "0788926713.json"}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data updated in location", "0000000000")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to update data in location", "")
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.update.return_value = test_case["output"]
        output = client.updateContact(test_case["input"])
        expected = test_case["output"]
        assert output == expected

def test_deleteContact(db, helpers):
    data = {"id": 1,"name": "Jimmy", "phone": "0788926713"}
    data_2 = {"id": 1,"name": "Jimmy", "phone": "0788926713.json"}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data updated in location")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to delete data in location")
        }
    ]
    for test_case in test_cases:
        client, data = helpers.phone_book(db=db)
        client.db.delete.return_value = test_case["output"]
        output = client.deleteContact(test_case["input"])
        expected = test_case["output"]
        assert output == expected


