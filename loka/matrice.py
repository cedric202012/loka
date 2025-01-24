"""
Support des opérations matricielles pour LOKA
"""
import numpy as np

class Matrice:
    def __init__(self, donnees):
        self.donnees = np.array(donnees, dtype=float)
    
    def __str__(self):
        return str(self.donnees)
    
    def __repr__(self):
        return f"Matrice({self.donnees.tolist()})"
    
    def __add__(self, autre):
        if isinstance(autre, Matrice):
            return Matrice(self.donnees + autre.donnees)
        return Matrice(self.donnees + autre)
    
    def __mul__(self, autre):
        if isinstance(autre, Matrice):
            return Matrice(np.dot(self.donnees, autre.donnees))
        return Matrice(self.donnees * autre)
    
    def transposer(self):
        return Matrice(self.donnees.T)
    
    def determinant(self):
        return float(np.linalg.det(self.donnees))
    
    @staticmethod
    def creer(donnees):
        """Crée une nouvelle matrice à partir d'une liste de listes"""
        return Matrice(donnees)
