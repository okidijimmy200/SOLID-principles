from abc import ABC, abstractmethod
from typing import Dict, Tuple
import json
import os
from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


# connect to mysql
SQLALCHAMY_DATABASE_URL = 'mysql://root:j4e4s4u4s.@localhost:3306/imagestore'


engine = create_engine(SQLALCHAMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()


# create model for ImageStore
class ImageStore(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(100), index=True)

    def __repr__(self):
        return 'id: {}, body: {}'.format(self.id, self.body)

Base.metadata.create_all(engine)


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

# filesystemDatabase
class MemorySystem(DatabaseBInterface):
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
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)

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
            return True, reason
        except  BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)

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

class DatabaseSystem(DatabaseBInterface):

    def __init__(self) -> None:
        super().__init__()
        self.db = SessionLocal()
        # yield self.db

    def connect(self):
        print("-Connecting to MYSQL Database")

    def disconnect(self):
        print("-Disconnecting from MYSQL Database")

    def create(self, location: str, data: str, test_db) -> Tuple[bool, str]:
        try:
            new_data = ImageStore(body=data)
            if test_db is None:
                self.db.add(new_data)
                self.db.commit()
                self.db.refresh(new_data)
                reason = f"Data stored succesfully at {location}"
                print(reason)
                return (True, reason)
            else:
                test_db.add(new_data)
                test_db.commit()
                test_db.refresh(new_data)
                reason = f"Data stored succesfully at {location}"
                print(reason)
                return (True, reason)
        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def read(self, location: str, test_db) -> Tuple[bool, str]:
        try:
            if test_db is None:
                new_data = self.db.query(ImageStore).all()
                reason = f"Data from MYSQL database at {location}"
                print(reason, new_data)
                return (True, reason, new_data)
            else:
                new_data = test_db.query(ImageStore).all()
                reason = f"Data from MYSQL database at {location}"
                print(reason, new_data)
                return (True, reason, new_data)

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def update(self, location: str, data: str, test_db) -> Tuple[bool, str]:
        try:
            if test_db is None:
                new_data = self.db.query(ImageStore).filter(ImageStore.id == location).first()
                new_data.body = data
                self.db.commit()
                if not new_data:
                    return {'detail': f'Data with the id {id} is not available'}

                reason = f"Data updated from MYSQL database at {location}"
                print(True, reason, new_data)
                return (True, reason, new_data)

            else:
                new_data = test_db.query(ImageStore).filter(ImageStore.id == location).first()
                new_data.body = data
                test_db.commit()
                if not new_data:
                    return {'detail': f'Data with the id {id} is not available'}

                reason = f"Data updated from MYSQL database at {location}"
                print(reason, new_data)
                return (True, reason, new_data)

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def delete(self, location: str, test_db) -> Tuple[bool, str]:
        try:
            if test_db is None:
                new_data = self.db.query(ImageStore).filter(ImageStore.id == location).delete()
                if not new_data:
                    return {'detail': f'Data with the id {id} is not available'}

                reason = f"Data with id {location} has been deleted from database"
                print(True, reason)
                return (True, reason)
            else:
                new_data = test_db.query(ImageStore).filter(ImageStore.id == location).delete()
                if not new_data:
                    return {'detail': f'Data with the id {id} is not available'}

                reason = f"Data with id {location} has been deleted from database"
                print(reason, new_data)
                return (True, reason)

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

class PhoneBookSystem:
    def __init__(self, db_service_provider: DatabaseBInterface) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup completed")

    def createContact(self, data: dict, test_db=None) -> Tuple[bool, str]:
        print("Creating contact")

        phone = data['phone']

        test = data['name']

        # created, reason = self.db.create(phone, data, test_db)
        # for db
        created, reason = self.db.create(phone, test, test_db)

        if not created:
            print(reason)
            return True, reason
        return reason

    def readContact(self, data: str, test_db=None) -> Tuple[bool, str, Dict[str, str]]:
        print("Reading from db")

        phone = data
        result, reason ,data= self.db.read(phone, test_db)

        if not result:
            print(reason)
            return True, reason
        
        print(data)
        return data

    def updateContact(self, data: dict, test_db=None) -> Tuple[bool, str]:
        print("Updating db")

        id = data["id"]
        phone = data['phone']
        # for db system
        updated, reason, data = self.db.update(id, phone, test_db)
        # for memory
        # updated, reason = self.db.update(id, data, test_db)

        if not updated:
            print(reason)
            return True, reason
        # return reason
        print(data)
        return data

    def deleteContact(self, data: dict, test_db=None) -> Tuple[bool, str]:
        print("Deleting contact from db")

        id = data["id"]
        data, reason = self.db.delete(id, test_db)

        if not data:
            print(reason)
            return True, reason
        return reason
        # print(data)
        # return data

database_service = DatabaseSystem()
# database_service = MemorySystem()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

id = 1
# for memory system
# id = "0788926713.json"
name = "Person-1"
phone = "0788926713.json"
phone2 = "0782142404.json"
# phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.readContact(phone)
# phone_book_system.updateContact({"id": id, "phone": phone2})
'''for memory system'''
# phone_book_system.updateContact({"id": id, "phone": name})
# phone_book_system.deleteContact({"id": id})

