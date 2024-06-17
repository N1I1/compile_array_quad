from my_parser import Parser
def output_quads(quad_gen):
    with open("output.txt", "w") as file:
        for quad in quad_gen.quads:
            file.write(str(quad) + "\n")

if __name__ == "__main__":
    with open("input.txt", "r") as file:
        code = file.read()
    parser = Parser(code)
    quad_gen = parser.parse()
    quad_gen.print_quads()
    output_quads(quad_gen)
