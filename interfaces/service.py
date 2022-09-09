from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join
import json
import os
import shutil
from typing import List, Dict, Tuple

# imagestore

class DBInterface(ABC):
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

    @abstractmethod
    def copyFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def listFilesInDirectory(self, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def checkIfFileExists(self, destinationURL: str) -> Tuple[bool]:
        pass

    @abstractmethod
    def createDirectory(self, destinationURL: str) -> Tuple[bool]:
        pass

    @abstractmethod
    def deleteDirectory(self, destinationURL: str) -> Tuple[bool]:
        pass

"""Filesystem database
"""
class FilesystemDatabase(DBInterface):
    def connect(self):
        self.base_path = "temp"
        return True

    def disconnect(self):
        return super().disconnect()

    def uploadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print(f"Uploading file to location {destinationURL}")
        try:
            f = open(f"{sourceURI}.json")
            data = json.load(f)

            with open(f"temp/{destinationURL}.json", "w") as f:
                json.dump(data, f)

            reason = f"Data created successfully in location {destinationURL}"
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
        print(f"Downloading data from location {destinationURL}")

        try:
            f = open(f"temp/{destinationURL}.json")
            data = json.load(f)
            
            with open(f"{sourceURI}.json", "w") as f:
                json.dump(data, f)

            reason = f"Data downloaded successfully in location {destinationURL}"
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
        try:
            if os.path.exists(f"temp/{destinationURL}.json"):
                os.remove(f"temp/{destinationURL}.json")
                reason = f"JSON {destinationURL} removed"
                print(reason)
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}") 

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        try:
            if os.path.exists(f"temp/{destinationURL}.json"):
                uri = f"http://localhost:8080/temp/{destinationURL}"
                reason = f"url path for {destinationURL} is {uri}"
                print(reason)
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    def copyFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        try:
            if os.path.exists(f"temp/{destinationURL}.json"):
                shutil.copy(f"temp/{destinationURL}.json", f"copy/{sourceURI}.json")
                reason = f"file copied to copy/{sourceURI}"
                print(reason)
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")
        
    def listFilesInDirectory(self, destinationURL) -> Tuple[bool, str]:
        try:
            if os.path.exists(f"temp/{destinationURL}.json"):
                onlyfiles = [f for f in listdir(f"temp/") if isfile(join(f"temp/", f))]
                reason = f"Files in the directory {onlyfiles}"
                print(reason)
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}") 

    def checkIfFileExists(self, destinationURL: str) -> Tuple[bool]:
        try:
            if os.path.exists(f"temp/{destinationURL}.json"):
                reason = f"File {destinationURL}.json exists"
                print(reason)
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    def createDirectory(self, destinationURL: str) -> Tuple[bool]:
        try:
            pathCWD = f"{os.getcwd()}/{destinationURL}"
            if os.path.isdir(pathCWD) is False:
                path = os.path.join(os.path.dirname(__file__), destinationURL)
                mode = 0o666
                os.mkdir(path, mode)
                reason = f"Directory {destinationURL} created"
                print(reason)
                return True, reason
            else:
                reason = "File exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    def deleteDirectory(self, destinationURL: str) -> Tuple[bool]:
        try:
            pathCWD = f"{os.getcwd()}/{destinationURL}"
            if os.path.isdir(pathCWD):
                path = os.path.join(os.path.dirname(__file__), destinationURL)
                os.rmdir(path)
                reason = f"Directory {destinationURL} deleted"
                print(reason)
                return True, reason
            else:
                reason = "File Doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    @staticmethod
    def getInstance() -> "FilesystemDatabase":
        return FilesystemDatabase()


if __name__ == '__main__':
    sourceURI = 'test'
    destinationURL = 'phone'
    FilesystemDatabase().deleteDirectory(destinationURL)