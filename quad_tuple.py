import math 

class QuadTuple:
    """
    >>> q = QuadTuple(1, 'ADD', 'a', 'b', 'c')
    >>> print(q)
    (1) (ADD, a, b, c)
    >>> q[0]
    'ADD'
    >>> q[1]
    'a'
    >>> q[2]
    'b'
    >>> q[3]
    'c'
    >>> p = QuadTuple(2, 'SUB', 'a', 'b')
    >>> print(p)
    (2) (SUB, a, _, b)"""

    def __init__(self, place, *args):
        self.place = place
        self.quad = []

        if len(args) == 3:
            self.quad.append(str(args[0]))
            self.quad.append(str(args[1]))
            self.quad.append("_")
            self.quad.append(str(args[2]))
        elif len(args) == 4:
            for arg in args:
                self.quad.append(str(arg))
        else:
            raise Exception('Invalid number of arguments')
    
    def __str__(self):
        place_str = ('(' + str(self.place) +')').ljust(3)

        quad_str = ', '.join(self.quad)
        quad_str = '(' + quad_str + ')'
        return place_str + ' ' + quad_str

    def __getitem__(self, key: int):
        return self.quad[key]