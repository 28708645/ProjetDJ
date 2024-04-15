from JeuSequentiel import JeuSequentiel
from Strategie import Strategie
import random
from copy import deepcopy
import numpy as np
class StrategieMiniMax(Strategie):
    """
    Represente une strategie de jeu aleatoire pour tout jeu sequentiel
    """
    def __init__(self,jeu:JeuSequentiel,k:int):
        super().__init__(jeu)
        self.profondeur=k

    def choisirProchainCoup(self,C):
        """
        Choisit un coup aleatoire suivant une distribution uniforme 
        sur tous les coups possibles dans la configuration C
        """
        cValides=self.jeu.coupsPossibles(C)
        #print(cValides)
        plateau = C["Plateau"]
        tour = C["Courant"]
        nextCoup= self.decision(C,cValides,self.profondeur,tour)
        #print("Par décision je joue le coup :", nextCoup)
        return nextCoup
    
    def decision(self,C,listecoup,profondeur,tour):
        bestmove=None
        ev = float("-inf")
        tab = np.zeros((3, 3), dtype=int)
        for i in listecoup :
            test = self.estimation(C, i, tour,profondeur)
            #print("coup= ",i," evalue a ", test)
            if(test>ev):
                bestmove =i
                ev =test
                #print("bestcoup= ",bestmove," evalue a ", ev)
            l, c = i
            tab[l, c] = test
        #print("tab eval")
        #print("+-----------+")
        #toPrint=""
        #for ligne in tab:
        #    toPrint+="|"
        #    for case in ligne:
        #        toPrint+=" "+str(case)+" |"
        #    print(toPrint)
        #    toPrint=""                
        #print("+-----------+")
        return bestmove 
    
    def estimation(self,C,coup,tour,profondeur) :
        """
        etatjeu*Coup*reel->reel
        """
        ####################################################
        # A REVOIR VALEUR CALCULE POUR LES BRANCHES DE MIN #
        ####################################################

        #if (profondeur==1) :
        #    print("PROFONDEUR 1", profondeur)
        #Ne sors pas
        copie= deepcopy(C)
        copieApCoup=self.jeu.joueLeCoup(copie,coup)
        #print("profondeur", profondeur)
        #self.jeu.Config = copieApCoup
        #self.jeu.afficheJeu()
        #Ne sors pas
        lcv=self.jeu.coupsPossibles(copieApCoup)
        aqui= self.jeu.joueurCourant(copieApCoup)
        #print(tour, aqui)
        listeseval=[] 
        #Test victoire
        if (self.jeu.estFini(copieApCoup)) :
            if(self.jeu.getGagnant(copieApCoup)==tour) :
                listeseval.append(100000)
            elif(self.jeu.getGagnant(copieApCoup)==0) :
                listeseval.append(0)
            else:
                listeseval.append(-100000)  
            return listeseval[0]  
        ###
        else :
            if (profondeur==0) :
                return self.evaluation(copieApCoup,tour)
            if (tour==aqui):    #On est dans un MAX
                for cou in lcv:
                    #tmp = self.estimation(copieApCoup,cou,tour,profondeur-1)
                    #print(coup, "->", cou, ":", tmp)
                    #listeseval.append(tmp)
                    listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
                #arg = np.argmax(listeseval)
                #print(coup, "evalue a", max(listeseval), " avec", lcv[arg])
                return max(listeseval)
            else :      #On est dans un MIN
                for cou in lcv:
                    #tmp = self.estimation(copieApCoup,cou,tour,profondeur-1)
                    #print(coup, "->", cou, ":", tmp)
                    #listeseval.append(tmp)
                    listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
                #arg = np.argmin(listeseval)
                #print(coup, "evalue a", min(listeseval), " avec", lcv[arg])
                return min(listeseval)
    
    def evaluation(self,C,tour):
        if(tour==1):
            return self.jeu.f1(C)
        else:
            return self.jeu.f2(C)