from cloud_interface import CloudSystemInterface
import boto3
from typing import Tuple

class AWSStorage(CloudSystemInterface):
    def connect(self):
        self.s3 = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        return True

    def disconnect(self):
       return super().disconnect()
    
    def upload(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
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

    def download(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
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

    def delete(self, destinationURL: str) -> Tuple[bool, str]:
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