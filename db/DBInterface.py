from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join
import json
from typing import List, Dict, Tuple

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