class Types:
    def __init__(self) -> None:
        self.DIGITS = '0123456789'

        self._INT = 'INT'
        self._FLOAT = 'FLOAT'
        self._STR = 'STRING'
        self._PLUS = 'PLUS'
        self._MINUS = 'MINUS'
        self._MUL = 'MUL'
        self._DIV = 'DIV'
        self._OPARAN = 'OPARAN'
        self._CPARAN = 'CPARAN'
        self._EQUALS = 'EQUALS'
        self._VAR = 'VARIABLE'
        self._PRINT = 'PRINT'
        self._RET = 'RETURN'
        self._EXIT = 'EXIT'

        self._OPERATORS = {'+': self._PLUS, '-': self._MINUS, '*': self._MUL, '/': self._DIV, '=': self._EQUALS}
        self._MAP = {'(': self._OPARAN, ')': self._CPARAN, '>': self._PRINT}
        self._KEY_MAP = {'exit': self._EXIT, 'return': self._RET, 'var': self._VAR}
    
    def get_key_types(self) -> list[str]:
        return self._KEY_MAP.values()

class Variable:
    def __init__(self, stack_location, type = None) -> None:
        self.stack_location = stack_location
        self.type = type
        
    def get_stack_loc(self):
        return self.stack_location