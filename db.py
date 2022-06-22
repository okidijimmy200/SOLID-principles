import sys
import json

from importlib_metadata import metadata

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Provider:
    def __init__(self, fwrite: str,fread: str, fupdate: str, fdelete: str, thisdict: dict):
        self.fwrite = fwrite
        self.thisdict = thisdict
        self.fread = fread
        self.fupdate = fupdate
        self.fdelete = fdelete

    def create(self):
        try:
            self.fwrite.write(json.dumps(self.thisdict))
            result = (True, 'Data saved in file')
            return tuple(result)
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            return tuple(result)
        finally:
            self.fwrite.close()
    
    def read(self):
        try:
            print(self.fread.read())
            return {
                True,
                f'Success',
                self.fread.read()
            }
        except BaseException as err:
            return {
                False, f"Unexpected {err=}, {type(err)=}"}
        finally:
            self.fread.close()

    def update(self):
        try:
            self.fupdate.write(self.thisdict)
            return tuple(True, 'Data has been updated in file')
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            return tuple(result)
        finally:
            self.fupdate.close()

    def delete(self):
        try:
            self.fdelete.truncate(0)
            return tuple(True, 'Data has been deleted in file')
        except BaseException as err:
            return {
                False, f"Unexpected {err=}, {type(err)=}"}
        finally:
            self.fdelete.close()


'''create a db connection'''
class DBConnection(metaclass=SingletonMeta):

    def __init__(self, provider: Provider):
        '''initialize your db connection here'''
        self.provider = provider


def main(dbConnection: DBConnection):
    return dbConnection.provider.create()

if __name__ == "__main__":
    s1 = DBConnection(Provider(
                fwrite=open('test.txt','w'),
                fread=open('test.txt','r'),
                fupdate=open("test.txt", "a"),
                fdelete=open('test.txt', 'r+'),
                thisdict= {
                  "brand": "Ford",
                  "model": "Mustang",
                  "year": 1964
                }
    ))
    s2 = DBConnection(Provider(
                fwrite=open('test.txt','w'),
                fread=open('test.txt','r'),
                fupdate=open("test.txt", "a"),
                fdelete=open('test.txt', 'r+'),
                thisdict= {
                  "brand": "Ford",
                  "model": "Mustang",
                  "year": 1964
                }
    ))

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
    main(
        dbConnection=DBConnection(
            Provider(
                fwrite=open('test.txt','w'),
                fread=open('test.txt','r'),
                fupdate=open("test.txt", "a"),
                fdelete=open('test.txt', 'r+'),
                thisdict= {
                  "brand": "Ford",
                  "model": "Mustang",
                  "year": 1964
                }
            )
        )
    )


