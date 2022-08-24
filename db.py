from abc import ABC, abstractmethod
from pickle import TUPLE
from typing import List, Dict, Tuple
import json
import os

class DatabaseBInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def read(self, location: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def delete(self, location: str) -> Tuple[bool, str]:
        pass

class FileSystem(DatabaseBInterface):
    def connect(self):
        self.base_path = "temp"
        return True

    def disconnect(self):
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"Creating data in location {location}")
        try:
            with open(f"{self.base_path}/{location}.json", "w") as f:
                json.dump(data, f)
            reason = f"Data created successfully in location {location}"
            print(reason)
            return True, reason

        except  Exception as e:
            reason = (
                f"Failed to create data in location {location}, reason:" 
                + f"{type(e).__name__} {str(e)}"
            )

            print(reason)
            return False, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        try:
            f= open(f"{self.base_path}/{location}.json")
            data = json.load(f)
            reason =f"Data read from {location}"
            return True, reason, data
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        try:
            f= open(f"{self.base_path}/{location}.json")
            old_data = json.load(f)
            # merge json files
            z = dict(list(old_data.items()) + list(data.items()))

            with open(f"{self.base_path}/{location}.json", "w") as f:
                json.dump(z, f)

            reason = f"Data updated successfully in location {location}"
            print(reason)
            return True, reason
        except  BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)

    def delete(self, location: str) -> Tuple[bool, str]:
        try:
            if os.path.exists(f"{self.base_path}/{location}.json"):
                os.remove(f"{self.base_path}/{location}.json")
                reason = f"JSON {location} removed"
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    @staticmethod
    def getInstance() -> "FileSystem":
        return FileSystem()

class DatabaseSystem(DatabaseBInterface):
    def connect(self):
        return super().connect()
