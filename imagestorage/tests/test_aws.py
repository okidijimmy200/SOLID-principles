from unittest import mock
from main import ImageStorageSystem
from aws import AWSStorage

# test aws connection
def test_aws_upload_file():
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": (True, 'Data uploaded successfully in aws')
        },
        {
            "name": "fail",
            "input-1": '',
            "output": (False, "Failed to create data in location '/path/to/file'")
        }
    ]
    for test_case in test_cases:
        cloud = mock.MagicMock()
        myclass = ImageStorageSystem(cloud)
        data = mock.MagicMock()
        myclass.cloud.upload.return_value = test_case["output"]
        reason = myclass.uploadFile(data)
        assert reason == test_case["output"]

def test_aws_delete_file():
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": (True, 'Data successfully removed from aws at /path/to/file')
        },
        {
            "name": "fail",
            "input-1": '',
            "output": (False, "Failed to remove data in from aws at location '/path/to/file'")
        }
    ]
    for test_case in test_cases:
        cloud = mock.MagicMock()
        myclass = ImageStorageSystem(cloud)
        data = mock.Mock()
        myclass.cloud.delete.return_value = test_case["output"]
        reason = myclass.deleteFile(data)
        assert reason == test_case["output"]

def test_aws_download_file():
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": (True, 'Data successfully downloaded from aws at /path/to/file')
        },
        {
            "name": "fail",
            "input-1": '',
            "output": (False, "Failed to download data in location at '/path/to/file'")
        }
    ]
    for test_case in test_cases:
        cloud = mock.MagicMock()
        myclass = ImageStorageSystem(cloud)
        data = mock.MagicMock()
        myclass.cloud.download.return_value = test_case["output"]
        reason = myclass.downloadFile(data)
        assert reason == test_case["output"]

def test_aws_get_file_url():
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": (True, 'URL aws path for data at http://localhost:8000/path/to/file')
        },
        {
            "name": "fail",
            "input-1": '',
            "output": (False, "Failed to locate data in location '/path/to/file'")
        }
    ]
    for test_case in test_cases:
        cloud = mock.MagicMock()
        myclass = ImageStorageSystem(cloud)
        data = mock.MagicMock()
        myclass.cloud.getFileURL.return_value = test_case["output"]
        reason = myclass.getFileURL(data)
        assert reason == test_case["output"]

@mock.patch('aws.AWSStorage.upload')
def test_upload(mock_upload):
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": 'Data uploaded successfully in aws at "/path/to/file"'
        },
        {
            "name": "fail",
            "input-1": '',
            "output": "Failed to create data in location '/path/to/file'"
        }
    ]
    for test_case in test_cases:
        mock_upload.return_value = test_case["output"]
        result = AWSStorage().upload('True', 'to/source', 'to/destination')
        assert result == test_case['output']

@mock.patch('aws.AWSStorage.download')
def test_download(mock_download):
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": 'Data successfully downloaded from aws at "/path/to/file"'
        },
        {
            "name": "fail",
            "input-1": '',
            "output": "Failed to download data in location at '/path/to/file'"
        }
    ]
    for test_case in test_cases:
        mock_download.return_value = test_case["output"]
        result = AWSStorage().download('True', 'to/source', 'to/destination')
        assert result == test_case['output']

@mock.patch('aws.AWSStorage.delete')
def test_delete(mock_delete):
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": 'Data successfully removed from aws at "/path/to/file"'
        },
        {
            "name": "fail",
            "input-1": '',
            "output": "Failed to remove data in location at '/path/to/file'"
        }
    ]
    for test_case in test_cases:
        mock_delete.return_value = test_case["output"]
        result = AWSStorage().delete('True', 'to/destination')
        assert result == test_case['output']

@mock.patch('aws.AWSStorage.getFileURL')
def test_getFileURL(mock_getFileURL):
    test_cases = [
        {
            "name": "pass",
            "input": '',
            "output": 'URL aws path for data at at "http://localhost:8000/path/to/file"'
        },
        {
            "name": "fail",
            "input-1": '',
            "output": "Failed to locate data in location at '/path/to/file'"
        }
    ]
    for test_case in test_cases:
        mock_getFileURL.return_value = test_case["output"]
        result = AWSStorage().getFileURL('True', 'to/destination')
        assert result == test_case['output']