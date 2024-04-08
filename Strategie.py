from JeuSequentiel import JeuSequentiel
class Strategie:
   """
   Represente une strategie de jeu
   """
   def __init__(self,jeu:JeuSequentiel):
        self.jeu=jeu
   def choisirProchainCoup(self,C):
        """
        ChoisituncoupparmilescoupspossiblesdanslaconfigurationC
        """
        raise NotImplementedError