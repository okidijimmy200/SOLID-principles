import pytest
from unittest import mock
from main import PhoneBookSystem
import json,tempfile


class Helpers:
    @staticmethod
    def phone_book(db):
        client = PhoneBookSystem(db_service_provider=db)
        data = mock.MagicMock()
        return client, data
        
    @staticmethod
    def input_variables():
        # write data to a particular location
        config = {"id": 1, "name": 'test', "phone": '0788926712.json'}
        tfile = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(config, tfile)
        tfile.flush()
        return tfile
        
@pytest.fixture
def helpers():
    return Helpers