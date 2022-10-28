from unittest import mock
from unittest.mock import mock_open, patch
from minios import MinioStorage

def test_upload(minioClient, bucket_minio):
    test_cases = [
        {
            "name": "pass",
            "input": 'files/AI.jpg',
            "output": (True, 'Data uploaded successfully in minio at files/AI.jpg')
        },
        {
            "name": "fail",
            "input": [123],
            "output": (False, "Failed to create data in location [123]")
        }
    ]
    for test_case in test_cases:
        result = MinioStorage(minioClient, bucket_minio).upload(test_case['input'], test_case['input'])
        assert result == test_case['output']

def test_delete(minioClient, bucket_minio):
    test_cases = [
        {
            "name": "pass",
            "input": 'files/AI.jpg',
            "result": True,
            "output": (True, 'Data successfully removed from minio at files/AI.jpg')
        },
        {
            "name": "fail",
            "input": 'home/files.jpg',
            "result": False,
            "output": (False, "Failed to remove data in location home/files.jpg")
        }
    ]
    for test_case in test_cases:
        MinioStorage(minioClient, bucket_minio).minioClient.remove_object.return_value = test_case["result"]
        result = MinioStorage(minioClient, bucket_minio).delete(test_case['input'])
        assert result == test_case['output']

# def test_download(minioClient, bucket_minio):
#     test_cases = [
#         {
#             "name": "pass",
#             "input": 'files/AI.jpg',
#             "result": 'True',
#             "output": (True, 'Data successfully removed from minio at files/AI.jpg')
#         },
#         {
#             "name": "fail",
#             "input": 'home/files.jpg',
#             "result": '',
#             "output": (False, "Failed to remove data in location home/files.jpg")
#         }
#     ]
#     for test_case in test_cases:
#         with patch('__main__.open', mock_open, create=True):
#             with open('foo', 'w') as h:
#                 h.write('some stuff')
#         result = MinioStorage(minioClient, bucket_minio).download(test_case['input'], test_case['input'])
#         assert result == test_case['output']


def test_getFileURL(minioClient, bucket_minio):
    test_cases = [
        {
            "name": "pass",
            "input": 'files/AI.jpg',
            "result": True,
            "output": (True, 'URL minio path for data at http//localhost:9000/files/AI.jpg')
        },
        {
            "name": "fail",
            "input": 'home/files.jpg',
            "result": False,
            "output": (False, "Failed to locate data in location home/files.jpg")
        }
    ]
    for test_case in test_cases:
        MinioStorage(minioClient, bucket_minio).minioClient.list_objects.return_value = test_case['result']
        result = MinioStorage(minioClient, bucket_minio).getFileURL(test_case['input'])
        assert result == test_case['output']