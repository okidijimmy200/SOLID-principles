import pytest
from unittest import mock
import os
import boto3
from moto import mock_s3, mock_sqs
from main import ImageStorageSystem

class Helpers:
    @staticmethod
    def image_storage(cloud):
        client = ImageStorageSystem(cloud_service_provider=cloud)
        data = mock.MagicMock()
        return client, data
        
@pytest.fixture
def helpers():
    return Helpers

# @pytest.fixture
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"


# @pytest.fixture
# def s3_client(aws_credentials):
#     with mock_s3():
#         conn = boto3.client("s3", region_name="us-east-1")
#         yield conn


# @pytest.fixture
# def sqs_client(aws_credentials):
#     with mock_sqs():
#         conn = boto3.client("sqs", region_name="us-east-1")
#         yield conn

def pytest_addoption(parser):
    parser.addoption(
        "--service", action="store", default="aws"
    )