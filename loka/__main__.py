#!/usr/bin/env python3
"""
Point d'entrée principal pour LOKA
"""
import sys
import logging
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreteur

def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    if len(sys.argv) != 2:
        print("Usage: python -m loka <fichier.loka>")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
        
        logger.debug("Code source lu avec succès")
        
        # Analyse lexicale
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        logger.debug("Analyse lexicale terminée")
        
        # Analyse syntaxique
        parser = Parser()
        ast = parser.parse(tokens)
        logger.debug("Analyse syntaxique terminée")
        
        # Interprétation
        interpreteur = Interpreteur()
        logger.debug("Début de l'exécution")
        interpreteur.executer(ast)
        logger.debug("Exécution terminée")
        
    except FileNotFoundError:
        print(f"Erreur: Fichier '{sys.argv[1]}' non trouvé")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
