import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

class LokaAI:
    """Bibliothèque standard d'IA pour LOKA"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
    
    def create_neural_network(self, hidden_layers=(100,)):
        """Crée un réseau de neurones"""
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            activation='relu',
            solver='adam',
            max_iter=1000
        )
    
    def train(self, X, y):
        """Entraîne le modèle"""
        if self.model is None:
            self.create_neural_network()
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, X):
        """Fait des prédictions"""
        if self.model is None:
            raise Exception("Le modèle doit être entraîné avant de faire des prédictions")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X, y):
        """Évalue les performances du modèle"""
        if self.model is None:
            raise Exception("Le modèle doit être entraîné avant l'évaluation")
        
        X_scaled = self.scaler.transform(X)
        return self.model.score(X_scaled, y)
