# Borg is also known as monostate. In the borg pattern, all of the instances are different, but they share the same state.

'''In the following code , the shared state is maintained in the _shared_state attribute. And all new instances of the Borg class will have this state as defined in the __new__ class method'''

class Borg(object):

    _shared_state = {}

    def __new__(cls, *args, **kwargs):

        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj
'''Generally, Python stores the instance state in the __dict__ dictionary 
and when instantiated normally, every instance will have its own __dict__. 
But, here we deliberately assign the class variable _shared_state to all of the created instances.'''

# Here is how it works with subclassing:

class Child(Borg):
    pass

borg = Borg()
another_borg = Borg()

print(borg is another_borg) #False

# child = Child()
borg.only_one_var = 'I am the only one var'
'''So, despite the fact that you can’t compare objects by their identity, using the is statement, all child objects share the parents’ state.'''
# print(child.only_one_var)

'''If you want to have a class, which is a descendant of the Borg class 
but has a different state, you can reset shared_state as follows:'''


class AnotherChild(Borg):
    _shared_state = {}

another_child = AnotherChild()
print(another_child.only_one_var)


'''NBs:
Which type of singleton should be used is up to you. 
If you expect that your singleton will not be inherited, you can choose the classic singleton; otherwise, it’s better to stick with borg.
'''
