# Tokens

INTEGER, FRACTION = 'INTEGER', 'FRACTION'
IDENTIFIER = 'IDENTIFIER'
PLUS, MINUS, DIV, MUL, MOD = 'PLUS', 'MINUS', 'DIV', 'MUL', 'MOD'
LPAREN RPAREN ASSIGN PRINT = 'LPAREN', 'RPAREN', 'ASSIGN', 'PRINT'
EQV, LT, GT, LTE, GTE = 'EQV', 'LT', 'GT', 'LTE', 'GTE'
SEMICOLON = 'SEMICOLON'
EOF = 'EOF'

Class Token(obj):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Tok({type}, {value})'.format(
            type=self.type, value=self.value
        )

    def __repr__(self):
        return self.__str__()


def main():

if __name__ == '__main__':
    main()
