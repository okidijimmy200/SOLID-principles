import xml.etree.ElementTree as etree

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

'''The JSONConnector class parses the JSON file and has a parsed_data() method that returns all data as a dictionary (dict). The property decorator is used to make parsed_data() appear as a normal variable instead of a method'''

class JSONConnector:
    def __init__(self, filepath):
        self.data = dict()

        with open(filepath, mode='r',encoding='utf-8') as f:
            self.data = json.load(f)



@property

def parsed_data(self):

    return self.data


'''The XMLConnector class parses the XML file and has a parsed_data() method that returns all data as a list of xml.etree.Element '''

class XMLConnector:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree

'''The connection_factory() function is a Factory Method. It returns an instance of JSONConnector or XMLConnector depending on the extension of the input file path'''

def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector

    elif filepath.endswith('xml'):
        connector = XMLConnector

    else:
        raise ValueError('Cannot connect to {}'.format(filepath))

    return connector(filepath)

'''The connect_to() function is a wrapper of connection_factory().'''
def connect_to(filepath):
    factory = None

    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)

'''The main() function demonstrates how the Factory Method design pattern can be used. The first part makes sure that exception handling is effective'''
def main():
    sqlite_factory = connect_to('person.sq3')

'''The next part shows how to work with the XML files using the Factory Method. XPath is used to find all person elements that have the last name Liar. For each matched person, the basic name and phone number information are shown'''
xml_factory = connect_to(Path(BASE_DIR).joinpath('person.xml'))

xml_data = xml_factory.parsed_data()

liars = xml_data.findall(".//{person}[{lastName}='{}']".format('Liar'))

print('found: {} persons'.format(len(liars)))

for liar in liars:
    print('first name: {}'.format(liar.find('firstName').text))

    print('last name: {}'.format(liar.find('lastName').text))

    [print('phone number ({}):'.format(p.attrib['type']), p.text) for p in liar.find('phoneNumbers')]

'''The final part shows how to work with the JSON files using the Factory Method. Here, there’s no pattern matching, and therefore the name, price, and topping of all donuts are shown'''
json_factory = connect_to('data/donut.json')

json_data = json_factory.parsed_data

print('found: {} donuts'.format(len(json_data)))

for donut in json_data:
    print('name: {}'.format(donut['name']))

    print('price: ${}'.format(donut['ppu']))

    [print('topping: {} {}'.format(t['id'], t['type'])) for t in donut['topping']]

if __name__ == '__main__':

    main()
