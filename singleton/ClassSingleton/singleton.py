'''Classic singleton
In classic singleton in Python, we check whether an instance is already created. If it is created, we return it; otherwise, we create a new instance, assign it to a class attribute, and return it.'''


class Singleton(object):

    '''Here, before creating the instance, we check for the special __new__ method, which is called right before __init__ if we had created an instance earlier. If not, we create a new instance; otherwise, we return the already created instance.'''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)

        return cls.instance

singleton = Singleton()

another_singleton = Singleton()

print(singleton is another_singleton)

singleton.only_one_var = 'I am only one'

another_singleton.only_one_var

# print(another_singleton.only_one_var)

'''Try to subclass the Singleton class with another one.'''

class Child(Singleton):
    '''If it’s a successor of Singleton, all of its instances should also be the 
    instances of Singleton, thus sharing its states. But this doesn’t work as illustrated in the following'''
    pass

child = Child()

# print(child is singleton)
# print(child.only_one_var)


