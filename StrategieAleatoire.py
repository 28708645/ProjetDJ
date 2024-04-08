from JeuSequentiel import JeuSequentiel
from Strategie import Strategie
import random
class StrategieAleatoire(Strategie):
   """
   Representeunestrategiedejeualeatoirepourtoutjeusequentiel
   """
   def __init__(self,jeu:JeuSequentiel):
      super().__init__(jeu)

   def choisirProchainCoup(self,C):
      """
      Choisit un coupale atoire suivant une distribution uniforme 
      sur tous les coups possibles dans la configuration C
      """
      cValides=self.jeu.coupsPossibles(C)
      #print(cValides)
      nextCoup=random.choice(cValides)
      return nextCoup