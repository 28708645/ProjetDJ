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
        Rend la valeur de l'evaluation de la
        configuration C pour le joueur 1
        """
        plateau = C["Plateau"]
        if self.estFini(C):
            if(self.getGagnant(C)==1) :
                return 100000
            elif(self.getGagnant(C)==0) :
                return 0
            else:
                return -100000
        else:
            return self.eval_ligne(plateau) + self.eval_colonne(plateau) + self.eval_diagonale(plateau)

    def eval_ligne(self, plateau):
        eval = 0
        for ligne in plateau:
            if (ligne == [1, 0, 0]) or (ligne == [0, 1, 0]) or (ligne == [0, 0, 1]):
                eval += 1
            elif (ligne == [1, 1, 0]) or (ligne == [0, 1, 1]) or (ligne == [1, 0, 1]):
                eval += 3
            elif (ligne == [2, 0, 0]) or (ligne == [0, 2, 0]) or (ligne == [0, 0, 2]):
                eval -= 2
            elif (ligne == [2, 2, 0]) or (ligne == [0, 2, 2]) or (ligne == [2, 0, 2]):
                eval -= 6
            else:
                eval += 0
        return eval
    
    def eval_colonne(self, plateau):
        eval = 0
        for i in range(3):
            colonne = [plateau[0][i], plateau[1][i], plateau[2][i]]
            if (colonne == [1, 0, 0]) or (colonne == [0, 1, 0]) or (colonne == [0, 0, 1]):
                eval += 1
            elif (colonne == [1, 1, 0]) or (colonne == [0, 1, 1]) or (colonne == [1, 0, 1]):
                eval += 3
            elif (colonne == [2, 0, 0]) or (colonne == [0, 2, 0]) or (colonne == [0, 0, 2]):
                eval -= 2
            elif (colonne == [2, 2, 0]) or (colonne == [0, 2, 2]) or (colonne == [2, 0, 2]):
                eval -= 6
            else:
                eval += 0
        return eval
    
    def eval_diagonale(self, plateau):
        eval = 0
        diag1=[plateau[2][0],plateau[1][1],plateau[0][2]]
        diag2=[plateau[0][0],plateau[1][1],plateau[2][2]]
        if (diag1 == [1, 0, 0]) or (diag1 == [0, 1, 0]) or (diag1 == [0, 0, 1]):
            eval += 1
        elif (diag1 == [1, 1, 0]) or (diag1 == [0, 1, 1]) or (diag1 == [1, 0, 1]):
            eval += 3
        elif (diag1 == [2, 0, 0]) or (diag1 == [0, 2, 0]) or (diag1 == [0, 0, 2]):
            eval -= 2
        elif (diag1 == [2, 2, 0]) or (diag1 == [0, 2, 2]) or (diag1 == [2, 0, 2]):
            eval -= 6
        else:
            eval += 0

        if (diag2 == [1, 0, 0]) or (diag2 == [0, 1, 0]) or (diag2 == [0, 0, 1]):
            eval += 1
        elif (diag2 == [1, 1, 0]) or (diag2 == [0, 1, 1]) or (diag2 == [1, 0, 1]):
            eval += 3
        elif (diag2 == [2, 0, 0]) or (diag2 == [0, 2, 0]) or (diag2 == [0, 0, 2]):
            eval -= 2
        elif (diag2 == [2, 2, 0]) or (diag2 == [0, 2, 2]) or (diag2 == [2, 0, 2]):
            eval -= 6
        else:
            eval += 0

        return eval

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
        plateau=C["Plateau"]
        courant=self.joueurCourant(C)
        i,j=coup
        plateau[i][j]=courant
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
        ligneBool , _ = self.ligneComplete(plateau)
        colonneBool , _ = self.colonneComplete(plateau)
        diagBool , _ = self.diagonaleComplete(plateau)
        ended=( ligneBool or colonneBool or diagBool)
        #print("ENDED ===",ended)
        if(ended):
            self.egalite=False
            C["Courant"]= self.changeJoueur(C)
            return True
        else:
            if(C["NbCoup"]==9):
                self.egalite=True
                return True
            else:
                self.egalite=False
                return False
            
    def getGagnant(self,C):
        plateau=C["Plateau"]
        ligneBool , winner = self.ligneComplete(plateau)
        colonneBool , winner = self.colonneComplete(plateau)
        diagBool , winner = self.diagonaleComplete(plateau)
        ended=(ligneBool or colonneBool or diagBool)
        if(ended):
            self.egalite=False
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
