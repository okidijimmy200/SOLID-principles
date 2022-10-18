from unittest import mock
import pytest
from db import DatabaseSystem
from memory import MemorySystem

@pytest.fixture(params = [DatabaseSystem, MemorySystem])
def Implementation(request):
   return request.param

def test_create(Implementation):
   assert Implementation().create('phonebook.json', 'data')

def test_read(Implementation):
   assert Implementation().read('phonebook.json')

def test_update(Implementation):
   assert Implementation().update('phonebook.json', 'data-2')

def test_delete(Implementation):
   assert Implementation().delete('phonebook.json')