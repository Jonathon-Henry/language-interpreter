from toks import *

Class Lexer(obj):
    def __init__(self, input):
        self.text = input
        self.index = 0




    def get_next_token(self):
        """Conditions for the lexer"""
        current_char = self.text[self.index]

        if current_char == ' ':

        if current_char == '+':
            return Token(PLUS, '+')

        if current_char == '-':
            return Token(PLUS, '+')

        if current_char == '*':
            return Token(PLUS, '+')

        if current_char == '/':
            return Token(PLUS, '+')

        if current_char == '%':
            return Token(PLUS, '+')

        if current_char == '==':
            return Token(PLUS, '+')

        if current_char == '<':
            return Token(PLUS, '+')

        if current_char == '>':
            return Token(PLUS, '+')

        if current_char == '<=' or current_char == '=<':
            return Token(PLUS, '+')

        if current_char == '>=' or current_char == '=>':
            return Token(PLUS, '+')

        if current_char == '(':
            return Token(PLUS, '+')

        if current_char == ')':
            return Token(PLUS, '+')



        self.index += 1

def main():


if __name__ == '__main__':
    main()
