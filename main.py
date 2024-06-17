from my_parser import Parser

if __name__ == "__main__":
    code = """
    a = 5;
    b = 6;
    c = a + b;
    d = a[1]
    """
    parser = Parser(code)
    parser.parse()
    parser.quad_gen.print_quads()