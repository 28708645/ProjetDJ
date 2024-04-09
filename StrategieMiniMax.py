from JeuSequentiel import JeuSequentiel
from Strategie import Strategie
import random
class StrategieMiniMax(Strategie):
    """
    Representeunestrategiedejeualeatoirepourtoutjeusequentiel
    """
    def __init__(self,jeu:JeuSequentiel,k:int):
        super().__init__(jeu)
        self.profondeur=k
    def choisirProchainCoup(self,C):
        """
        Choisit un coupale atoire suivant une distribution uniforme 
        sur tous les coups possibles dans la configuration C
        """
        cValides=self.jeu.coupsPossibles(C)
        #print(cValides)
        plateau = C["Plateau"]
        tour = C["Courant"]
        nextCoup= self.decision(C,cValides,self.profondeur,tour)
        return nextCoup
    def decision(self,C,listecoup,profondeur,tour):
        if (C["Courant"]==1) :
            listecoup.reverse()
            bestmove=listecoup[0]
            ev = self.estimation(C,bestmove,tour,profondeur)
        else:
            bestmove=listecoup[0]
            ev = self.estimation(C,bestmove,tour, profondeur)
            for i in listecoup :
                test = self.estimation(C, i, tour,profondeur)
                #print("coup= ",i," evalue a ", test)
                if(test>ev):
                    bestmove =i
                    ev =test
                elif(test==ev) :
                    bestmove=bestmove
                    ev=ev
                    #print("bestcoup= ",bestmove," evalue a ", ev)
        return bestmove 
    def estimation(self,C,coup,tour,profondeur) :
        """
        etatjeu*Coup*reel->reel
        """
        #if (profondeur==1) :
        #    print("PROFONDEUR 1", profondeur)
        #Ne sors pas
        copie= C.copy()
        copieApCoup=self.jeu.joueCoup(copie,coup)
        #Ne sors pas
        lcv=self.jeu.coupsPossibles(copieApCoup)
        aqui= self.jeu.joueurCourant(copieApCoup)
        listeseval=[] 
        #Test victoire
        if (self.jeu.estFini(copieApCoup)) :
            if(self.jeu.getGagnant(copieApCoup)==tour) :
                listeseval.append(100000)
            elif(self.jeu.getGagnant(copieApCoup)==0) :
                listeseval.append(-100)
            else:
                listeseval.append(-100000)  
            return listeseval[0]  
        ###
        else :
            if (profondeur==0) :
                return self.evaluation(copieApCoup,tour)
            if (tour==aqui):    #On est dans un MAX
                for cou in lcv:
                    listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
                return max(listeseval)
            else :      #On est dans un MIN
                for cou in lcv:
                    listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
            return min(listeseval)
    
    def evaluation(self,C,tour):
        if(tour==1):
            return self.jeu.f1(C)
        else:
            return self.jeu.f2(C)