import logging
from interperter import Interpreter

def main():
    import sys

    logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

    interpreter = Interpreter()
    result = interpreter.interpret()
    print(result)


if __name__ == '__main__':
    main()
