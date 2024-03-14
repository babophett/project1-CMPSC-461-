# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.keywords = ['if', 'then', 'else', 'while', 'do']
        self.arithmetic = ['+' , '-', '*','/','=', '(', ')']
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
            operator = self.code[self.position]
            if operator == '=':
                equal = operator
                self.position += 1
                return 'EQUAL', equal
            start = self.position
            self.position += 1
            if operator == "*" or  operator == "/":
                return 'MULTIDIV', operator
            elif operator == "+" or  operator == "-": 
                return 'ADDSUB', operator
            elif operator == "(":
                return 'LP', operator
            elif operator == ")":
                return 'RP', operator



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
        return self.program()

    # move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()

    # parse the one or multiple statements
    def program(self):
        self.advance()
        tree = []
        while self.current_token[1] is not None:
            
            tree.append(self.statement())
        return ''.join(tree)

    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token[0] == 'IF':
            return self.if_statement()
        elif self.current_token[0] == 'WHILE':
            return self.while_loop()
        elif self.current_token[0] == 'VAR':
            return self.assignment()
            
        

    # parse assignment statements
    def assignment(self):
        var = self.current_token[1]
        self.advance()
        equal = self.current_token[1]
        self.advance()
        arithmetic_expression = self.arithmetic_expression()
        return f"('{equal}', '{var}', {arithmetic_expression})"
    # parse arithmetic experssions
    def arithmetic_expression(self):
        term1 = self.term()  # Parse the first term
        while self.current_token[0] != "END" and self.current_token[0] == "ADDSUB":
            operator = self.current_token[1]  # Get the operator
            self.advance()  # Move past the operator
            term2 = self.term()  # Parse the next term
            # Handle the operator here, for example:
            term1 = f"('{operator}', {term1}, {term2})"
        if self.current_token[0] == 'RP':
            self.advance()
        return term1

    def term(self):
        factor1 = self.factor()  # Parse the first factor
        while self.current_token[0] != "END" and self.current_token[0] == "MULTIDIV":
            operator = self.current_token[1]  # Get the operator
            self.advance()  # Move past the operator
            factor2 = self.factor()  # Parse the next factor
            # Handle the operator here, for example:
            factor1 = f"('{operator}', {factor1}, {factor2})"
        return factor1
    def factor(self):
        if self.current_token[0] == "VAR":
            temp = self.current_token[1]
            self.advance()
            return f"'{temp}'"
        if self.current_token[0] == "NUM":
            temp = self.current_token[1]
            self.advance()
            return temp
        else:
            self.advance()
            return f"{self.arithmetic_expression()}"
    
        

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        self.advance()
        condition = self.condition()
        self.advance()
        statement = self.statement()
        if self.current_token[0] == 'ELSE':
            self.advance()
            elseStatement = self.statement()
            return f"('if', {condition}, {statement}, {elseStatement})"
        return f"('if', {condition}, {statement})"
    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        self.advance()
        condition = self.condition()
        self.advance()
        statement = [self.statement()]
        statement = f'{statement}'
        statement = statement.replace('"', '')

        return f"('while', {condition}, {statement})"


    def condition(self):
        leftExpr = self.arithmetic_expression()
        comparative_operator = f"'{self.current_token[1]}'"
        self.advance()
        rightExpr = self.arithmetic_expression()
        return f"({comparative_operator}, {leftExpr}, {rightExpr})"
