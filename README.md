# interPY
The interpreter written in Python by Jon Henry and Alex Zoumaya

To run:

$python3 interpy.py

May need to pip install PLY

Alex Zoumaya | Jon Henry

## Part 1: The language

  One of the best things about python is the readability and how close it is to english. We wanted to find a way to keep our language as close to english as possible, with a few minor tweaks. All basic operators remain the same, which include +,-, /, *, and %. Order of operations is maintained even if the operations are printed all on one line. Types are inferred, 1 will be treated as an int, while 1.1 is treated as a float without explicitly stating so. All keywords in InterPY must be capitalized to invoke them. So when declaring a variable it must read as LET x =10, so the interpreter can read it in as a variable declaration, this is the same for IF THEN ELSE statements, and declaring FXNs. We also implemented a COMPARE function, which takes in 3 ints/floats and returns the MIN and MAX values. Our structure for users building functions are LET <identifier> =  FXN( <parameters> ) [ <function body> ]; The parameters may be declared after the fxn is declared. To invoke the function, you must declare which variables you are using by stating USING <param> IN <identifier for function>. PRINT is also a viable portion of our language, that can print out a single word or variable. 

![image](https://user-images.githubusercontent.com/67361112/118328970-72fa3a00-b4d4-11eb-8669-4c21f707e734.png)

Example: 

![image](https://user-images.githubusercontent.com/67361112/118329095-9fae5180-b4d4-11eb-8db5-df78e0341a98.png)



## Part 2: Implementation

Since we wrote our interpreter in python, we looked for a library that could assist us in building our language. Luckily we found a library called PLY, PLY stands for Python Lex Yacc. So in order to build our language, all we had to do was follow the same rules to build the interpreter as we did earlier in the semester with our Lexx Yacc project in C. Of course, with modifications we built so that it was more true to our language. We first defined all tokens, reserved keys, and any regular expressions for our tokens. Then, we defined the parser rules and how it would interpret the language passed by the lexer. We did this by using Python’s tuples and a recursive algorithm to break down each statement until we got to one specific answer. To establish variables, we created an environment dictionary that is called with every recursive call so that in case a variable is being used, the interpreter runs it as if there is just a value there and not a variable. To circumvent issues with functions and their local environments, we created environments specific to the functions so that the local values will not be altered and can live within the function. Interpy is able to define variables, use them over and over, while still maintaining integrity. The user interface is simply a for loop that continuously yields values from the user, but waits until the functions are done until it asks again. 


## Part 3: Evaluation
Simple math, order of operations, variable declaration and use, function declaration and use, print usage
 
![image](https://user-images.githubusercontent.com/67361112/118329250-be144d00-b4d4-11eb-8018-c23799a759ba.png)

Syntax errors, on print, undeclared variables, improper capitalization, and incomplete or wrong statements
 
![image](https://user-images.githubusercontent.com/67361112/118329275-c40a2e00-b4d4-11eb-950d-a64ecb469cda.png)

