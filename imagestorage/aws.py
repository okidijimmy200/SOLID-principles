from cloud_interface import CloudSystemInterface
import boto3
import os
from typing import Tuple

class AWSStorage(CloudSystemInterface):

    def __init__(self, boto, bucket) -> None:
        super().__init__()
        # self.s3_client = boto3.client('s3')
        self.s3_client = boto
        # self.bucket = 'image-store-1995'
        self.bucket = bucket

    def connect(self):
        self.s3_client = boto3.client('s3')
        return True

    def disconnect(self):
       return super().disconnect()
    
    def upload(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        try:
            f = open(f"{sourceURI}", "rb")
            # self.s3.Bucket(self.bucket).put_object(Key=f'{destinationURL}', Body=f)
            self.s3_client.upload_file(sourceURI, self.bucket, destinationURL)

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

    def download(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        try:
            objs = self.s3_client.list_objects(Bucket=self.bucket, Prefix=destinationURL)
            print([object["Key"] for object in objs["Contents"]]
)
            if objs['Contents']:
                # with open(f"{sourceURI}", 'wb') as f:
                    # self.s3_client.download_fileobj(self.bucket, destinationURL.rsplit('/', 1)[-1], f)
                self.s3_client.download_file(self.bucket, destinationURL.rsplit('/', 1)[-1], destinationURL)
                    # print(response)
                reason = f"Data successfully downloaded from aws at {sourceURI} to {destinationURL}"
                print(reason)
                return True, reason

        except  Exception as e:
            reason = (
                f"Failed to download data in location {sourceURI}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to download data in location {sourceURI}'
            print(reason)
            return False, result

    def delete(self, destinationURL: str) -> Tuple[bool, str]:
        print("Deleting Object from bucket")
        try:
            objs = self.s3_client.list_objects(Bucket=self.bucket, Prefix=destinationURL)
            print([object["Key"] for object in objs["Contents"]]
)
            if objs['Contents']:
                self.s3_client.delete_object(Bucket=self.bucket, Key=f"{destinationURL}")
                reason = f"Data successfully removed from aws at {destinationURL}"
                print(reason)
                return True, reason

        except Exception as e:
            reason = (
                f"Failed to remove data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to remove data in location {destinationURL}'
            print(reason)
            return False, result

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        try:
            objs = self.s3_client.list_objects(Bucket=self.bucket, Prefix=destinationURL)
            print([object["Key"] for object in objs["Contents"]]
)
            if objs['Contents']:
                bucket_location = self.s3_client.get_bucket_location(Bucket=self.bucket)
                object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
                bucket_location['LocationConstraint'],
                self.bucket,
                destinationURL)
                reason = f"URL aws path for data at {object_url}"
                print(reason)
                return True, reason

        except  Exception as e:
            reason = (
                f"Failed to locate data in location {destinationURL}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )
            result = f'Failed to locate data in location {destinationURL}'

            print(reason)
            return False, result