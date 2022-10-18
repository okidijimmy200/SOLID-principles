from typing import Dict, Tuple
import json
import os
from interface import PhoneBookInterface

# filesystemDatabase
class MemorySystem(PhoneBookInterface):
    def connect(self):
        self.base_path = "temp"
        return True

    def disconnect(self):
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"Creating data in location {location}")
        try:
            with open(f"{location}", "w") as f:
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
            f= open(f"{location}")
            data = json.load(f)
            reason =f"Data read from {location}"
            return True, reason, data
        except BaseException as err:
            reason = (f"Unexpected {err=}, {type(err)=}")
            print(reason)
            data= None
            # return False, data, reason
            return False, reason, data

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        try:
            f= open(f"{location}")
            old_data = json.load(f)
            # merge json files
            z = dict(list(old_data.items()) + list(data.items()))

            with open(f"{location}", "w") as f:
                json.dump(z, f)

            reason = f"Data updated successfully in location"
            print(reason)
            return True, reason, z
        except  BaseException as err:
            result = (f"Unexpected {err=}, {type(err)=}")
            print(result)
            # for db
            data = ''
            return False, result, data

    def delete(self, location: str) -> Tuple[bool, str]:
        try:
            if os.path.exists(f"{location}"):
                os.remove(f"{location}")
                reason = f"JSON {location} removed"
                return True, reason
            else:
                reason = "File doesnot exist"
                print(reason)
                return False, reason

        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")

    @staticmethod
    def getInstance() -> "MemorySystem":
        return MemorySystem()