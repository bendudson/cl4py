'''
Correspondence of Python types and Lisp types in cl4py:

| Python             |     | Lisp               |
|--------------------+-----+--------------------|
| True, False        | <-> | T, NIL             |
| None               | --> | NIL                |
| int                | <-> | integer            |
| float              | <-> | double-float       |
| float              | <-- | single-float       |
| complex            | <-> | (complex *)        |
| string             | <-> | inserted literally |
| list               | <-> | simple-vector      |
| tuple              | --> | list               |
| dict               | <-> | hash-table         |
| cl4py.Cons         | <-> | cons               |
| cl4py.String       | <-> | string             |
| cl4py.LispObject   | <-> | #N? handle         |
| fractions.Fraction | <-> | ratio              |
| numpy.array        | <-> | array              |

'''
import re
from fractions import Fraction

class LispObject:
    def __init__(self, lisp, handle):
        self.lisp = lisp
        self.handle = handle

    def __del__(self):
        try:
            self.lisp.eval('#{}!'.format(self.handle))
        except:
            pass

    def __call__(self, *args):
        return self.lisp.eval(List('CL:FUNCALL', self, *[Quote(arg) for arg in args]))


class ListIterator:
    def __init__(self, elt):
        self.elt = elt

    def __iter__(self):
        return self

    def __next__(self):
        if isinstance(self.elt, Cons):
            value = self.elt.car
            self.elt = self.elt.cdr
            return value
        else:
            raise StopIteration

class Cons:
   def __init__(self, car, cdr):
       self.car = car
       self.cdr = cdr

   def __repr__(self):
       datum = self
       content = ""
       # TODO handle circularity
       while isinstance(datum, Cons):
           content += repr(datum.car)
           datum = datum.cdr
           if isinstance(datum, Cons):
               content += ", "
       if datum != None:
           return "cl4py.Cons(" + repr(self.car) + ", " + repr(self.cdr) + ")"
       return "cl4py.List(" + content + ")"

   def __iter__(self):
       return ListIterator(self)

class String:
    def __init__(self, data):
        if not isinstance(data, str):
            raise RuntimeError("Not a string: " + str(data))
        self.data = data

    def __repr__(self):
        return "cl4py.String(" + repr(self.data) + ")"

    def __str__(self):
        return str(self.data)


def List(*args):
    head = None
    for arg in args[::-1]:
        head = Cons(arg, head)
    return head


def Quote(arg):
    return List('CL:QUOTE', arg)
