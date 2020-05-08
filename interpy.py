# from cfonts import render
import sys
import itertools
import ply.yacc as yacc
import ply.lex as lex

keywords = ['IF', 'THEN', 'ELSE', 'LET', 'PRINT']
tokens = keywords + ['IDENTIFIER', 'NUMBER', 'PLUS', 'MINUS', 'TIMES',
          'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN',
          'ASSIGN', 'EQV', 'LT', 'GT', 'FLOAT' ,
          'SEMICOLON', 'MOD']

t_ignore = r" "
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_EQV = r"=="
t_EQUALS = r"\="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LT = r"\<"
t_GT = r"\>"
t_SEMICOLON = r"\;"
t_MOD = r"\%"

def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in keywords:
        t.type = t.value
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

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
               | assign'''
    print(run(p[1]))

def p_empty(p):
    '''empty : '''
    p[0] = None

def p_assign(p):
    '''assign : IDENTIFIER EQUALS expr'''
    p[0] = ('=', p[1], p[3])

def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr DIVIDE expr
            | expr TIMES expr
            | expr MOD expr
            | expr LT expr
            | expr GT expr
            | expr EQV expr'''
    p[0] = (p[2], p[1], p[3])

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_float(p):
    '''expr : FLOAT'''
    p[0] = p[1]

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = p[1]

def p_expr_print(p):
    '''expr : PRINT expr'''
    p[0] = p[2]

def p_expr_identifier(p):
    '''expr : IDENTIFIER'''
    p[0] = ('IDENTIFIER', p[1])


def p_error(p):
    sys.stderr.write('Syntax Error')

precedence = (
     ('left', 'LT', 'GT', 'EQV'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE', 'MOD'),
     ('left', 'LPAREN')
 )

env = {}

def run(p):
    print(p)
    global env
    if type(p) is tuple:
        if p[0] is '+':
            return run(p[1]) + run(p[2])
        elif p[0] is '-':
            return run(p[1]) - run(p[2])
        elif p[0] is '/':
            return run(p[1]) / run(p[2])
        elif p[0] is '*':
            return run(p[1]) * run(p[2])
        elif p[0] is '%':
            return run(p[1]) % run(p[2])
        elif p[0] is '<':
            return run(p[1]) < run(p[2])
        elif p[0] is '>':
            return run(p[1]) > run(p[2])
        elif p[0] is '==':
            return run(p[1]) is run(p[2])
        elif p[0] is '=':
            env[p[1]] = run(p[2])
            print(env)
        elif p[0] is 'IDENTIFIER':
            if p[1] not in env:
                return "Undeclared Variable Found!"
            return env[p[1]]

    else:
        return p
# Code to get all input/exec values

def getInput():
    for i in itertools.count():
        try:
            yield i, input("interpy> ")
        except KeyboardInterrupt:
            pass
        except EOFError:
            break


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
        if userIn == "--exit":
            exit(0)
        lexer.input(userIn)
        while True:
            tok = lexer.token()
            if not tok:
                break
            #print(tok)
        parser.parse(userIn)

if __name__ == '__main__':
    # output = render('Interpy', font='block', align='left', colors=['yellow', '#f80'])
    # print(output)
    print('\nWelcome to Interpy, the interpreter written in python. To find the syntax for Interpy, '
          'please refer to the grammar.txt file within the repository.\nThis was done by Alex Zoumaya and Jon Henry for'
          ' Dr. Phu Phung\'s CPS352.\n\n'
          '\t\t\t--exit\t\tterminate program\n\n')
    main()
