from Strategie import Strategie
from Allumettes import Allumettes
from Grundy import Grundy
import random

class StrategieAllumettes(Strategie):
    """
    Represente la strategie optimale pour le jeu des allumettes
    """
    def __init__(self, jeu:Allumettes):
        super().__init__(jeu)
        self.grundy = Grundy(jeu.g, jeu.m).vals
        #print(self.grundy[tuple([jeu.m]*jeu.g)])
    
    def choisirProchainCoup(self, C):
        cValides=self.jeu.coupsPossibles(C)
        etatsPossible = []
        etatCurrent = C['Plateau'][:]
        #print("etat current :", etatCurrent)
        #print("coup possible :", cValides)
        for i, j in cValides:
            newEtatPossible = etatCurrent[:]
            newEtatPossible[i] -= j
            etatsPossible.append(((i, j), tuple(newEtatPossible)))
        #print("etat possible :", etatsPossible)

        for coupPossible, etatPossible in etatsPossible:
            if self.grundy[etatPossible] == 0:
                return coupPossible
        
        nextCoup=random.choice(cValides)
        return nextCoup
