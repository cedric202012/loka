"""
Analyseur lexical pour le langage LOKA
"""
from enum import Enum, auto

class TokenType(Enum):
    # Mots-clés
    FONCTION = auto()
    FUNCTION = auto()  # Version anglaise
    CLASSE = auto()
    CLASS = auto()     # Version anglaise
    SI = auto()
    IF = auto()        # Version anglaise
    SINON = auto()
    ELSE = auto()      # Version anglaise
    POUR = auto()
    FOR = auto()       # Version anglaise
    TANT_QUE = auto()
    WHILE = auto()     # Version anglaise
    RETOURNE = auto()
    RETURN = auto()    # Version anglaise
    AFFICHE = auto()
    PRINT = auto()     # Version anglaise
    
    # Symboles
    PARENTHESE_GAUCHE = auto()
    PARENTHESE_DROITE = auto()
    ACCOLADE_GAUCHE = auto()
    ACCOLADE_DROITE = auto()
    CROCHET_GAUCHE = auto()
    CROCHET_DROIT = auto()
    VIRGULE = auto()
    POINT = auto()
    PLUS = auto()
    MOINS = auto()
    MULTIPLIE = auto()
    DIVISE = auto()
    EGAL = auto()
    PLUS_EGAL = auto()
    MOINS_EGAL = auto()
    GUILLEMET = auto()
    
    # Types de base
    NOMBRE = auto()
    CHAINE = auto()
    IDENTIFIANT = auto()
    
    # Fin de fichier
    EOF = auto()

class Token:
    def __init__(self, type, valeur, ligne, colonne):
        self.type = type
        self.valeur = valeur
        self.ligne = ligne
        self.colonne = colonne
    
    def __str__(self):
        return f"Token({self.type}, '{self.valeur}', ligne={self.ligne}, col={self.colonne})"

class Lexer:
    def __init__(self):
        self.code = ""
        self.position = 0
        self.ligne = 1
        self.colonne = 1
        self.current_char = None
        
        # Mots-clés
        self.keywords = {
            'fonction': TokenType.FONCTION,
            'function': TokenType.FUNCTION,
            'classe': TokenType.CLASSE,
            'class': TokenType.CLASS,
            'si': TokenType.SI,
            'if': TokenType.IF,
            'sinon': TokenType.SINON,
            'else': TokenType.ELSE,
            'pour': TokenType.POUR,
            'for': TokenType.FOR,
            'tant_que': TokenType.TANT_QUE,
            'while': TokenType.WHILE,
            'retourne': TokenType.RETOURNE,
            'return': TokenType.RETURN,
            'affiche': TokenType.AFFICHE,
            'print': TokenType.PRINT
        }
    
    def init_code(self, code):
        self.code = code
        self.position = 0
        self.ligne = 1
        self.colonne = 1
        self.current_char = self.code[0] if code else None
    
    def advance(self):
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None
        else:
            if self.current_char == '\n':
                self.ligne += 1
                self.colonne = 1
            else:
                self.colonne += 1
            self.current_char = self.code[self.position]
    
    def peek(self):
        if self.position + 1 >= len(self.code):
            return None
        return self.code[self.position + 1]
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()
    
    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = self.keywords.get(result, TokenType.IDENTIFIANT)
        return Token(token_type, result, self.ligne, self.colonne)
    
    def get_number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NOMBRE, float(result), self.ligne, self.colonne)
    
    def get_string(self):
        self.advance()  # Skip initial quote
        result = ''
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip closing quote
        return Token(TokenType.CHAINE, result, self.ligne, self.colonne)
    
    def get_next_token(self):
        while self.current_char:
            # Espaces
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Commentaires
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Identifiants et mots-clés
            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()
            
            # Nombres
            if self.current_char.isdigit():
                return self.get_number()
            
            # Chaînes
            if self.current_char == '"':
                return self.get_string()
            
            # Symboles simples
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.PARENTHESE_GAUCHE, '(', self.ligne, self.colonne - 1)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.PARENTHESE_DROITE, ')', self.ligne, self.colonne - 1)
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.ACCOLADE_GAUCHE, '{', self.ligne, self.colonne - 1)
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.ACCOLADE_DROITE, '}', self.ligne, self.colonne - 1)
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.CROCHET_GAUCHE, '[', self.ligne, self.colonne - 1)
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.CROCHET_DROIT, ']', self.ligne, self.colonne - 1)
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.VIRGULE, ',', self.ligne, self.colonne - 1)
            if self.current_char == '.':
                self.advance()
                return Token(TokenType.POINT, '.', self.ligne, self.colonne - 1)
            if self.current_char == '+':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.PLUS_EGAL, "+=", self.ligne, self.colonne - 2)
                self.advance()
                return Token(TokenType.PLUS, "+", self.ligne, self.colonne - 1)
            if self.current_char == '-':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.MOINS_EGAL, "-=", self.ligne, self.colonne - 2)
                self.advance()
                return Token(TokenType.MOINS, "-", self.ligne, self.colonne - 1)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLIE, "*", self.ligne, self.colonne - 1)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVISE, "/", self.ligne, self.colonne - 1)
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EGAL, "=", self.ligne, self.colonne - 1)
            
            raise SyntaxError(f"Caractère inattendu '{self.current_char}' à la ligne {self.ligne}, colonne {self.colonne}")
        
        return Token(TokenType.EOF, None, self.ligne, self.colonne)
    
    def tokenize(self, code):
        self.init_code(code)
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
