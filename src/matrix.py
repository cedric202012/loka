import numpy as np

class LokaMatrix:
    """Implémentation des opérations matricielles optimisées pour LOKA"""
    
    def __init__(self, data):
        self.data = np.array(data)
    
    def multiply(self, other):
        """Multiplication matricielle optimisée"""
        if isinstance(other, LokaMatrix):
            return LokaMatrix(np.dot(self.data, other.data))
        return LokaMatrix(self.data * other)
    
    def add(self, other):
        """Addition matricielle"""
        if isinstance(other, LokaMatrix):
            return LokaMatrix(self.data + other.data)
        return LokaMatrix(self.data + other)
    
    @staticmethod
    def zeros(shape):
        """Crée une matrice de zéros"""
        return LokaMatrix(np.zeros(shape))
    
    @staticmethod
    def random(shape):
        """Crée une matrice aléatoire"""
        return LokaMatrix(np.random.random(shape))
    
    def transpose(self):
        """Transpose la matrice"""
        return LokaMatrix(self.data.T)
    
    def inverse(self):
        """Calcule l'inverse de la matrice"""
        return LokaMatrix(np.linalg.inv(self.data))
