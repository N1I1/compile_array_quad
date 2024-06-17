from quad_tuple import QuadTuple

class QuadGenerator:
    def __init__(self):
        self.quads = []
        self.nextquad = 0
        self.tmp_count = 0

    def newtmp(self):
        tmp = f"t{self.tmp_count}"
        self.tmp_count += 1
        return tmp

    def gen(self, *args):
        new_quad = QuadTuple(self.nextquad, *args)
        self.nextquad += 1
        self.quads.append(new_quad)

    def print_quads(self):
        for quad in self.quads:
            print(quad)
    
    def __str__(self):
        return '\n'.join(map(str, self.quads))
