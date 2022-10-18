from cloud_interface import CloudSystemInterface
from typing import Tuple
from minios import MinioStorage
from aws import AWSStorage

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

        created, reason = self.cloud.upload(sourceURI, destinationURL)

        if not created:
            print(reason)
            return False, reason
        return True, reason
        
    def deleteFile(self, data: str) -> Tuple[bool, str]:

        destinationURL = data

        deleted, reason = self.cloud.delete(destinationURL)

        if not deleted:
            print(reason)
            return False, reason
        return True, reason

    def downloadFile(self, data: dict) -> Tuple[bool, str]:

        sourceURI = data['uri']
        destinationURL = data['url']

        downloaded, reason = self.cloud.download(sourceURI, destinationURL)

        if not downloaded:
            print(reason)
            return False, reason
        return True, reason

    def getFileURL(self, data: str) -> Tuple[bool, str]:
        result, reason = self.cloud.getFileURL(data)

        if not result:
            print(reason)
            return False, reason
        return True, reason

database_service = MinioStorage()
# database_service = AWSStorage()

image_storage_system = ImageStorageSystem(database_service)
image_storage_system.setUpSystem()

# sourceURI = 'files/AI.jpg'
# destinationURL = 'zeus/AI.jpg'

# for minioa
sourceURI = 'files/AI.jpg'
destinationURL = 'files/AI.jpg'


'''sudo service mysql start'''
# for downloading
# sourceURI = 'zeus/AI.jpg'
# destinationURL = 'files/AI.jpg'


# image_storage_system.uploadFile({'uri': sourceURI, 'url': destinationURL})
# image_storage_system.deleteFile(destinationURL)
# image_storage_system.downloadFile({'uri': sourceURI, 'url': destinationURL})
# image_storage_system.getFileURL(destinationURL)

