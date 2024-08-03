import os
import sys
from lexical_parser import parseText
from token_parse import Token_Parse
from generator import Generator

def build(text) -> str:
    tokens, error = parseText(text)
    if error:
        print(error)
    else:
        head = Token_Parse(tokens).parse()
        return Generator(head).generate() 

def main(argv: list[str]) -> None:
    if len(argv) == 1:
        raise ValueError("need to specify file")
    path = os.getcwd() + "/" + argv[1]

    file = open(path, "r")
    contents = file.read()
    file.close()

    results = build(contents)
    file = open(os.getcwd()+"/"+argv[2], "w")
    file.write(results)
    file.close

    print('file is successfully compiled')
    
if __name__ == '__main__':
    main(sys.argv)