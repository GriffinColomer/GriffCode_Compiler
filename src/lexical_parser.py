from lib.type import Types
# Error Handling
class Position:
    def __init__(self, idx: int, ln: int, col: int) -> None:
        self.idx = idx
        self.ln = ln
        self.col = col
    
    def advance(self, current_char: str | None) -> None:
        self.idx += 1
        self.col += 1
        
        if current_char == '\n':
            self.col = 1
            self.ln += 1
    
    def copy(self) -> any:
        return Position(self.idx, self.ln, self.col)
    
    def __repr__(self) -> str:
        return f'line: {self.ln} Column: {self.col}'

class Error:
    def __init__(self, error_name: str, error_details: str, position: Position) -> None:
        self.error_name = error_name
        self.error_details = error_details
        self.position = position
        
    def __repr__(self) -> str:
        return f'{self.error_name}: {self.error_details} at {self.position}'

class IllegalCharError(Error):
    def __init__(self, error_details: str, position: Position) -> None:
        super().__init__('Illegal Character', error_details, position)

# Input Handling
class Token:
    def __init__(self, type_: str, value: int | float | str = None) -> None:
          self.type = type_
          self.value = value
    
    def __str__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexar:
    def __init__(self, text: str):
        self.text = text
        self.pos = Position(-1, 1, 0)
        self.character = None
        self.types = Types()
        self.advance()
    
    def advance(self) -> None:
        self.pos.advance(self.character)
        self.character = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def __make_number(self) -> Token:
        num: str = ''
        dots = 0
        while self.character and self.character in self.types.DIGITS + '.':
            if self.character == '.':
                if dots == 1:
                    break
                dots += 1
            num += self.character
            self.advance()
        if dots != 0:
            return Token(self.types._FLOAT, float(num))
        return Token(self.types._INT, int(num))
    
    def __make_key_word(self) -> Token:
        word: str = ''
        while self.character and self.character.isalnum():
            word += self.character
            self.advance()
        if self.types._KEY_MAP[word]:
            return Token(self.types._KEY_MAP[word])
        return Token(self.types._VAR, word)
        
    def __make_string(self) -> Token:
        string = ''
        self.advance()
        while self.character not in '"\'':
            string += self.character
            self.advance()
        self.advance()
        return Token(self.types._STR, string)
    
    def make_tokens(self) -> tuple[list[Token], None | Error]:
        tokens: list[Token] = []
        while self.character != None:
            if self.character in ' \t':
                self.advance()
            elif self.character in '>()':
                tokens.append(Token(self.types._MAP[self.character]))
                self.advance()
            elif self.character in self.types._OPERATORS.keys():
                tokens.append(Token(self.types._OPERATORS[self.character]))
            elif self.character in '"\'':
                tokens.append(self.__make_string())
            elif self.character in self.types.DIGITS:
                tokens.append(self.__make_number())
            elif self.character.isalpha():
                tokens.append(self.__make_key_word())
        
            else:
                return [], IllegalCharError(f'\'{self.character}\'', self.pos)
        return tokens, None
    
def parseText(text):
    lexar = Lexar(text)
    tokens, error = lexar.make_tokens()
    return tokens, error