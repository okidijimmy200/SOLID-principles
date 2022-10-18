import os
import sys
import pytest
from aws import AWSStorage
from minios import MinioStorage
from main import ImageStorageSystem


@pytest.fixture
def db_service(getDatabaseService):
    image_storage_system = ImageStorageSystem(getDatabaseService)
    image_storage_system.setUpSystem()
    return image_storage_system

@pytest.fixture
def db_name(request):
    service = request.config.getoption('--service')
    return service

@pytest.fixture
def getDatabaseService(db_name):
    print(db_name)
    if db_name == 'aws':
        return AWSStorage()
    else:
        return MinioStorage()

def test_uploadFile(db_service):
    data = {"uri": "files/AI.jpg", "url": "/output/AI.jpg"}
    data_2 = {"uri": "home/files/AI.jpg", "url": "/output/AI.jpg"}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data uploaded successfully")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to create data in location")
        }
    ]
    for test_case in test_cases:
        output = db_service.uploadFile(test_case["input"])
        expected = test_case["output"]
        assert output, expected

def test_downloadFile(db_service):
    data = {"uri": "files/AI.jpg", "url": "/output/AI.jpg"}
    data_2 = {"uri": "home/files/AI.jpg", "url": "/output/AI.jpg"}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data downloaded successfully")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to download data from location")
        }
    ]
    for test_case in test_cases:
        output = db_service.downloadFile(test_case["input"])
        expected = test_case["output"]
        assert output, expected

def test_deleteFile(db_service):
    data =  "/output/AI.jpg"
    data_2 =  "home/output/AI.jpg"
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data deleted successfully")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to delete data in location")
        }
    ]
    for test_case in test_cases:
        output = db_service.deleteFile(test_case["input"])
        expected = test_case["output"]
        assert output, expected

def test_getFileURL(db_service):
    data =  "/output/AI.jpg"
    data_2 =  "home/output/AI.jpg"
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "File url is https://imagestore.com/output/AI.jpg")
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "Failed to get file URL")
        }
    ]
    for test_case in test_cases:
        output = db_service.getFileURL(test_case["input"])
        expected = test_case["output"]
        assert output, expected