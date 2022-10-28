from interface import PhoneBookInterface
from typing import Dict, Tuple
from memory import MemorySystem
from db import DatabaseSystem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db import SessionLocal

class PhoneBookSystem:
    def __init__(self, db_service_provider: PhoneBookInterface) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup completed")

    def createContact(self, data: dict) -> Tuple[bool, str]:
        print("Creating contact")

        phone = data['phone']

        test = data['name']

        # created, reason = self.db.create(phone, data, test_db)
        # for db
        created, reason = self.db.create(phone, test)

        if not created:
            print(reason)
            return False, reason
        return True, reason

    def readContact(self, data: str) -> Tuple[bool, str, Dict[str, str]]:
        print("Reading from db")

        phone = data
        result, reason ,data= self.db.read(phone)

        if not result:
            print(reason)
            return False, reason, data
        
        print(data)
        return True, reason, data

    def updateContact(self, data: dict) -> Tuple[bool, str]:
        print("Updating db")

        id = data["id"]
        phone = data['phone']
        # for db system
        # updated, reason, data = self.db.update(id, phone)
        # for memory
        updated, reason, data = self.db.update(id, data)

        if not updated:
            print(reason)
            return False, reason, data
        # return reason
        print(data)
        return True, reason, data

    def deleteContact(self, data: dict) -> Tuple[bool, str]:
        print("Deleting contact from db")

        id = data["id"]
        data, reason = self.db.delete(id)

        if not data:
            print(reason)
            return False, reason
        return True, reason
        # print(data)
        # return data
    def disconnect(self):
        print("Shutting down system")
        self.db.disconnect()
        print("System shut down")

session_local = SessionLocal()
database_service = DatabaseSystem(session_local)
# database_service = MemorySystem()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

id = 1
# for memory system
# id = "0788926713.json"
name = "Person-456"
phone = "0788926713.json"
phone2 = "0782142404.json"
phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.readContact(id)
# phone_book_system.updateContact({"id": id, "phone": phone2})
'''for memory system'''
# phone_book_system.updateContact({"id": id, "phone": name})
# phone_book_system.deleteContact({"id": id})

