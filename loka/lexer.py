class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, language='fr'):
        self.language = language
        self.keywords = self._get_keywords()
    
    def _get_keywords(self):
        if self.language == 'fr':
            return {
                'si': 'IF',
                'sinon': 'ELSE',
                'tant_que': 'WHILE',
                'pour': 'FOR',
                'fonction': 'FUNCTION',
                'retourne': 'RETURN',
                'classe': 'CLASS',
                'importe': 'IMPORT'
            }
        else:  # English by default
            return {
                'if': 'IF',
                'else': 'ELSE',
                'while': 'WHILE',
                'for': 'FOR',
                'function': 'FUNCTION',
                'return': 'RETURN',
                'class': 'CLASS',
                'import': 'IMPORT'
            }
    
    def tokenize(self, code):
        tokens = []
        current = 0
        
        while current < len(code):
            char = code[current]
            
            # Ignore les espaces
            if char.isspace():
                current += 1
                continue
                
            # Identifiants et mots-clés
            if char.isalpha():
                value = ''
                while current < len(code) and (code[current].isalnum() or code[current] == '_'):
                    value += code[current]
                    current += 1
                    
                token_type = self.keywords.get(value, 'IDENTIFIER')
                tokens.append(Token(token_type, value))
                continue
            
            # Nombres
            if char.isdigit():
                value = ''
                while current < len(code) and (code[current].isdigit() or code[current] == '.'):
                    value += code[current]
                    current += 1
                tokens.append(Token('NUMBER', float(value)))
                continue
            
            current += 1
            
        return tokens
