from aws import AWSStorage

def test_upload(s3_client, bucket):
    test_cases = [
        {
            "name": "pass",
            "input_1": 'files/AI.jpg',
            "input_2": 'files/AI.jpg',
            "output":  (True, 'Data uploaded successfully in aws at files/AI.jpg')
        },
        {
            "name": "fail",
            "input_1": '/home/files/AI.jpg',
            "input_2": 'files/AI.jpg',
            "output": (False, "Failed to create data in location files/AI.jpg, reason:FileNotFoundError [Errno 2] No such file or directory: '/home/files/AI.jpg'")
        }
    ]

    for test_case in test_cases:
        my_client = AWSStorage(s3_client, bucket)
        objects = my_client.upload(test_case['input_1'], test_case['input_2'])

        assert objects == test_case['output']

def test_download(s3_client, bucket):
    test_cases = [
        {
            "name": "pass",
            "input_1": 'AI-2.jpg',
            "input_2": 'AI-2.jpg',
            "create": "AI-2.jpg",
            "output":  (True, 'Data successfully downloaded from aws at AI-2.jpg to AI-2.jpg')
        },
        {
            "name": "fail",
            "input_1": '/home/files/AI-2.jpg',
            "input_2": '/home/files/AI-2.jpg',
            "create": "AI-2.jpg",
            "output": (False, "Failed to download data in location /home/files/AI-2.jpg")
        }
    ]

    for test_case in test_cases:
        # upload file
        AWSStorage(s3_client, bucket).upload(test_case['create'], test_case['create'])
        my_client = AWSStorage(s3_client, bucket)
        objects = my_client.download(test_case['input_1'], test_case['input_2'])

        assert objects == test_case['output']

def test_delete(s3_client, bucket):
    test_cases = [
        {
            "name": "pass",
            "input": 'files/AI.jpg',
            "create": "files/AI.jpg",
            "output":  (True, 'Data successfully removed from aws at files/AI.jpg')
        },
        {
            "name": "fail",
            "input": 'home/files/AI.jpg',
            "create": "files/AI.jpg",
            "output": (False, "Failed to remove data in location home/files/AI.jpg")
        }
    ]

# NB: mock_s3 test for fail works!!!!!!!!
    for test_case in test_cases:
        # upload file
        AWSStorage(s3_client, bucket).upload(test_case['create'], test_case['create'])
        my_client = AWSStorage(s3_client, bucket)
        objects = my_client.delete(test_case['input'])

        assert objects == test_case['output']


def test_getFileURL(s3_client, bucket):
    test_cases = [
        {
            "name": "pass",
            "input": 'files/AI.jpg',
            "create": "files/AI.jpg",
            "output":  (True, 'URL aws path for data at https://s3-None.amazonaws.com/test_bucket/files/AI.jpg')
        },
        {
            "name": "fail",
            "input": 'home/files/AI.jpg',
            "create": "files/AI.jpg",
            "output": (False, "Failed to locate data in location home/files/AI.jpg")
        }
    ]

    for test_case in test_cases:
        # upload file
        AWSStorage(s3_client, bucket).upload(test_case['create'], test_case['create'])
        my_client = AWSStorage(s3_client, bucket)
        objects = my_client.getFileURL(test_case['input'])

        assert objects == test_case['output']