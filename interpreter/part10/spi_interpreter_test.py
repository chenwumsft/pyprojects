from spi_lexer import *
from spi_parser import *
from spi_interpreter import *

source_code = ''
with open('part10.pas', 'r') as f:
    for ln in f:
        source_code += ln

print source_code

l = Lexer(source_code)
p = Parser(l)
interpreter = Interpreter(p)
interpreter.interpret()
print(interpreter.GLOBAL_SCOPE)