# from cfonts import render, say
import os
import parser
import itertools

def getInput():

    for i in itertools.count():
        try:
            yield i, input("interpy> ")
        except KeyboardInterrupt:
            pass
        except EOFError:
            break

def exec_function(userIn):

    try:
        compile(userIn, '<stdin>', 'eval')
    except SyntaxError:
        return 
    return eval
    

def exec_input(i, userIn, user_globals):
    
    user_globals = user_globals.copy()

    try:
        result = exec_function(userIn)(userIn, user_globals)
    except Exception as e:
        print("Error: {0}".format(e))
    else:
        if result is not None:
            print(result)
    return user_globals

def selected_user_globals(user_globals):
    return ( 
        (key, user_globals[key])
        for key in sorted(user_globals)
        if not key.startswith('__') or not key.endswith('__')
    )

def write_globals(user_globals, path='user_globals.txt'):

    with open(path, 'w') as file:
        for key, val in selected_user_globals(user_globals):
            file.write('{0} = {1}'.format(key, val))

def main():

    user_globals = {}
    write_globals(user_globals)
    for i, userIn in getInput():
       user_globals = exec_input(i, userIn, user_globals)
       write_globals(user_globals)


if __name__ == '__main__':
    # output = render('Interpy', colors=['blue', 'red'], align='center')
    # print(output)
    main()
