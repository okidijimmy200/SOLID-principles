import json
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod

'''https://towardsdatascience.com/solid-coding-in-python-1281392a6a94'''

class DatabaseInterface(ABC):
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
    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
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


class FileSystemDatabase(DatabaseInterface):
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
            reason = f"-Data created successfully in location {location}"
            print(reason)
            return True, reason
        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        return True, "", {}

    def readAll(self, location: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        pass

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        return True, ""

    def delete(self, location: str) -> Tuple[bool, str]:
        return True, ""

    @staticmethod
    def getInstance() -> "FileSystemDatabase":
        return FileSystemDatabase()


class InMemoryDatabase(DatabaseInterface):
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
        print(self.data)
        reason = f"-Data created successfully in location {location}"
        print(reason)
        return True, reason

    def read(self):
        print("-Reading data from In Memory Database")
    
    def readAll(self, location: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        pass

    def update(self, location: str) -> Tuple[bool, str]:
        pass

    def delete(self):
        print("-Deleting data from In Memory Database")


# Phone book system implementation


class PhoneBookSystem:
    # # System set up

    # SOLID:
    # - Single Responsibility Principle
    # - Open/Closed Principle
    # - Liskov Substitution Principle
    # - Interface Segregation Principle
    # - Dependency Inversion Principle

    def __init__(self, db_service_provider: DatabaseInterface) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup complete")

    # # End of system setup

    # # System functionality
    def createContact(self, data: dict) -> Tuple[bool, str]:
        print("Creating contact")

        phone = data["phone"]

        created, reason = self.db.create(phone, data)
        if not created:
            print(reason)
            return False, reason

        reason = "Contact created successfully"
        print(reason)
        return True, reason

    # # End of system functionality

    # # System tear down
    def tearDownSystem(self) -> None:
        print("Shutting down system")
        self.db.disconnect()
        print("System shut down complete")

    # # End of system tear down

    # End of phone book system implementation


# main.py

# Phone book system usage

# interchanging these should have no effect on system behaviour

# database_service = InMemoryDatabase()
database_service = FileSystemDatabase.getInstance()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

# name = input("Enter name: ")
# phone = input("Enter phone: ")

name = "Person"
phone = "0787870021"

phone_book_system.createContact({"name": name, "phone": phone})

phone_book_system.tearDownSystem()
