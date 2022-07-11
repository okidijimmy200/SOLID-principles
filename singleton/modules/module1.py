import singleton

'''Here, if you try to import a global variable in a singleton module and change its value in the module1 module, module2 will get a changed variable.'''
print(singleton.only_one_var)

singleton.only_one_var += " after modification"

import singleton.modules.module2 as module2