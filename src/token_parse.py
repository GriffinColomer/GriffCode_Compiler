from lexical_parser import Token, Types

class Node_Expr:
    def __init__(self, token) -> None:
        self.token = token

class Node_Print(Node_Expr):
    def __init__(self, expression) -> None:
        super().__init__(expression.token)
        self.expression = expression

class Token_Parse:
    def __init__(self, tokens: list[Token]) -> None:
        self.types = Types()
        self.index = -1
        self.tokens = tokens
        self.current_token = None
        self.__advance()

    def __advance(self) -> None:
        self.index += 1
        if self.index == len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def __parse_expr(self) -> Node_Expr | None:
        self.__advance()
        if self.current_token.type == self.types._STR:
            return Node_Expr(self.current_token)
        else:
            return None

    def parse(self) -> Node_Print | None:
        print_node = None
        while self.current_token:
            if(self.current_token.type == self.types._PRINT):
                expersssion = self.__parse_expr() 
                if expersssion:
                    print_node = Node_Print(expersssion)
            self.__advance()
        return print_node
    
# def interpret_tokens(tokens: list[Token]) -> str:
#     interpretation: str = ''
#     for i in range(len(tokens)):
#         if tokens[i].type == 'PRINT' and tokens[i+1].type == 'STRING':
#             interpretation += f'print("{tokens[i+1].value}")\n'
#     return interpretation
        