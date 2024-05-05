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
        joueur = C["Courant"]
        nextCoup= self.decision(C,cValides,self.profondeur,joueur)
        #print("Par décision je joue le coup :", nextCoup)
        return nextCoup
    
    def decision(self,C,listecoup,profondeur,joueur):
        bestmove=None
        ev = float("-inf")
        #print("------------- JE SUIS J",joueur," ----------------")
        #print("coup possible :", listecoup)
        bestmove_Tab=[]
        for i in listecoup :
            #print("j'estime le coup", i)
            testEv, _ = self.estimation(C, i, joueur,joueur, profondeur)
            #print("coup= ",i," evalue a ", testEv)
            if(testEv>ev):
                bestmove =i
                ev =testEv
                #print("bestcoup= ",bestmove," evalue a ", ev)
                bestmove_Tab=[i]
            elif(testEv==ev):
                bestmove_Tab.append(i)
        ##print("tab eval")
        """print("+-----------+")
        toPrint=""
        for ligne in tab:
            toPrint+="|"
            for case in ligne:
                toPrint+=" "+str(case)+" |"
            print(toPrint)
            toPrint=""                
        print("+-----------+")
        print("bestmove :", bestmove)
        """
        #print("bestcoup= ",bestmove," evalue a ", ev)
        #return random.choice(bestmove_Tab)
        return bestmove 
    
    def estimation(self,C,coup,tour,joueur,profondeur) :
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
        tour = self.jeu.joueurCourant(copie)
        copieApCoup=self.jeu.joueLeCoup(copie,coup)
        #print("profondeur", profondeur)
        #self.jeu.afficheConfig(copieApCoup)
        #self.jeu.Config = copieApCoup
        #self.jeu.afficheJeu()
        #Ne sors pas
        lcv=self.jeu.coupsPossibles(copieApCoup)
        aqui= self.jeu.joueurCourant(copieApCoup)
        #print("joueur =",joueur," tour =",tour, "aqui =",aqui)
        listeseval=[] 
        listesConfig = []
        #Test victoire
        if (self.jeu.estFini(copieApCoup)) :
            #print("Coup evalue ",coup)
            eval=self.evaluation(copieApCoup, joueur)
            #if(joueur==1):
            #    print("other eval = ",self.evaluation(copieApCoup,2))
            #if(joueur==2):
            #    print("other eval = ",self.evaluation(copieApCoup,1))
            #print("eval a ",eval)
            return eval, copieApCoup
        ###
        else :
            if (profondeur==0) :
                #print("Coup evalue ",coup)
                #self.jeu.afficheConfig(copieApCoup)
                #if(joueur==1):
                #    print("other eval = ",self.evaluation(copieApCoup,2))
                #if(joueur==2):
                #    print("other eval = ",self.evaluation(copieApCoup,1))
                eval=self.evaluation(copieApCoup, joueur)
                #print("eval a ",eval)
                return eval, copieApCoup
            if (aqui==joueur):    #On est dans un MAX
                #print("p =", profondeur, "on est dans un max, tour =", tour)
                for cou in lcv:
                    res, tmp = self.estimation(copieApCoup,cou,tour,joueur,profondeur-1)
                    listeseval.append(res)
                    listesConfig.append(tmp)
                    #print(coup, "->", cou, ":", res)
                    #listeseval.append(tmp)
                    #listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
                arg = np.argmax(listeseval)
                #print("p =", profondeur, coup, "evalue a", max(listeseval), " avec", lcv[arg])
                #print("HERE 6-----------  joueur= ",joueur," tour=",tour)
                #print("p =", profondeur, "Liste eval =",listeseval, " de MAX =",max(listeseval))
                return max(listeseval), listesConfig[np.argmax(listeseval)]
            else :      #On est dans un MIN
                #print("p =", profondeur, "on est dans un min, tour =", tour)
                for cou in lcv:
                    res, tmp = self.estimation(copieApCoup,cou,tour,joueur,profondeur-1)
                    listeseval.append(res)
                    listesConfig.append(tmp)
                    #print(coup, "->", cou, ":", res)
                    #listeseval.append(tmp)
                    #listeseval.append(self.estimation(copieApCoup,cou,tour,profondeur-1))
                arg = np.argmin(listeseval)
                #print("p =", profondeur, coup, "evalue a", min(listeseval), " avec", lcv[arg])
                #print("HERE 6-----------  joueur= ",joueur," tour=",tour)
                #print("p =", profondeur, "Liste eval =",listeseval, " de MIN =",min(listeseval))
                return min(listeseval), listesConfig[np.argmin(listeseval)]
    
    def evaluation(self,C,tour):
        #print("tour", tour)
        if(tour==1):
            return self.jeu.f1(C)
        else:
            return self.jeu.f2(C)