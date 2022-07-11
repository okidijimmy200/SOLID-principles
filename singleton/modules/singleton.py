'''Check whether a module is already imported. If yes, return it. If not, find a module, initialize it, and return it.
Initializing a module means executing a code, including all module-level assignments.
When you import the module for the first time, all of the initializations will be done; however, if you try to import the module for the second time, Python will return the initialized module. Thus, the initialization will not be done, and you get a previously imported module with all of its data.'''

only_one_var = 'I am only one var'

'''This function is quick and sometimes is all that you need; however, we need to consider the following points:

It’s pretty error-prone. For example, if you happen to forget the global statements, variables local to the function will be created and, the module’s variables won’t be changed, which is not what you want.
It’s ugly, especially if you have a lot of objects that should remain as singletons.
They pollute the module namespace with unnecessary variables.
They don’t permit lazy allocation and initialization; all global variables will be loaded during the module import process.
It’s not possible to re-use the code because you can not use the inheritance.
No special methods and no object-oriented programming benefits at all.'''