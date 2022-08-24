import os
import io
import shutil
from os import listdir
from os.path import isfile, join
import json
from typing import List, Dict, Tuple
from DBInterface import DBInterface

class InMemoryDB(DBInterface):
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    def connect(self):
        print("-Connecting to In Memory Database")

    def disconnect(self):
        print("-Disconnecting from In Memory Database")

    def uploadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        f = open(f"{sourceURI}.json")
        data1 = f.read()
        self.data[destinationURL] = data1
        print(self.data)
        reason = f"-Data created successfully in location {destinationURL}"
        print(reason)
        return True, reason, self.data

    def downloadFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        print("-Reading data from In Memory Database")
        
        print(self.data)

    def deleteFile(self, destinationURL: str) -> Tuple[bool, str]:
        return super().deleteFile(destinationURL)

    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        pass

    def copyFile(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    def listFilesInDirectory(self, destinationURL: str) -> Tuple[bool, str]:
        pass

    def checkIfFileExists(self, destinationURL: str) -> Tuple[bool]:
        pass

    def createDirectory(self, destinationURL: str) -> Tuple[bool]:
        pass

    def createDirectory(self, destinationURL: str) -> Tuple[bool]:
        pass

    def deleteDirectory(self, destinationURL: str) -> Tuple[bool]:
        pass

if __name__ == '__main__':
    sourceURI = 'test'
    destinationURL = 'phone'
    InMemoryDB().downloadFile(sourceURI, destinationURL)