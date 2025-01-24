"""
Interpréteur pour le langage LOKA
"""
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .lexer import TokenType
from .parser import (
    Programme, Fonction, AppelFonction, AppelMethode,
    Affectation, BlocCode, Nombre, 
    Chaine, Identifiant, OperationBinaire,
    Liste
)
from .matrice import Matrice

class Environnement:
    def __init__(self, parent=None):
        self.variables = {}
        self.fonctions = {}
        self.parent = parent
    
    def definir_variable(self, nom, valeur):
        self.variables[nom] = valeur
    
    def obtenir_variable(self, nom):
        if nom in self.variables:
            return self.variables[nom]
        elif self.parent:
            return self.parent.obtenir_variable(nom)
        else:
            raise NameError(f"Variable non définie : {nom}")
    
    def definir_fonction(self, nom, fonction):
        self.fonctions[nom] = fonction
    
    def obtenir_fonction(self, nom):
        if nom in self.fonctions:
            return self.fonctions[nom]
        elif self.parent:
            return self.parent.obtenir_fonction(nom)
        else:
            raise NameError(f"Fonction non définie : {nom}")

class Interpreteur:
    def __init__(self):
        logger.info("Initialisation de l'interpréteur")
        self.env_global = Environnement()
        self.definir_fonctions_natives()
    
    def definir_fonctions_natives(self):
        logger.debug("Définition des fonctions natives")
        def affiche(*args):
            logger.debug(f"Fonction native affiche() appelée avec: {args}")
            print(*args)
        
        def str_loka(x):
            logger.debug(f"Fonction native str() appelée avec: {x}")
            return str(x)
        
        def matrice(donnees):
            return Matrice.creer(donnees)
        
        self.env_global.definir_fonction("affiche", affiche)
        self.env_global.definir_fonction("print", affiche)
        self.env_global.definir_fonction("str", str_loka)
        self.env_global.definir_fonction("matrice", matrice)
    
    def executer(self, arbre):
        logger.info("Début de l'exécution")
        env = Environnement(self.env_global)
        
        # Exécuter le programme
        self.visiter(arbre, env)
        
        # Appeler la fonction main si elle existe
        if env.obtenir_fonction("main"):
            logger.debug("Appel de la fonction main()")
            self.visiter_AppelFonction(AppelFonction("main", []), env)
        else:
            logger.warning("Pas de fonction main() trouvée")
    
    def interpreter(self, ast):
        return self.visiter(ast, self.env_global)
    
    def visiter(self, node, env):
        # Dispatch vers la méthode appropriée selon le type de nœud
        method_name = f'visiter_{node.__class__.__name__}'
        method = getattr(self, method_name, None)
        if method:
            return method(node, env)
        else:
            raise NotImplementedError(f"Pas de méthode pour visiter {node.__class__.__name__}")
    
    def visiter_Programme(self, node, env):
        logger.debug("Visite du programme principal")
        resultats = []
        for declaration in node.declarations:
            resultat = self.visiter(declaration, env)
            resultats.append(resultat)
        return resultats
    
    def visiter_Fonction(self, node, env):
        logger.debug(f"Définition de la fonction: {node.nom}")
        def fonction_wrapper(*args):
            nouvel_env = Environnement(env)
            for param, arg in zip(node.parametres, args):
                nouvel_env.definir_variable(param, arg)
            return self.visiter(node.corps, nouvel_env)
        
        env.definir_fonction(node.nom, fonction_wrapper)
        return fonction_wrapper
    
    def visiter_AppelFonction(self, node, env):
        logger.debug(f"Appel de la fonction: {node.nom}")
        fonction = env.obtenir_fonction(node.nom)
        
        if fonction is None:
            logger.error(f"Fonction non trouvée: {node.nom}")
            raise ValueError(f"Fonction non définie: {node.nom}")
        
        # Évaluation des arguments
        args = [self.visiter(arg, env) for arg in node.arguments]
        logger.debug(f"Arguments évalués: {args}")
        
        # Si c'est une fonction native (Python)
        if callable(fonction):
            logger.debug("Appel d'une fonction native")
            return fonction(*args)
            
        # Si c'est une fonction LOKA
        nouvel_env = Environnement(env)
        for param, arg in zip(fonction.parametres, args):
            nouvel_env.definir_variable(param, arg)
        
        return self.visiter(fonction.corps, nouvel_env)

    def visiter_AppelMethode(self, node, env):
        logger.debug(f"Appel de la méthode: {node.methode}")
        objet = self.visiter(node.objet, env)
        methode = getattr(objet, node.methode)
        arguments = [self.visiter(arg, env) for arg in node.arguments]
        logger.debug(f"Arguments évalués: {arguments}")
        return methode(*arguments)
    
    def visiter_Affectation(self, node, env):
        logger.debug(f"Affectation de la variable: {node.nom}")
        valeur = self.visiter(node.valeur, env)
        env.definir_variable(node.nom, valeur)
        return valeur
    
    def visiter_BlocCode(self, node, env):
        logger.debug("Visite d'un bloc de code")
        resultats = []
        for instruction in node.instructions:
            resultat = self.visiter(instruction, env)
            resultats.append(resultat)
        return resultats
    
    def visiter_Nombre(self, node, env):
        logger.debug(f"Visite d'un nombre: {node.valeur}")
        return node.valeur
    
    def visiter_Chaine(self, node, env):
        logger.debug(f"Visite d'une chaîne: {node.valeur}")
        return node.valeur
    
    def visiter_Identifiant(self, node, env):
        logger.debug(f"Visite d'un identifiant: {node.nom}")
        return env.obtenir_variable(node.nom)
    
    def visiter_Liste(self, node, env):
        logger.debug("Visite d'une liste")
        return [self.visiter(element, env) for element in node.elements]
    
    def visiter_OperationBinaire(self, node, env):
        logger.debug("Évaluation d'une opération binaire")
        gauche = self.visiter(node.gauche, env)
        droite = self.visiter(node.droite, env)
        logger.debug(f"Opération: {gauche} {node.operateur.type} {droite}")
        
        if node.operateur.type == TokenType.PLUS:
            if isinstance(gauche, str) or isinstance(droite, str):
                return str(gauche) + str(droite)
            return gauche + droite
        elif node.operateur.type == TokenType.MOINS:
            return gauche - droite
        elif node.operateur.type == TokenType.MULTIPLIE:
            return gauche * droite
        elif node.operateur.type == TokenType.DIVISE:
            if droite == 0:
                raise ValueError("Division par zéro")
            return gauche / droite
        elif node.operateur.type == TokenType.PLUS_EGAL:
            resultat = gauche + droite
            if isinstance(node.gauche, Identifiant):
                env.definir_variable(node.gauche.nom, resultat)
            return resultat
        elif node.operateur.type == TokenType.MOINS_EGAL:
            resultat = gauche - droite
            if isinstance(node.gauche, Identifiant):
                env.definir_variable(node.gauche.nom, resultat)
            return resultat
            
        raise ValueError(f"Opérateur non supporté: {node.operateur.type}")
