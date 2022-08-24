import os
from abc import ABC, abstractmethod
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
    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def read(self, location: str) -> Tuple[bool, str, Dict[str,str]]:
        pass

    @abstractmethod
    def readAll(self, location: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        pass

    @abstractmethod
    def update(self, location: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def delete(self, location: str) -> Tuple[bool, str]:
        pass

"""FileSystem DB
"""

class FileSystemDatabase(DBInterface):
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

    def readAll(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        pass

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
    def getInstance() -> "FileSystemDatabase":
        return FileSystemDatabase()


class InMemoryDB(DBInterface):
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    def connect(self):
        print("-Connecting to In Memory Database")

    def disconnect(self):
        print("-Disconnecting from In Memory Database")

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"-Creating data in location {location}")
        self.data[location] = data
        reason = f"-Data created successfully in location {location}"
        print(reason)
        return True, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        print("-Reading data from In Memory Database")
        print(self.data)
        
    
    def readAll(self, location: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        pass

    def update(self, location: str) -> Tuple[bool, str]:
        pass

    def delete(self):
        print("-Deleting data from In Memory Database")


class PhoneBookSystem:
    def __init__(self, db_service_provider: DBInterface) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup completed")

    def createContact(self, data: dict) -> Tuple[bool, str]:
        print("Creating contact")

        phone = data['phone']

        created, reason = self.db.create(phone, data)

        if not created:
            print(reason)
            return True, reason

    def readContact(self, data: dict) -> Tuple[bool, str]:
        print("Reading from db")

        phone = data['phone']
        read, reason, data = self.db.read(phone)

        if not read:
            print(reason)
            return True, reason
        
        print(data)
        return data

    def updateContact(self, data: dict) -> Tuple[bool, str]:
        print("Updating contact")

        phone = data['phone']

        updated, reason = self.db.update(phone, data)

        if not updated:
            print(reason)
            return True, reason

    def deleteContact(self, data: dict) -> Tuple[bool, str]:
        print("Deleting contact")

        phone = data["phone"]

        deleted, reason = self.db.delete(phone)

        if not deleted:
            print(reason)
            return True, reason
        


    # system teardown
    def tearDownSystem(self) -> None:
        print("Shutting down system")
        self.db.disconnect()
        print("System shutdown complete")

# main.py

# Phone book system usage

# interchanging these should have no effect on system behaviour

database_service = InMemoryDB()
# database_service = FileSystemDatabase.getInstance()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

name = "Person"
phone = "0787870021"
age = 26

# phone_book_system.createContact({"name": name, "phone": phone})
phone_book_system.readContact({"phone": phone})
# phone_book_system.updateContact({"phone": phone, "age": age})
# phone_book_system.deleteContact({"phone": phone})
phone_book_system.tearDownSystem()


