from quad_generator import QuadGenerator
from lexer import tokenize

def width(ndim):
    return f'width_{ndim}'
    dims = [i for i in range(6, 11)]
    dims.reverse()
    res = 1
    for i in range(ndim):
        res *= dims[i]
    
    return res

def unit_size(ndim):
    return 'unit_size'

class Parser:
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.token_index = 0
        self.quad_gen = QuadGenerator()

    def match(self, expected_type):
        if self.token_index < len(self.tokens) \
            and self.current_token[0] == expected_type:
            self.token_index += 1
        else:
            raise SyntaxError(f"Expected {expected_type} but got {self.current_token}")
    
    @property
    def next_token(self):
        if self.token_index < len(self.tokens)-1:
            return self.tokens[self.token_index+1]
        else:
            return None

    @property
    def current_token(self):
        if self.token_index < len(self.tokens):
            return self.tokens[self.token_index]
        return None

    def parse(self):
        self.S()
        # self.quad_gen.print_quads()
        return self.quad_gen
        

    def S(self):
        self.A()
        if self.current_token:
            self.S()

    def A(self):
        lhs_dic = self.LHS()
        self.match('ASSIGN')
        e_dic = self.E()
        self.match('SEMICOLON')
        self.quad_gen.gen("=", lhs_dic['addr'], e_dic['addr'])

    def LHS(self):
        if self.current_token[0] == 'ID':
            id_token = self.current_token[1]
            self.match('ID')
            if self.current_token[0] == 'LBRACKET':
                self.match('LBRACKET')
                e_list_dic = self.E_list()
                self.match('RBRACKET')
                lhs_ndim = e_list_dic['ndim'] + 1
                array_list_offset = self.quad_gen.newtmp()
                # array_offset = self.quad_gen.newtmp()
                self.quad_gen.gen('*', unit_size(e_list_dic['ndim']), e_list_dic['addr'], array_list_offset)
                # lhs_addr = self.quad_gen.newtmp()
                lhs_addr = self.quad_gen.newtmp()
                self.quad_gen.gen('[]', id_token, array_list_offset , lhs_addr)
            else:
                lhs_addr = id_token
                lhs_ndim = 0
            return {'addr': lhs_addr, 'ndim': lhs_ndim}
        raise SyntaxError(f"Unexpected token {self.current_token} in LHS")

    def E_list(self):
        if self.current_token[0] == 'NUM' or self.current_token[0] == 'ID' or self.current_token[0] == 'LPAREN':
            e_dic = self.E()
            if self.current_token[0] == 'COMMA':
                self.match('COMMA')
                e_list_tail_dic = self.E_list()
                e_list_addr = self.quad_gen.newtmp()
                e_list_ndim = e_list_tail_dic['ndim'] + 1
                self.quad_gen.gen("*", e_dic['addr'], width(e_list_ndim), e_list_addr)
                self.quad_gen.gen("+", e_list_addr, e_list_tail_dic['addr'], e_list_addr)
            else:
                e_list_addr = e_dic['addr']
                e_list_ndim = 1
            return {'addr': e_list_addr, 'ndim': e_list_ndim}
        raise SyntaxError('Syntax error in "[]"')


    def E(self):
        t_dic = self.T()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            current_token = self.current_token[1]
            self.match(self.current_token[0])
            new_t_dic = self.T()
            e_addr = self.quad_gen.newtmp()
            self.quad_gen.gen(current_token, t_dic['addr'], new_t_dic['addr'], e_addr)
            t_dic = {'addr': e_addr}
            
        e_addr = t_dic['addr']
        return {'addr': e_addr}

    def T(self):
        f_dic = self.F()
        # T -> T * F | T / F
        while self.current_token[0] in ['TIMES', 'DIVIDE']:
            current_token = self.current_token[1]
            self.match(self.current_token[0])
            new_f_dic = self.F()
            t_addr = self.quad_gen.newtmp()
            self.quad_gen.gen(current_token, f_dic['addr'], new_f_dic['addr'], t_addr)
            f_dic = {'addr': t_addr}
        # T -> F
        t_addr = f_dic['addr']
        return {'addr': t_addr}
    

    def F(self):
        # F -> (E)
        if self.current_token[0] == 'LPAREN':
            self.match('LPAREN')
            e_dic = self.E()
            self.match('RPAREN')
            f_addr = e_dic['addr']
        elif self.current_token[0] == 'ID':
            id_token = self.current_token[1]
            self.match('ID')
            # F -> id [ E_list ]
            if self.current_token[0] == 'LBRACKET':
                self.match('LBRACKET')
                e_list_dic = self.E_list()
                self.match('RBRACKET')
                array_list_offset = self.quad_gen.newtmp()
                self.quad_gen.gen("*", unit_size(e_list_dic['ndim']), e_list_dic['addr'], array_list_offset)
                f_addr = self.quad_gen.newtmp()
                self.quad_gen.gen("[]", id_token, array_list_offset, f_addr)
            # F -> id
            else:
                f_addr = id_token
        # F -> NUM
        elif self.current_token[0] == 'NUM':
            num_token = self.current_token[1]
            self.match('NUM')
            f_addr = num_token
        else:
            raise SyntaxError(f"Unexpected token {self.current_token} in F")
        return {'addr': f_addr}