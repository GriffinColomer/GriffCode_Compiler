import token_parse

class Generator:
    def __init__(self, root: token_parse.Node_Print) -> None:
        self.root = root

        
    def generate(self) -> str:
        interpretation: str = ''
        interpretation = f'print("{self.root.expression.token.value}")'
        return interpretation