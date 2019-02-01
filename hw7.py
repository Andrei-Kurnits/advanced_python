class MyMeta(type):

    def __new__(cls, name, bases, classdict):
        print("Meta new")
        classdict['getx'] = MyMeta.getx
        classdict['setx'] = MyMeta.setx
        classdict['delx'] = MyMeta.delx
        return type.__new__(cls, name, bases, classdict)

    def __init__(cls, name, bases, classdict):
        print("Meta init")
        cls.__x = None
        type.__init__(cls, name, bases, classdict)

    def getx(self):
        return self.__x

    def setx(self, value):
        self.__x = value

    def delx(self):
        del self.__x


class MyClass(metaclass=MyMeta):
    def __init__(self):
        print("MyClass.__init__")


o1 = MyClass()
o2 = MyClass()

o1.setx(666)
o2.setx(111)
# print(o1.__x, o2.__x)
print(o1.getx(), o2.getx())

print(dir(MyClass))
print(dir(o1))

