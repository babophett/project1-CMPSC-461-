# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.keywords = ['if', 'then', 'else', 'while', 'do']
        self.arithmetic = ['+' , '-', '*','/','=']
        self.operators = ['==' , '!=' , '<' , '>' , '<=' , '>=']
    # move the lexer position and identify next possible tokens.
    def get_token(self):
        if self.position >= len(self.code):
            return None

        if self.position < len(self.code) and (self.code[self.position].isspace() or self.code[self.position] == "\n"):
            self.position += 1
            return None, ""

        if self.code[self.position].isalpha():  # handles keywords or variables
            start = self.position
            while self.position < len(self.code) and (self.code[self.position].isalnum()):
                self.position += 1
            token = self.code[start:self.position]
            if token in self.keywords:
                return 'KEYWORD', token
            else:
                return 'VAR', token

        elif self.code[self.position].isdigit():  # handles numbers
            start = self.position
            while self.position < len(self.code) and (self.code[self.position].isdigit()):
                self.position += 1
            number = self.code[start:self.position]
            return 'NUM', number

        elif self.code[self.position] in self.operators:  # handles comparative operators
            start = self.position
            if self.position + 1 < len(self.code) and self.code[self.position:self.position + 2] in self.operators:
                self.position += 2
                return 'OP', self.code[start:self.position]
            self.position += 1
            return 'OP', self.code[start:self.position]

        elif self.code[self.position] in self.arithmetic:  # handles arithmetic operators
            if self.code[self.position] == '=':
                equal = self.code[self.position]
                self.position += 1
                return 'EXPR', equal
            start = self.position
            self.position += 1
            return 'MATH', self.code[start:self.position]
        
        return None
        
code = '''a = x + y + z'''
code = '''
    x = 1
    y = 2
    z = 3
    a = x + y + z
    '''

lexer = Lexer(code)
res = []
while lexer.position < len(lexer.code):
    res.append(lexer.get_token())

for token in res:
    print(token)
 
        


# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    # function to parse the entire program
    def parse(self):
        pass
    # move to the next token.
    def advance(self):
        pass
    # parse the one or multiple statements
    def program(self):
        pass
        
    # parse if, while, assignment statement.
    def statement(self):
        pass

    # parse assignment statements
    def assignment(self):
        pass

    # parse arithmetic experssions
    def arithmetic_expression(self):
        pass
   
    def term(self):
        pass

    def factor(self):
        pass

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        pass
    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        pass

    def condition(self):
        pass
