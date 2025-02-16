"""
Interface en ligne de commande pour LOKA
"""
import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreteur

def main():
    """Point d'entrée principal de LOKA"""
    if len(sys.argv) < 2:
        print("Usage: loka <fichier.loka>")
        sys.exit(1)
        
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        # Analyse lexicale
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        
        # Analyse syntaxique
        parser = Parser()
        ast = parser.parse(tokens)
        
        # Interprétation
        interpreteur = Interpreteur()
        interpreteur.interpreter(ast)
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' n'existe pas.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Erreur de syntaxe : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
