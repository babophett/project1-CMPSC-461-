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
       
        while self.position < len(self.code) and (self.code[self.position].isspace() or self.code[self.position] == "\n"):
            self.position += 1
        if self.position >= len(self.code):
                return 'END', None
        if self.code[self.position].isalpha():  # handles keywords or variables
            start = self.position
            while self.position < len(self.code) and (self.code[self.position].isalnum()):
                self.position += 1
            token = self.code[start:self.position]
            if token in self.keywords:
                return token.upper(), token
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
                return 'EQUAL', equal
            start = self.position
            self.position += 1
            return 'MATH', self.code[start:self.position]
        


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

    def parse(self):
        self.program()

    # move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()

    # parse the one or multiple statements
    def program(self):
        self.advance()
        while self.current_token is not None:

            self.statement()

    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token[0] == "IF":
            self.if_statement()
        elif self.current_token[0] == "WHILE":
            self.while_loop()
        elif self.current_token[0] == "VAR":
            self.assignment()
        

    # parse assignment statements
    def assignment(self):
        var = self.current_token[1]
        self.advance()
        equal = self.current_token[1]
        arithmetic_expression = self.arithmetic_expression()
        
        return f"('{equal}', '{var}', '{arithmetic_expression}')"
    # parse arithmetic experssions
    def arithmetic_expression(self):
        term1 = self.term()  # Parse the first term
        while self.current_token is not None and self.current_token[0] == "MATH":
            operator = self.current_token[1]  # Get the operator
            self.advance()  # Move past the operator
            term2 = self.term()  # Parse the next term
            # Handle the operator here, for example:
            if operator == '+':
                expr = f"('{operator}', '{term1}', '{term2}')"
            elif operator == '-':
                expr = f"('{operator}', '{term1}', '{term2}')"
        print(expr)
        return expr

    def term(self):
        factor1 = self.factor()  # Parse the first factor
        while self.current_token is not None and self.current_token[0] == "MATH":
            operator = self.current_token[1]  # Get the operator
            self.advance()  # Move past the operator
            factor2 = self.factor()  # Parse the next factor
            # Handle the operator here, for example:
            if operator == '*':
                expr = f"('{operator}', '{factor1}', '{factor2}')"
            elif operator == '/':
                expr = f"('{operator}', '{factor1}', '{factor2}')"
        print(expr)
        return expr
    def factor(self):
        if self.current_token[0] == "VAR":
            return self.current_token[1]
        if self.current_token[0] == "NUM":
            return self.current_token[1]
        else:
            # Call arithmetic_expression and then advance token
            arithmetic_expr = self.arithmetic_expression()
            self.advance()
            return arithmetic_expr

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
code = '''
    x = 5 + 3
    '''
lexer = Lexer(code)
    
parser = Parser(lexer)
ast = parser.parse()
print(ast)