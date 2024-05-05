from JeuSequentiel import JeuSequentiel
import numpy as np
import random
from functools import reduce
class Allumettes(JeuSequentiel):
    """
    Represente le jeu du morpion(3x3)
    """
    def __init__(self,g:int,m:int):
       super().__init__()
       self.g = g
       self.m = m
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
                for j in range (1,ligne+1):
                    #Coup = <retirer dans groupe i j allumettes>
                    coup= (i,j)
                    rep.append(coup)
        return rep

    
    def afficheJeu(self):
        plateau= self.Config["Plateau"]   
        print("+-----------+")
        print(plateau)
        print("+-----------+")
        return

    def f1(self, C):
        """
        Rend la valeur de l’evaluation de la
        configuration C pour le joueur 1
        """
        plateau=C['Plateau']
        list_Bin_Groupes=[]
        for groupe in plateau:
            list_Bin_Groupes.append(bin(groupe)[2:])
        res=reduce(lambda x ,y : int(x) ^int(y),list_Bin_Groupes)
        if(res==0):
            return +10
        else:
            return 0

    def f2(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 2
       """
       return -self.f1(C)
       
    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres
        que le joueur courant ait joue le coup
        dans la configuration C
        """
        #print(coup)
        plateau=C["Plateau"]
        courant=self.joueurCourant(C)
        i,j=coup
        plateau[i]=plateau[i]-j
        #Changement joueur suivant
        C["NbCoup"]= C["NbCoup"]+1
        C["Courant"]= self.changeJoueur(C)
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
            return False