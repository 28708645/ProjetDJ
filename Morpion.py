from JeuSequentiel import JeuSequentiel
import numpy as np
class Morpion(JeuSequentiel):
    """
    Represente le jeu du morpion(3x3)
    """
    def __init__(self):
       super().__init__()
       self.Config["Plateau"]=[[0,0,0],[0,0,0],[0,0,0]]
       
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
            for j in range(0,len(ligne)):
                case=ligne[j]
                if(case == 0):
                    rep.append((i,j))
        return rep

    
    def afficheJeu(self):
        plateau= self.Config["Plateau"]   
        print("+-----------+")
        toPrint=""
        for ligne in plateau:
            toPrint+="|"
            for case in ligne:
                if(case==1):
                    toPrint+=" X |"
                elif(case==2):
                    toPrint+=" O |"
                else:
                    toPrint+="   |"
            
            print(toPrint)
            toPrint=""                
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
        plateau[i][j]=courant
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
        ligneBool , _ = self.ligneComplete(plateau)
        colonneBool , _ = self.colonneComplete(plateau)
        diagBool , _ = self.diagonaleComplete(plateau)
        ended=( ligneBool or colonneBool or diagBool)
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
            
    def getGagnant(self,C):
        plateau=C["Plateau"]
        ligneBool , winner = self.ligneComplete(plateau)
        colonneBool , winner = self.colonneComplete(plateau)
        diagBool , winner = self.diagonaleComplete(plateau)
        ended=(ligneBool or colonneBool or diagBool)
        if(ended):
            return winner
        else:
            if(C["NbCoup"]==9):
                self.egalite=True
                return 0
    
    def ligneComplete(self,plateau):
        for ligne in plateau:
            if((ligne==[1,1,1])):
                return (True,1)
            if((ligne==[2,2,2])):
                return (True,2)
        return (False,0)
    
    def colonneComplete(self,plateau):
        for i in range (0, len(plateau)):
            colonne= np.array(plateau)[:,i]
            if ((all (colonne==[1,1,1]))):
                return (True,1)
            if((all(colonne==[2,2,2]))):
                return (True,1)
        return (False,0)
    
    def diagonaleComplete(self,plateau):
        diag1=[plateau[2][0],plateau[1][1],plateau[0][2]]
        diag2=[plateau[0][0],plateau[1][1],plateau[2][2]]
        if((diag1==[1,1,1]) or (diag2==[1,1,1])):
                return (True,1)
        if((diag1==[2,2,2])or (diag2==[2,2,2])):
                return (True,1)
        return (False,0)
    
    def opportunite(plateau,i,j,tour):
        ligne= plateau[i]
        opEnligne=1
        if(tour==1):
            ennemi=2
        else:
            ennemi=1

        for case in ligne :
            if (case==ennemi):
                opEnligne=0
        diags=[(2,0),(1,1),(0,2),(0,0),(2,2)]
        opEnDiag=0
        if((i,j) in diags):
            opEnDiag=2
            diag1=[plateau[2][0],plateau[1][1],plateau[0][2]]
            diag2=[plateau[0][0],plateau[1][1],plateau[2][2]]
            if(ennemi in diag1):
                opEnDiag-=1
            if(ennemi in diag2):
                opEnDiag-=1
        
        colonne= list(np.array(plateau)[:,j])
        opEnColonne=1
        for case in colonne:
            if(case==ennemi):
                opEnColonne-=1
        return opEnligne+opEnDiag+opEnColonne
