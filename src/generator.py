import token_parse
from lib.type import Types, Variable

class Generator:
    def __init__(self, root_list: list[token_parse.Node_Prog]) -> None:
        self.types = Types()
        self.variable_map: dict[Variable] = {}
        self.index = -1
        self.root_list = root_list
        self.current_root: token_parse.Node_Prog = None
        self.stack_size = 0
        self.__advance()
    
    def __advance(self):
        self.index += 1
        if self.index == len(self.root_list):
            self.current_root = None
        else:
            self.current_root = self.root_list[self.index]

    def __push(self, register) -> str:
        self.stack_size += 1
        return f'\tpush {register}\n'

    def __pop(self, register) -> str:
        self.stack_size -= 1
        return f'\tpop {register}\n'
        
    def __var_set(self, name, register, val):
        ret = ''
        if name not in self.variable_map.keys():
            self.variable_map[name] = Variable(self.stack_size + 1)
            ret += f'\tmov {register}, {val}\n'
            ret += self.__push(register)
            return ret
        else:
            raise NameError(name, "variable name already exists")

    def __var_get(self, name):
        ret = ''
        if name in self.variable_map.keys():
            var_location = self.variable_map[name].get_stack_loc()
            ret += self.__push(f'QWORD [rsp + {(self.stack_size - var_location) *8}]')
            return ret
        else:
            raise NameError(name, "Variable does not exist")
            
    def __parse_exit(self, expr: token_parse.Node_Expr | token_parse.Leaf):
        out = ''
        if type(expr) == token_parse.Leaf_Factor:
            if expr.get_type() == self.types._VAR:
                out += self.__var_get(expr.get_value())
                out += '\tpop rdi\n'
                return out
            if expr.get_type() == self.types._INT:
                out += f'\tmov rdi, {expr.get_value()}\n'
                return out           
        if expr.get_left():
            out+= self.__parse_exit(expr.get_left()) 
            expr.set_left(None)
        if expr.get_right():
            out += self.__parse_exit(expr.get_right())
            expr.set_right(None)
        return out

    def generate(self) -> str:
        interpretation = 'global _start\n_start:\n'
        while self.current_root:
            if self.current_root.type == self.types._VAR:
                expr: token_parse.Node_Expr = self.current_root.get_expression()
                var_name = expr.get_left().get_operator().get_value()
                value = expr.get_left().get_left().get_value()
                interpretation += self.__var_set(var_name, "rax", value)
                self.__advance() 
            # implement Variables. they should go into rax register than can be pushed to the stack
            # to retirve get offset with stack pointer and push to top of stack then pop it to remove
            # initial thoughts probably better way to do sleepy -_-
            if self.current_root.type == self.types._EXIT:
                expr: token_parse.Node_Expr = self.current_root.get_expression()
                new_exit = self.__parse_exit(expr)
                interpretation += f'\tmov rax, 60\n{new_exit}\tsyscall'
                self.__advance()
        return interpretation    