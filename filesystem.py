from abc import ABC, abstractmethod
import json
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil
import io
from minio import Minio
from typing import List, Dict, Tuple
from urllib.parse import unquote, urlparse
import urllib3
import boto3

MINIO_URL = '172.24.32.1:9000'
BUCKET = 'imagestore'
MINIO_ACCESS_KEY = 'minioadmin'
MINIO_SECRET_KEY = 'minioadmin'

minioClient = Minio(
    MINIO_URL, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False )


class CloudSystemInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def uploadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def downloadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def deleteFile(self, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        pass

"""Filesystem database
"""
class MinioStorage(CloudSystemInterface):
    def connect(self):
        return super().connect()

    def disconnect(self):
       return super().disconnect()

    def uploadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print(f"Uploading file to minio")
        try:
            # shutil.copyfile(sourceURI, f"{self.base_path}/{destinationURL}")
            if not minioClient.bucket_exists(BUCKET):
                minioClient.make_bucket(BUCKET)
        except Exception as e:
            print("Bucket Exception : {}".format(e))

        try:
            f = open(f"{sourceURI}", "r")
            data = f.read().encode()
            print(data)
            minioClient.put_object(
            BUCKET, destinationURL, io.BytesIO(data), len(data)
        )
            reason = f"Data uploaded successfully in minio at {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to create data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def deleteFile(self, destinationURL: str) -> Tuple[bool, str]:
        print("Deleting Object from bucket")
        try:
            minioClient.remove_object(
            BUCKET, destinationURL
        )
            reason = f"Data successfully removed from minio at {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to remove data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def downloadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print("Downloading Object from bucket")
        try:
            response = minioClient.get_object(
            BUCKET, sourceURI
        )
            data = response.data
            values = json.loads(data)
            with open(f"{destinationURL}", 'w') as f:
                json.dump(values, f)
            # print(response)
            reason = f"Data successfully downloaded from minio at {sourceURI} to {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to download data in location {sourceURI}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        try:
            result = f"http//localhost:9000/{destinationURL}"
            reason = f"URL minio path for data at {result}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to locate data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

class AWSStorage(CloudSystemInterface):
    def connect(self):
        self.s3 = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        return True

    def disconnect(self):
       return super().disconnect()
    
    def uploadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        try:
            f = open(f"{sourceURI}", "rb")
            self.s3.Bucket('image-store-1995').put_object(Key=f'{destinationURL}', Body=f)

            reason = f"Data uploaded successfully in aws at {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to create data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def downloadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        try:
            with open(f"{sourceURI}", 'wb') as f:
                self.s3_client.download_fileobj('image-store-1995', 'test.json', f)
            # print(response)
            reason = f"Data successfully downloaded from aws at {sourceURI} to {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to download data in location {sourceURI}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def deleteFile(self, destinationURL: str) -> Tuple[bool, str]:
        print("Deleting Object from bucket")
        try:
            self.s3_client.delete_object(Bucket='image-store-1995', Key=f'{destinationURL}')
            reason = f"Data successfully removed from minio at {destinationURL}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to remove data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        try:
            bucket_location = self.s3_client.get_bucket_location(Bucket='image-store-1995')
            object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            'image-store-1995',
            destinationURL)
            reason = f"URL aws path for data at {object_url}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to locate data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

class ImageStorageSystem:
    def __init__(self, cloud_service_provider: CloudSystemInterface) -> None:
        self.cloud = cloud_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.cloud.connect()
        print("System startup completed")

    def uploadFile(self, data: dict) -> Tuple[bool, str]:

        sourceURI = data['uri']
        destinationURL = data['url']

        created, reason = self.cloud.uploadFile(sourceURI, destinationURL)

        if not created:
            print(reason)
            return True, reason
    def deleteFile(self, data: str) -> Tuple[bool, str]:

        destinationURL = data

        deleted, reason = self.cloud.deleteFile(destinationURL)

        if not deleted:
            print(reason)
            return True, reason

    def downloadFile(self, data: dict) -> Tuple[bool, str]:

        sourceURI = data['uri']
        destinationURL = data['url']

        downloaded, reason = self.cloud.downloadFile(sourceURI, destinationURL)

        if not downloaded:
            print(reason)
            return True, reason

    def getFileURL(self, data: str) -> Tuple[bool, str]:
        result, reason = self.cloud.getFileURL(data)

        if not result:
            print(reason)
            return True, reason

# database_service = MinioStorage()
database_service = AWSStorage()

image_storage_system = ImageStorageSystem(database_service)
image_storage_system.setUpSystem()

sourceURI = 'files/test.json'
destinationURL = 'zeus/test.json'

# for downloading
# sourceURI = 'zeus/test.json'
# destinationURL = 'files/test.json'

# image_storage_system.uploadFile({'uri': sourceURI, 'url': destinationURL})
# image_storage_system.deleteFile(destinationURL)
# image_storage_system.downloadFile({'uri': sourceURI, 'url': destinationURL})
image_storage_system.getFileURL(destinationURL)

