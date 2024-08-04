import token_parse
from lib.type import Types

class Generator:
    def __init__(self, root_list: list[token_parse.Node_Prog]) -> None:
        self.types = Types()
        self.index = -1
        self.root_list = root_list
        self.current_root: token_parse.Node_Prog = None
        self.__advance()
    
    def __advance(self):
        self.index += 1
        if self.index == len(self.root_list):
            self.current_root = None
        else:
            self.current_root = self.root_list[self.index]

    def generate(self) -> str:
        interpretation = 'global _start\n_start:\n'
        while self.current_root:
            if self.current_root.type == self.types._EXIT:
                expr: token_parse.Node_Expr = self.current_root.get_expression()
                interpretation += f'\tmov rax, 60\n\tmov rdi, {expr.get_left().get_value()}\n\tsyscall'
                self.__advance()
        return interpretation    

            # if self.root.expression.token.type == self.types._INT:
            #     interpretation += f'\tmov rax, 60\n\tmov rdi, {self.root.expression.token.value}\n\tsyscall'
            # return interpretation