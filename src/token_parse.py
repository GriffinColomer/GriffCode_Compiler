from lexical_parser import Token, Types
from typing import Self

# Program Node for parse Tree, will be used to identify key functions exit, return, print, etc...
class Node_Prog:
    def __init__(self, type = None, expr = None) -> None:
        self.expr = expr
        self.type = type
    
    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type
    
    def get_expression(self):
        return self.expr
    
    def set_expression(self, expr):
        self.expr = expr

# Main Leaf node to operators and numbers --add vaiable leaf soon
class Leaf:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def get_value(self):
        return self.token.value
    
    def get_type(self):
        return self.token.type

class Leaf_Factor(Leaf):
    def __init__(self, token: Token) -> None:
        super().__init__(token)

class Leaf_Operator(Leaf):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        
# Expression node used to represent what a program will use identified by waht is in between paratheses
# also used to do addition and subtraction
class Node_Expr:
    def __init__(self, left = None, right = None, operator = None) -> None:
        self.left: Self | Leaf = left
        self.right: Self | Leaf = right
        self.operator: Leaf = operator
    
    def get_left(self) -> Self | Leaf:
        return self.left

    def get_right(self) -> Self | Leaf:
        return self.right
        
    def get_operator(self) -> Leaf:
        return self.operator
        
    def set_right(self, right) -> None:
        self.right = right
    
    def set_left(self, left) -> None:
        self.left = left
    
    def set_operator(self, operator) -> None:
        self.operator = operator
        
# Term Node used to do mult and div operations
class Node_Term(Node_Expr):
    def __init__(self, left=None, right=None, operator=None) -> None:
        super().__init__(left, right, operator)
        
# Big Class used to parse the list of tokens and create the list of program trees
class Token_Parse:
    def __init__(self, tokens: list[Token]) -> None:
        self.types = Types()
        self.index = -1
        self.tokens = tokens
        self.current_token = None
        self.__advance()

# Increment the current token
    def __advance(self) -> None:
        self.index += 1
        if self.index == len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def __set_node(self, node: Node_Expr | Node_Term, new_node: Leaf):
        if not node.get_left():
            node.set_left(new_node)
        else:
            node.set_right(new_node)

    # Makes sure program has a type, and creates an initial expression for the program
    # Checks to make sure the program has parantheses and builds the tree recursively
    # Once closing parantheses are reached the program tree is complete
    def __parse_expr(self, head: Node_Prog) -> None:
        if not head.get_type():
            head.set_expression(Node_Expr())
            head.set_type(self.current_token.type)
        self.__advance()
        current_node: Node_Expr | Node_Term = head.get_expression()
        var_name: Token = None
        if self.current_token.type == self.types._VAR:
            var_name = self.current_token
            self.__advance()
        if self.current_token.type == self.types._OPARAN or self.current_token.type == self.types._EQUALS or self.current_token.type == self.types._VAR:
            self.__advance()
            if self.current_token and self.current_token.type == self.types._VAR:
                self.__set_node(current_node, Node_Expr(Leaf_Factor(self.current_token), operator = Leaf_Operator(var_name)))
                self.__advance()
            while self.current_token and self.current_token.type not in self.types.get_key_types():
                if self.current_token.type == self.types._INT:
                    self.__set_node(current_node, Node_Expr(Leaf_Factor(self.current_token), operator = Leaf_Operator(var_name)))
                    self.__advance()
                elif self.current_token.type == self.types._INT:
                    self.__set_node(current_node, Leaf_Factor(self.current_token))
                    self.__advance()
                elif self.current_token.type == self.types._OPARAN:
                    self.__set_node(current_node, Node_Expr())
                    self.__parse_expr(current_node.left())
                elif self.current_token.type == self.types._CPARAN:
                    break
                                

    # Is a driver function for the expression parsing function
    # Makes a list of program nodes for generator to work with
    def parse(self) -> list[Node_Prog]:
        programs = [] 
        while self.current_token:
            head = Node_Prog()
            current_node = head
            if(self.current_token.type in self.types.get_key_types()):
                self.__parse_expr(current_node)
                programs.append(head)
            else:
                self.__advance()
        return programs
    
