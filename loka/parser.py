"""
Analyseur syntaxique pour le langage LOKA
"""
from .lexer import TokenType

class ASTNode:
    pass

class Programme(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations

class Fonction(ASTNode):
    def __init__(self, nom, parametres, corps):
        self.nom = nom
        self.parametres = parametres
        self.corps = corps

class AppelFonction(ASTNode):
    def __init__(self, nom, arguments):
        self.nom = nom
        self.arguments = arguments

class AppelMethode(ASTNode):
    def __init__(self, objet, methode, arguments):
        self.objet = objet
        self.methode = methode
        self.arguments = arguments

class Affectation(ASTNode):
    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur

class BlocCode(ASTNode):
    def __init__(self, instructions):
        self.instructions = instructions

class Expression(ASTNode):
    pass

class Nombre(Expression):
    def __init__(self, valeur):
        self.valeur = valeur

class Chaine(Expression):
    def __init__(self, valeur):
        self.valeur = valeur

class Identifiant(Expression):
    def __init__(self, nom):
        self.nom = nom

class Liste(Expression):
    def __init__(self, elements):
        self.elements = elements

class OperationBinaire(Expression):
    def __init__(self, gauche, operateur, droite):
        self.gauche = gauche
        self.operateur = operateur
        self.droite = droite

class Parser:
    def __init__(self):
        self.tokens = []
        self.position = 0
        self.current_token = None
    
    def init_parser(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message):
        if self.current_token:
            raise SyntaxError(f"{message} à la ligne {self.current_token.ligne}, colonne {self.current_token.colonne}")
        else:
            raise SyntaxError(message)
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            self.error(f"Token attendu : {token_type}, reçu : {self.current_token.type if self.current_token else 'None'}")
    
    def parse(self, tokens):
        self.init_parser(tokens)
        return self.programme()
    
    def programme(self):
        declarations = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.current_token.type in (TokenType.FONCTION, TokenType.FUNCTION):
                declarations.append(self.declaration_fonction())
            else:
                self.error("Déclaration de fonction attendue")
        
        return Programme(declarations)
    
    def declaration_fonction(self):
        self.eat(TokenType.FONCTION)  # ou FUNCTION
        nom = self.eat(TokenType.IDENTIFIANT).valeur
        
        self.eat(TokenType.PARENTHESE_GAUCHE)
        parametres = []
        
        if self.current_token.type != TokenType.PARENTHESE_DROITE:
            parametres.append(self.eat(TokenType.IDENTIFIANT).valeur)
            while self.current_token.type == TokenType.VIRGULE:
                self.eat(TokenType.VIRGULE)
                parametres.append(self.eat(TokenType.IDENTIFIANT).valeur)
        
        self.eat(TokenType.PARENTHESE_DROITE)
        corps = self.bloc_code()
        
        return Fonction(nom, parametres, corps)
    
    def bloc_code(self):
        self.eat(TokenType.ACCOLADE_GAUCHE)
        instructions = []
        
        while self.current_token and self.current_token.type != TokenType.ACCOLADE_DROITE:
            if self.current_token.type in (TokenType.AFFICHE, TokenType.PRINT):
                instructions.append(self.instruction_affichage())
            elif self.current_token.type == TokenType.IDENTIFIANT:
                token = self.eat(TokenType.IDENTIFIANT)
                if self.current_token.type == TokenType.EGAL:
                    # Affectation
                    self.position -= 1  # Reculer pour relire l'identifiant
                    self.current_token = self.tokens[self.position]
                    instructions.append(self.instruction_affectation())
                elif self.current_token.type == TokenType.POINT:
                    # Appel de méthode
                    instructions.append(self.appel_methode(Identifiant(token.valeur)))
                elif self.current_token.type == TokenType.PARENTHESE_GAUCHE:
                    # Appel de fonction
                    instructions.append(self.appel_fonction(token.valeur))
                else:
                    self.error("Instruction non reconnue")
            else:
                self.error("Instruction non reconnue")
    
        self.eat(TokenType.ACCOLADE_DROITE)
        return BlocCode(instructions)
    
    def instruction_affichage(self):
        self.eat(TokenType.AFFICHE)  # ou PRINT
        self.eat(TokenType.PARENTHESE_GAUCHE)
        expr = self.expression()
        self.eat(TokenType.PARENTHESE_DROITE)
        return AppelFonction("affiche", [expr])
    
    def instruction_affectation(self):
        nom = self.eat(TokenType.IDENTIFIANT).valeur
        self.eat(TokenType.EGAL)
        valeur = self.expression()
        return Affectation(nom, valeur)
    
    def expression(self):
        """Analyse une expression"""
        gauche = self.terme()
        
        while self.current_token and self.current_token.type in [
            TokenType.PLUS, TokenType.MOINS,
            TokenType.PLUS_EGAL, TokenType.MOINS_EGAL
        ]:
            operateur = self.current_token
            self.advance()
            droite = self.terme()
            gauche = OperationBinaire(gauche, operateur, droite)
        
        return gauche
    
    def terme(self):
        """Analyse un terme (multiplication/division)"""
        gauche = self.facteur()
        
        while self.current_token and self.current_token.type in [
            TokenType.MULTIPLIE, TokenType.DIVISE
        ]:
            operateur = self.current_token
            self.advance()
            droite = self.facteur()
            gauche = OperationBinaire(gauche, operateur, droite)
        
        return gauche
    
    def facteur(self):
        """Analyse un facteur (nombre, identifiant, etc.)"""
        token = self.current_token
        
        if token.type == TokenType.NOMBRE:
            self.advance()
            return Nombre(float(token.valeur))
        
        elif token.type == TokenType.IDENTIFIANT:
            self.advance()
            # Vérifier si c'est un appel de fonction
            if self.current_token and self.current_token.type == TokenType.PARENTHESE_GAUCHE:
                return self.appel_fonction(token.valeur)
            return Identifiant(token.valeur)
        
        elif token.type == TokenType.PARENTHESE_GAUCHE:
            self.advance()
            expr = self.expression()
            self.eat(TokenType.PARENTHESE_DROITE)
            return expr
        
        elif token.type == TokenType.CHAINE:
            self.advance()
            return Chaine(token.valeur)
        
        self.error(f"Token inattendu: {token.type}")
    
    def appel_fonction(self, nom):
        self.eat(TokenType.PARENTHESE_GAUCHE)
        arguments = []
        
        if self.current_token.type != TokenType.PARENTHESE_DROITE:
            arguments.append(self.expression())
            while self.current_token.type == TokenType.VIRGULE:
                self.eat(TokenType.VIRGULE)
                arguments.append(self.expression())
        
        self.eat(TokenType.PARENTHESE_DROITE)
        return AppelFonction(nom, arguments)
    
    def appel_methode(self, objet):
        self.eat(TokenType.POINT)
        methode = self.eat(TokenType.IDENTIFIANT).valeur
        
        self.eat(TokenType.PARENTHESE_GAUCHE)
        arguments = []
        
        if self.current_token.type != TokenType.PARENTHESE_DROITE:
            arguments.append(self.expression())
            while self.current_token.type == TokenType.VIRGULE:
                self.eat(TokenType.VIRGULE)
                arguments.append(self.expression())
        
        self.eat(TokenType.PARENTHESE_DROITE)
        return AppelMethode(objet, methode, arguments)
    
    def liste(self):
        self.eat(TokenType.CROCHET_GAUCHE)
        elements = []
        
        if self.current_token.type != TokenType.CROCHET_DROIT:
            elements.append(self.expression())
            while self.current_token.type == TokenType.VIRGULE:
                self.eat(TokenType.VIRGULE)
                elements.append(self.expression())
        
        self.eat(TokenType.CROCHET_DROIT)
        return Liste(elements)
