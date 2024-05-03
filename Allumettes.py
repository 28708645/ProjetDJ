from JeuSequentiel import JeuSequentiel
import numpy as np
import random
class Allumettes(JeuSequentiel):
    """
    Represente le jeu du morpion(3x3)
    """
    def __init__(self,g:int,m:int):
       super().__init__()
       for i in range (g):
           self.Config["Plateau"].append(m)
        
       
    def joueurCourant(self, C):
        return C["Courant"]
    
    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        la configuration C
        """
        rep=[]
        for i in range(0,len(C["Plateau"])):
            ligne= C["Plateau"][i]
            if(ligne >0):
                for j in range (ligne):
                    #Coup = <retirer dans groupe i j allumettes>
                    coup= (ligne,j)
                    rep.append(coup)
        return rep

    
    def afficheJeu(self):
        plateau= self.Config["Plateau"]   
        print("+-----------+")
        toPrint=""
        for groupe in plateau:
            toPrint+= ""   
        print("+-----------+")
        return

    def f1(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 1
       """
       self.joueur1.eval(C)

    def f2(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 2
       """
       -self.f1(C)
       
    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres
        que le joueur courant ait joue le coup
        dans la configuration C
        """
        plateau=C["Plateau"]
        courant=self.joueurCourant(C)
        i,j=coup
        plateau[i]=plateau[i]-j
        #Changement joueur suivant
        C["NbCoup"]= C["NbCoup"]+1
        C["History"].append(coup)
        return C
    def estFini(self, C):
        """
        Rend True si la configuration C est
        une configuration finale
        """
        plateau=C["Plateau"]
        ended=True
        for case in plateau:
            if(case!=0):
                ended=False
        #print("ENDED ===",ended)
        if(ended):
            return True
        else:
            if(C["NbCoup"]==9):
                self.egalite=True
                return True
            else:
                C["Courant"]= self.changeJoueur(C)
                return False