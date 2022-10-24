import mock
import pytest

@pytest.fixture
def db_name(request):
    service = request.config.getoption('--service')
    return service

@pytest.fixture
@mock.patch('aws.AWSStorage')
@mock.patch('minios.MinioStorage')
def cloud(mock_aws, mock_minios, db_name):
    print(db_name)
    if db_name == 'aws':
        return mock_aws
    elif db_name == 'minios':
        return mock_minios

def test_uploadFile(cloud, helpers):
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
        client, data = helpers.image_storage(cloud=cloud)
        client.cloud.upload.return_value = test_case["output"]
        output = client.uploadFile(test_case["input"])
        expected = test_case["output"]
        assert output == expected

def test_downloadFile(cloud, helpers):
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
        client, data = helpers.image_storage(cloud=cloud)
        client.cloud.download.return_value = test_case["output"]
        output = client.downloadFile(test_case["input"])
        expected = test_case["output"]
        assert output == expected

def test_deleteFile(cloud, helpers):
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
        client, data = helpers.image_storage(cloud=cloud)
        client.cloud.delete.return_value = test_case["output"]
        output = client.deleteFile(test_case["input"])
        expected = test_case["output"]
        assert output == expected

def test_getFileURL(cloud, helpers):
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
        client, data = helpers.image_storage(cloud=cloud)
        client.cloud.getFileURL.return_value = test_case["output"]
        output = client.getFileURL(test_case["input"])
        expected = test_case["output"]
        assert output == expected