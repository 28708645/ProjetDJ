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
        print(self.grundy)
    
    def choisirProchainCoup(self, C):
        cValides=self.jeu.coupsPossibles(C)
        etatsPossible = []
        etatCurrent = C['Plateau']
        for i, j in cValides:
            newEtatPossible = etatCurrent[:]
            newEtatPossible[i] -= j
            etatsPossible.append(((i, j), tuple(newEtatPossible)))

        for coupPossible, etatPossible in etatsPossible:
            if self.grundy[etatPossible] == 0:
                return coupPossible
        
        nextCoup=random.choice(cValides)
        return nextCoup

a = Allumettes(3, 5)
s = StrategieAllumettes(a)
