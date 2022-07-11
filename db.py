import abc
import json
import sqlite3

class DBInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create') and
                callable(subclass.create) and
                hasattr(subclass, 'read') and
                callable(subclass.read) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete))


class DBConnectionFILESYSTEM:
    def create(self, path: str, data: dict) -> any:
        try:
            path.write(json.dumps(data))
            result = (True, 'Data saved in file')
            print(result)
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)
        finally:
            path.close()

    def read(self, path: str) -> str:
        try:
            print(True, f'Success', path.read())
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)
        finally:
            path.close()

    def update(self, path: str, data: dict) -> any:
        try:
            path.write(json.dumps(data))
            print((True, 'Data has been updated in file'))
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)
        finally:
            path.close()

    def delete(self, path: str) -> str:
        try:
            path.truncate(0)
            print((True, 'Data has been deleted in file'))
        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}")                
        finally:
            path.close()

class DBConnectionTOSQL:
    def create(self, path: str, msg: dict) -> any:
        connection = sqlite3.connect(f'{path}')
        try:
            with open('schema.sql') as f:
                connection.executescript(f.read())

                cur = connection.cursor()

                cur.execute("INSERT INTO dbInterface (msg) VALUES (?);", (json.dumps(msg),)
                )
            connection.commit()
            connection.close()
            result = (True, 'Data saved in database')
            print(result)
        except BaseException as err:
            result = (False, f"Unexpected {err=}, {type(err)=}")
            print(result)
    
    def read(self, path: str) -> str:
        conn = sqlite3.connect(f'{path}')
        try:
            conn.row_factory = sqlite3.Row
            posts = conn.execute('SELECT * FROM dbInterface').fetchall()
            conn.close()
            for post in posts:
                print(post['msg'])
        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}") 

    def update(self, path: str, msg: dict) -> any:
        connection = sqlite3.connect(f'{path}')
        try:
            cur = connection.cursor()
            sql = '''UPDATE dbInterface set msg = ?
            '''

            cur.execute(sql, (json.dumps(msg),)
                )
            connection.commit()
            connection.close()
            result = (True, 'Data updated in database')
            print(result)
        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}") 

    def delete(self, path:str) -> str:
        connection = sqlite3.connect(f'{path}')
        try:
            cur = connection.cursor()
            sql = '''DELETE FROM dbInterface'''
            
            cur.execute(sql)
            connection.commit()
            result = (True, 'Data deleted')
            print(result)
        except BaseException as err:
            print(False, f"Unexpected {err=}, {type(err)=}") 



if __name__ == '__main__':
    DBConnectionFILESYSTEM().create(
        path=open('test.txt','w'),
        data= {
                  "brand": "Ford",
                  "model": "Mustang",
                  "year": 1964
            }
    )
    DBConnectionFILESYSTEM().read(
        path=open('test.txt','r')
    )
    DBConnectionFILESYSTEM().update(
        path=open('test.txt','w+'),
        data= {
                  "brand": "Musda"
            }
    )
    DBConnectionFILESYSTEM().delete(
        path=open('test.txt', 'r+')
    )
    DBConnectionTOSQL().create(
        path='DB/database.db',
        msg={
                  "brand": "Ford",
                  "model": "Mustang",
                  "year": 1964
            })
    DBConnectionTOSQL().read(
        path='DB/database.db'
    )
    DBConnectionTOSQL().update(
        path='DB/database.db',
        msg={
                  "brand": "cysler",
                  "model": "boomerang",
                  "year": 2019
        })
    DBConnectionTOSQL().delete(
        path='DB/database.db'
    )

    