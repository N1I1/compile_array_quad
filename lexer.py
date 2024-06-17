import re

tokens = [
    ('ID', r'[a-zA-Z_]\w*'),
    ('NUM', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('SKIP', r'[ \t]+'),
    ('SEMICOLON',r';'),
    ('COMMA', r','),
    ('MISMATCH', r'.'),
]

def tokenize(code):
    """
    利用正则表达式将字符串分割成token
    >>> tokenize('sum  3 4')
    [('ID', 'sum'), ('NUM', 3), ('NUM', 4)]
    >>> tokenize('([/*+')
    [('LPAREN', '('), ('LBRACKET', '['), ('DIVIDE', '/'), ('TIMES', '*'), ('PLUS', '+')]"""
    token_specification = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in tokens)
    tok_regex = re.compile(token_specification)
    token_list = []
    for mo in tok_regex.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUM':
            value = int(value)
        elif kind in [token[0] for token in tokens if token[0] not in ['NUM', 'SKIP', 'MISMATCH']]:
            pass
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        token_list.append((kind, value))
    return token_list