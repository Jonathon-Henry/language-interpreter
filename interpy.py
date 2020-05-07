# from cfonts import render
import sys
import itertools
import ply.yacc as yacc
import ply.lex as lex

tokens = ['IDENTIFIER', 'NUMBER', 'PLUS', 'MINUS', 'TIMES',
          'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN', 'PRINT',
          'ASSIGN', 'EQV', 'LT', 'GT', 'LTE', 'GTE',
          'SEMICOLON', 'MOD']

t_ignore = r" "
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_EQUALS = r"\="
t_IDENTIFIER = r"[a-zA-Z]+[0-9]*"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_PRINT = r"print"
t_EQV = r"=="
t_LT = r"\<"
t_GT = r"\>"
t_LTE = r"<="
t_GTE = r">="
t_SEMICOLON = r"\;"
t_MOD = r"\%"

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal token: {0}".format(t))
    t.lexer.skip(1)

def p_program(p):
    '''program : expr
               | empty
               | NUMBER'''
    print(p[1])

def p_empty(p):
    '''empty : '''
    p[0] = None

def p_assign(p):
    '''assign : IDENTIFIER EQUALS expr'''
    p[0] = p[1]

def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr DIVIDE expr
            | expr TIMES expr
            | expr MOD expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = p[1]

def p_error(p):
    sys.stderr.write('Syntax Error')

precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
 )

# Code to get all input/exec values

def getInput():
    for i in itertools.count():
        try:
            yield i, input("interpy> ")
        except KeyboardInterrupt:
            pass
        except EOFError:
            break

def exec_function(userIn):

    if compare(userIn)[0]:
        return "Min value: {0}, Max value: {1}".format(compare(userIn)[1], compare(userIn)[2])
    try:
        compile(userIn, '<stdin>', 'eval')
    except SyntaxError:
        return exec
    return eval

def exec_input(i, userIn):
    try:
        result = exec_function(userIn)(userIn)
    except Exception as e:
        print("Error: {0}".format(e))
    else:
        if result is not None:
            print(result)
    return None

def compare(input):
    min = input[0]
    max = input[-1]
    try:
        for x in range(len(input)):
            if min > input[x]:
                min = input[x]
            if max > input[x]:
                max = input[x]
        return True, min, max
    except:
        return False, 0, 0

def main():
    parser = yacc.yacc()
    lexer = lex.lex()

    for i, userIn in getInput():
        # user_globals = exec_input(i, userIn)
        lexer.input(userIn)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
        parser.parse(userIn)
        pass

if __name__ == '__main__':
    # output = render('Interpy', font='block', align='left', colors=['yellow', '#f80'])
    # print(output)
    print('\nWelcome to Interpy, the interpreter written in python. To find the syntax for Interpy, '
          'please refer to the grammar.txt file within the repository.\nThis was done by Alex Zoumaya and Jon Henry for'
          ' Dr. Phu Phung\'s CPS352.\n\n'
          '\t\t\t--help\t\tmenu\n\t\t\t--exit\t\tterminate program\n\n')
    main()
