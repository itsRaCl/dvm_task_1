class C:
    def __init__(self):
        pass
    def add1(self,x,y):

        return x+y

    @classmethod
    def add2(cls,x,y):
        return x+y



print(C().add1(10,20))
print(C.add2(10,30))