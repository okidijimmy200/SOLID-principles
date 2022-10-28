import json
import io
from minio import Minio
from typing import Tuple
from cloud_interface import CloudSystemInterface

MINIO_URL = '0.0.0.0:9000'
BUCKET = 'imagestore'
MINIO_ACCESS_KEY = 'minioadmin'
MINIO_SECRET_KEY = 'minioadmin'

minioClient = Minio(
    MINIO_URL, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False )

"""Minio Storage"""
class MinioStorage(CloudSystemInterface):

    def __init__(self, minioClient, bucket) -> None:
        super().__init__()
        self.minioClient = minioClient
        self.bucket = bucket

    def connect(self):
        return super().connect()

    def disconnect(self):
       return super().disconnect()

    def upload(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print(f"Uploading file to minio")
        try:
            if not self.minioClient.bucket_exists(self.bucket):
                self.minioClient.make_bucket(self.bucket)

        except Exception as e:
            print("Bucket Exception : {}".format(e))

        try:
                image = sourceURI.split()[-1]
                self.minioClient.fput_object(
                self.bucket, image ,sourceURI
            )
                reason = f"Data uploaded successfully in minio at {destinationURL}"
                print(reason)
                return True, reason


        except  Exception as e:
            reason = (
                f"Failed to create data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to create data in location {destinationURL}'

            print(reason)
            return False, result

    def delete(self, destinationURL: str) -> Tuple[bool, str]:
        try:
            objects = self.minioClient.list_objects(self.bucket)
            if objects:
                results = self.minioClient.remove_object(
                self.bucket, destinationURL )
                print(results)
                if results:
                    reason = f"Data successfully removed from minio at {destinationURL}"
                    print(reason)
                    return True, reason
                else:
                    reason = f"Failed to remove data in location {destinationURL}"
                    print(reason)
                    return False, reason


        except  Exception as e:
            reason = (
                f"Failed to remove data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to remove data in location {destinationURL}'
            print(reason)
            return False, result

    def download(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print("Downloading Object from bucket")
        try:
            response = self.minioClient.get_object(
            self.bucket, sourceURI
        )
            data = response.data
            with open(f"{destinationURL}", 'wb') as handler:
                try:
                    handler.write(data)
                    reason = f"Data successfully downloaded from minio at {sourceURI} to {destinationURL}"
                    print(reason)
                    return True, reason
                except (IOError, OSError):
                    print("Error writing to file")

        except  Exception as e:
            reason = (
                f"Failed to download data in location {sourceURI}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        try:
            objects = self.minioClient.list_objects(self.bucket)
            if objects:
                result = f"http//localhost:9000/{destinationURL}"
                reason = f"URL minio path for data at {result}"
                print(reason)
                return True, reason

            else:
                result = f'Failed to locate data in location {destinationURL}'

                print(reason)
                return False, result

        except  Exception as e:
            reason = (
                f"Failed to locate data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to locate data in location {destinationURL}'

            print(reason)
            return False, result