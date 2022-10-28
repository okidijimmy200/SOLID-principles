PhoneBook Storage:
Designed an interface called inteface.py for phonebook with create, read, update and delete methods.
Created a database implementation of interface called DatabaseSystem which is connected to a MYSQL database.
Also created a Filesystem implementation of interface called MemorySystem where the data is either created, read, deleted or updated from the file created.

Finally created the Phonebook system that implements the Interface injected. 
So the system can either use Database system or MemorySystem to connected to a storage device.

Implemented unit tests for the system with a test badge coverage of 90%.