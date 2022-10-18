from abc import ABC, abstractmethod
from typing import Tuple

class CloudSystemInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def upload(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def download(self, sourceURI: str, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def delete(self, destinationURL: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def getFileURL(self, destinationURL: str) -> Tuple[str]:
        pass