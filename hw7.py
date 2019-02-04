class MyMeta(type):

    def __new__(cls, name, bases, classdict):
        variables = dict()
        for e in classdict.items():
            if e[0].startswith('get_') or e[0].startswith('set_') or e[0].startswith('del_'):
                var = e[0][4:]
                getter = None
                setter = None
                deleter = None
                for e in classdict.items():
                    if e[0].startswith('get_') and e[0][4:] == var:
                        getter = e[1]
                    if e[0].startswith('set_') and e[0][4:] == var:
                        setter = e[1]
                    if e[0].startswith('det_') and e[0][4:] == var:
                        deleter = e[1]
                variables.update({var: property(getter, setter, deleter)})
        for i in variables.items():
            print(i)
        classdict.update(variables)
        return type.__new__(cls, name, bases, classdict)

    def __init__(cls, name, bases, classdict):
        type.__init__(cls, name, bases, classdict)


class Example(metaclass=MyMeta):

    def __init__(self):
        self._x = None

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def get_y(self):
        return 'y'

    def set_z(self, val):
        self._z = val


ex = Example()
ex.x = 255
ex.z = 666
print(ex.x)
print(ex.y)
# print(ex.z)
