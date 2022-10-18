from typing import Tuple
from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from interface import PhoneBookInterface


# connect to mysql
SQLALCHAMY_DATABASE_URL = 'mysql://root:j4e4s4u4s.@localhost:3306/phonebook'


engine = create_engine(SQLALCHAMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()


# create model for PhoneBook
class PhoneBook(Base):
    __tablename__ = 'phonebook'
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String(100), index=True)

    def __repr__(self):
        return 'id: {}, body: {}'.format(self.id, self.body)

Base.metadata.create_all(engine)

class DatabaseSystem(PhoneBookInterface):

    def __init__(self) -> None:
        super().__init__()
        self.db = SessionLocal()
        # yield self.db

    def connect(self):
        print("-Connecting to MYSQL Database")

    def disconnect(self):
        print("-Disconnecting from MYSQL Database")

    def create(self, location: str, data: str) -> Tuple[bool, str]:
        try:
            new_data = PhoneBook(body=data)
            self.db.add(new_data)
            self.db.commit()
            self.db.refresh(new_data)
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

    def read(self, location: str) -> Tuple[bool, str]:
        try:
            new_data = self.db.query(PhoneBook).all()
            reason = f"Data from MYSQL database at {location}"
            print(reason, new_data)
            return (True, reason, new_data)

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            data = ''
            print(reason)
            return False, data, reason

    def update(self, location: str, data: str) -> Tuple[bool, str]:
        try:
            new_data = self.db.query(PhoneBook).filter(PhoneBook.id == location).first()
            new_data.body = data
            self.db.commit()
            if not new_data:
                return {'detail': f'Data with the id {id} is not available'}

            reason = f"Data updated from MYSQL database at {location}"
            print(True, reason, new_data)
            return True, reason, new_data

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            data = ''
            print(reason)
            return False, reason, data

    def delete(self, location: str) -> Tuple[bool, str]:
        try:
            new_data = self.db.query(PhoneBook).filter(PhoneBook.id == location).delete()
            if not new_data:
                return {'detail': f'Data with the id {id} is not available'}

            reason = f"Data with id {location} has been deleted from database"
            print(True, reason)
            return (True, reason)

        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason