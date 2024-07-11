from copy import deepcopy
class A():
    def test():
        pass
    
a = A 

dict_1 = {'a':a, 'b':"", 's':{'s':1}}

dict_2 = deepcopy(dict_1)
print(dict_2)