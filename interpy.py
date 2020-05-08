# from cfonts import render
import sys
import itertools
import ply.yacc as yacc
import ply.lex as lex

keywords = ['IF', 'THEN', 'ELSE', 'LET', 'PRINT', 'FXN', 'USING', 'IN']
tokens = keywords + ['IDENTIFIER', 'NUMBER', 'PLUS', 'MINUS', 'TIMES',
          'DIVIDE', 'EQUALS', 'LPAREN', 'RPAREN',
          'ASSIGN', 'EQV', 'LT', 'GT', 'FLOAT' ,
          'SEMICOLON', 'MOD', 'LBRACKET', 'RBRACKET', 'COMMA', 'STRING']

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
t_COMMA = r","
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_STRING = r"\"\w*\""

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
    '''assign : LET IDENTIFIER EQUALS expr'''
    p[0] = ('=', p[2], p[4])

def p_assign_function(p):
    '''assign : LET IDENTIFIER EQUALS FXN LPAREN listofidentifiers RPAREN LBRACKET expr RBRACKET SEMICOLON'''
    p[0] = ('FUNCTION', p[2], p[6], p[9])

def p_listofidentifiers(p):
    '''
    listofidentifiers : IDENTIFIER COMMA listofidentifiers
                      | IDENTIFIER
    '''
    if len(p) >= 3:
        p[0] = ('LOI', p[1], p[3])
    else:
        p[0] = p[1]

def p_listofexpr(p):
    '''
    listofexpr : expr SEMICOLON listofexpr
               | expr
    '''

    if len(p) >= 3:
        p[0] = ('LOE', p[1], p[3])
    else:
        p[0] = p[1]

def p_using(p):
    '''
    expr : USING listofexpr IN IDENTIFIER
    '''
    expressions = []
    #print(p[2])
    #print(functionHelper(p[2]))

    processedlist = functionHelper(p[2])
    if type(processedlist) is tuple: #Then passing only one expression to function, so just process the expression
        expressions = [run(processedlist)]
    else: #Otherwise, have to go through each expression and process it, and add to the list of expression values.
        for expression in functionHelper(p[2]): #evaluates the expressions given in the statement
            expressions += [run(expression)]
        #print(expression)
        #print(run(expression))

    p[0] = ('USING', expressions, p[4]) #Returns ('USING', values for function, function id)

def p_if_expression(p):
    '''
    expr : IF expr THEN expr ELSE expr
    '''
    p[0] = ('IF', p[2], p[4], p[6])

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

def p_expr_uminus(p):
    '''
    expr : MINUS expr %prec UMINUS
    '''
    p[0] = -p[2]

def p_expr_print(p):
    '''expr : PRINT STRING'''
    p[0] = ('PRINT', p[2])

def p_expr_identifier(p):
    '''expr : IDENTIFIER'''
    p[0] = ('IDENTIFIER', p[1])


def p_error(p):
    sys.stderr.write('Syntax Error')

precedence = (
     ('right', 'PRINT'),
     ('nonassoc', 'LT', 'GT', 'EQV'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE', 'MOD'),
     ('right', 'UMINUS'),
 )

env = {}

def run(p, env=env):
    #print(p)
    #global env
    if type(p) is tuple:
        if p[0] is '+':
            return run(p[1], env) + run(p[2], env)
        elif p[0] is '-':
            return run(p[1], env) - run(p[2], env)
        elif p[0] is '/':
            return run(p[1], env) / run(p[2], env)
        elif p[0] is '*':
            return run(p[1], env) * run(p[2],env)
        elif p[0] is '%':
            return run(p[1],env) % run(p[2],env)
        elif p[0] is '<':
            return run(p[1],env) < run(p[2],env)
        elif p[0] is '>':
            return run(p[1],env) > run(p[2],env)
        elif p[0] is '==':
            return run(p[1],env) is run(p[2],env)
        elif p[0] is '=':
            env[p[1]] = run(p[2],env)
            #print(env)
        elif p[0] is 'IDENTIFIER':
            if p[1] not in env:
                return "Undeclared Variable Found!"
            return env[p[1]]
        elif p[0] is 'IF':
            condition = p[1]
            t = p[2]
            e = p[3]

            if run(condition):
                return run(t)
            else:
                return run(e)
        elif p[0] is 'USING':
            if p[2] not in env or type(env[p[2]]) is not tuple or env[p[2]][0] != 'READYFUNCTION':
                 return "Function does not exist!"

            function = env[p[2]]
            if len(p[1]) != len(function[1]):
                return "Invalid number of identifiers given for function!"

            localenv = {}
            listofvalues = p[1]
            listofidentifiers = function[1]
            for i in range(len(listofvalues)):
                localenv[listofidentifiers[i]] = listofvalues[i]

            return run(function[2], localenv)

        elif p[0] is 'FUNCTION':
            list = p[2]
            expression = p[3]

            list = functionHelper(list, id='LOI')

            #"creates" a function with identifiers and the function's expression and binds it in the dictionary
            env[p[1]] = ('READYFUNCTION', list, expression)


    else:
        return p
# Code to get all input/exec values

#Helps parse data in list of expression or list of identifiers
def functionHelper(list, id='LOE'):
    if len(list) != 1 and list[0] == id:
        newlist = []
        while list[0] == id:
            newlist = newlist + [list[1]]
            list = list[2]
            if list[0] != id:
                newlist = newlist + [list]
        list = newlist
    return list



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
