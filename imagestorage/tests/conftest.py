import pytest
from unittest import mock
from minio import Minio
import boto3
from moto import mock_s3
from main import ImageStorageSystem


MINIO_URL = '0.0.0.0:9000'
BUCKET = 'testbucket'
MINIO_ACCESS_KEY = 'minioadmin'
MINIO_SECRET_KEY = 'minioadmin'

class Helpers:
    @staticmethod
    def image_storage(cloud):
        client = ImageStorageSystem(cloud_service_provider=cloud)
        data = mock.MagicMock()
        return client, data
        
@pytest.fixture
def helpers():
    return Helpers



@pytest.fixture
def s3_client():
    with mock_s3():
        conn = boto3.client("s3", region_name="us-east-1")
        conn.create_bucket(Bucket='test_bucket')
        yield conn

@pytest.fixture
def bucket():
    yield 'test_bucket'

@pytest.fixture
def bucket_minio():
    bucket = mock.MagicMock()
    return bucket


def pytest_addoption(parser):
    parser.addoption(
        "--service", action="store", default="aws"
    )

@pytest.fixture
@mock.patch('minios.Minio')
def minioClient(mock_minio):
    return mock_minio
