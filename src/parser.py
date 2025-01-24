class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        """
        Parse le programme LOKA et construit l'AST
        """
        program = []
        while self.current < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                program.append(statement)
        return ASTNode('PROGRAM', children=program)
    
    def parse_statement(self):
        """
        Parse une instruction LOKA
        """
        token = self.current_token()
        
        if token.type == 'FUNCTION':
            return self.parse_function()
        elif token.type == 'CLASS':
            return self.parse_class()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'WHILE':
            return self.parse_while()
        
        return None
    
    def current_token(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
