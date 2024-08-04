import token_parse
from lib.type import Types

class Generator:
    def __init__(self, root: token_parse.Node_Print) -> None:
        self.types = Types()
        self.root = root

    def generate(self) -> str:
        interpretation = 'global _start\n_start:\n'
        if self.root.expression.token.type == self.types._STR:
            interpretation = f'print("{self.root.expression.token.value}")'
        if self.root.expression.token.type == self.types._INT:
            interpretation += f'\tmov rax, 60\n\tmov rdi, {self.root.expression.token.value}\n\tsyscall'
        return interpretation