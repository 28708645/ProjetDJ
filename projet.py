import numpy as np
import random
from functools import reduce
from copy import deepcopy

#########################################################
####################### LES JEUX ########################
#########################################################
class JeuSequentiel:
    """
    Represente un jeu sequentiel, a somme
    nulle, a information parfaite
    """
    def __init__(self):
        self.Config={}
        self.Config["Plateau"]=[]
        self.Config["NbCoup"]=0
        self.Config["Courant"]=1
        self.Config["History"]=[]
        self.egalite=False
        return
    
    def joueurCourant(self, C):
        
        return C["Courant"]
    
    def changeJoueur(self,C):
        cur=self.joueurCourant(C)
        if(cur==1):
            return 2
        else: 
            return 1
    
    def afficheJeu(self):
        raise NotImplementedError
    def afficheConfig(self,C):
        raise NotImplementedError
    
    def f1(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 1
       """
       raise NotImplementedError
    
    def f2(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 2
       """
       raise NotImplementedError
    
    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        la configuration C
        """
        raise NotImplementedError

    def joueLeCoup(self, C, coup):
       """
       Rend le joueur courant dans la
       configuration C
       """
       raise NotImplementedError
    
    def estFini(self, C):
        """
        Rend True si la configuration C est
        une configuration finale
        """
        raise NotImplementedError
    
    def getGagnant(self,C):
        raise NotImplementedError
    
    def getCurrentConfig(self):
        return self.Config

class Morpion(JeuSequentiel):
    """
    Represente le jeu du morpion(3x3)
    """

    def __init__(self):
       super().__init__()
       # Si 0 = aucun pion, 1 = pion j1, 2 = pion j2
       self.Config["Plateau"]=[[0,0,0],[0,0,0],[0,0,0]]
       
    def joueurCourant(self, C):
        """
        rend le joueur courant
        """
        return C["Courant"]
    
    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        la configuration C
        """
        rep=[]
        # Chaque case vide est un coup possible
        for i in range(0,len(C["Plateau"])):
            ligne= C["Plateau"][i]
            for j in range(0,len(ligne)):
                case=ligne[j]
                if(case == 0):
                    rep.append((i,j))
        return rep

    def afficheJeu(self):
        """
        permet d'afficher le plateau du morpion
        Avec j1 = X et j2 = O
        """
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
    
    def afficheConfig(self,C):
        """
        Permet d'afficher une configuration C
        Sert pour le debug du MiniMax notemment
        """
        plateau= C['Plateau']
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
            winner=self.getGagnant(C)
            if(winner==1) :
                return 100000
            elif(winner==0) :
                return -100
            else:
                return -100000
        else:
            eval_ligne=self.eval_ligne(plateau)
            eval_colonne=self.eval_colonne(plateau)
            eval_diag=self.eval_diagonale(plateau)
            return eval_ligne+eval_colonne+eval_diag

    def eval_ligne(self, plateau):
        """
        Renvoie l'évaluation du plateau pour les lignes
        Selon point de vue du joueur 1
        """
        eval = 0
        for ligne in plateau:
            if (ligne == [1, 0, 0]) or (ligne == [0, 1, 0]) or (ligne == [0, 0, 1]):
                eval += 1
            elif (ligne == [1, 1, 0]) or (ligne == [0, 1, 1]) or (ligne == [1, 0, 1]):
                eval += 3
            #On met l'accent sur le fait de bloquer l'autre en indiquant une plus mauvaise situation
            elif (ligne == [2, 0, 0]) or (ligne == [0, 2, 0]) or (ligne == [0, 0, 2]):
                eval -= 2
            elif (ligne == [2, 2, 0]) or (ligne == [0, 2, 2]) or (ligne == [2, 0, 2]):
                eval -= 6
            else:
                eval += 0
        return eval
    
    def eval_colonne(self, plateau):
        """
        Renvoie l'évaluation du plateau pour les colonnes
        Selon point de vue du joueur 1
        """
        eval = 0
        for i in range(3):
            colonne = [plateau[0][i], plateau[1][i], plateau[2][i]]
            if (colonne == [1, 0, 0]) or (colonne == [0, 1, 0]) or (colonne == [0, 0, 1]):
                eval += 1
            elif (colonne == [1, 1, 0]) or (colonne == [0, 1, 1]) or (colonne == [1, 0, 1]):
                eval += 3
            #On met l'accent sur le fait de bloquer l'autre en indiquant une plus mauvaise situation
            elif (colonne == [2, 0, 0]) or (colonne == [0, 2, 0]) or (colonne == [0, 0, 2]):
                eval -= 2
            elif (colonne == [2, 2, 0]) or (colonne == [0, 2, 2]) or (colonne == [2, 0, 2]):
                eval -= 6
            else:
                eval += 0
        return eval
    
    def eval_diagonale(self, plateau):
        """
        Renvoie l'évaluation du plateau pour les diagonales
        Selon point de vue du joueur 1
        """
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
        if(ended):
            self.egalite=False
            #Changement de joueur afin de bien afficher le bon vainqueur
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
        """
        Renvoie le joueur qui a remporte la partie
        Sert dans le MiniMax
        """
        if(self.estFini(C)):
            plateau=C["Plateau"]
            ligneBool , winner = self.ligneComplete(plateau)
            if(ligneBool):
                self.egalite=False
                return winner
            colonneBool , winner = self.colonneComplete(plateau)
            if(colonneBool):
                self.egalite=False
                return winner
            diagBool , winner = self.diagonaleComplete(plateau)
            if(diagBool):
                self.egalite=False
                return winner
            if(C["NbCoup"]==9):
                self.egalite=True
                return 0
        else:
            return 0
    
    def ligneComplete(self,plateau):
        """
        Vérifie si une ligne est complete 
        et renvoie le joueur associe si c'est le cas
        """
        for ligne in plateau:
            if((ligne==[1,1,1])):
                return (True,1)
            if((ligne==[2,2,2])):
                return (True,2)
        return (False,0)
    
    def colonneComplete(self,plateau):
        """
        Vérifie si une colonne est complete 
        et renvoie le joueur associe si c'est le cas
        """
        for i in range (0, len(plateau)):
            colonne= np.array(plateau)[:,i]
            if ((all (colonne==[1,1,1]))):
                return (True,1)
            if((all(colonne==[2,2,2]))):
                return (True,2)
        return (False,0)
    
    def diagonaleComplete(self,plateau):
        """
        Vérifie si une diagonale est complete 
        et renvoie le joueur associe si c'est le cas
        """
        diag1=[plateau[2][0],plateau[1][1],plateau[0][2]]
        diag2=[plateau[0][0],plateau[1][1],plateau[2][2]]
        if((diag1==[1,1,1]) or (diag2==[1,1,1])):
                return (True,1)
        if((diag1==[2,2,2])or (diag2==[2,2,2])):
                return (True,2)
        return (False,0)

class Allumettes(JeuSequentiel):
    """
    Represente le jeu des Allumettes
    avec g groupes de m allumettes
    """
    def __init__(self,g:int,m:int):
       super().__init__()
       self.g = g
       self.m = m
       for i in range (g):
           self.Config["Plateau"].append(m)
        
       
    def joueurCourant(self, C):
        """
        Retourne le joueur courant
        """
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
        """
        permet d'affichager le plateau du jeu
        """
        plateau= self.Config["Plateau"]   
        print("+-----------+")
        print(plateau)
        print("+-----------+")
        return

    def f1(self, C):
        """
        Rend la valeur de l’evaluation de la
        configuration C pour le joueur 1

        Utilise le théorème de Sprague_Grundy, extrait d'un site
        source : https://interstices.info/strategies-magiques-au-pays-de-nim/
        """
        plateau=C['Plateau']
        list_Bin_Groupes=[]
        for groupe in plateau:
            list_Bin_Groupes.append(bin(groupe)[2:])
        res=reduce(lambda x ,y : int(x) ^int(y),list_Bin_Groupes)
        # res == 0 on est dans une situation gagnante 
        # sinon on est dans une situation perdante 
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

#########################################################
###################### LES JOUEURS ######################
#########################################################
class Strategie:
   """
   Represente une strategie de jeu
   """
   def __init__(self,jeu:JeuSequentiel):
        self.jeu=jeu

   def choisirProchainCoup(self,C):
        """
        Choisit un coup parmi les coups possibles dans la configuration C
        """
        raise NotImplementedError

class StrategieAleatoire(Strategie):
   """
   Represente une strategie de jeu aleatoire pour tout jeu sequentiel
   """
   def __init__(self,jeu:JeuSequentiel):
      super().__init__(jeu)

   def choisirProchainCoup(self,C):
      """
      Choisit un coupale atoire suivant une distribution uniforme 
      sur tous les coups possibles dans la configuration C
      """
      coupsValides=self.jeu.coupsPossibles(C)
      nextCoup=random.choice(coupsValides)
      return nextCoup

class StrategieHumaine(Strategie):
    """
    Represente une strategie de jeu humaine pour tout jeu sequentiel
    Sert au debug ou pour s'amuser
    """
    def __init__(self,jeu:JeuSequentiel):
        super().__init__(jeu)
        
    def choisirProchainCoup(self,C):
        """
        Choisit un couple suivant une entree humaine 
        sur tous les coups possibles dans la configuration C
        """
        cValides=self.jeu.coupsPossibles(C)
        valide=False
        i=0
        while(not valide):
            print("Coup possibles :",cValides)
            tour = C["Courant"]
            try :
                c=input("Joueur "+str(tour)+": <Ligne><espace><colonne>\n")
                tab=c.split(" ")
                coup=(int(tab[0]),int(tab[1]))
                #print("Teste ",coup)
                if(coup in cValides):
                    valide=True
                    nextCoup=coup
            except IndexError:
                if(i>=1):
                    print("Quelques pb de lecture")
                if(i>=2):
                    print("Besoin de lunettes ?")
                if(i>=3):
                    print("Vous le faites expres ?")
            i+=1
            if(i>=6):
                i=1
        return nextCoup
    
class StrategieMiniMax(Strategie):
    """
    Represente une strategie de jeu MiniMax pour tout jeu sequentiel
    """
    def __init__(self,jeu:JeuSequentiel,k:int):
        super().__init__(jeu)
        self.profondeur=k

    def choisirProchainCoup(self,C):
        """
        Choisit un coup selon sa décision
        sur tous les coups possibles dans la configuration C
        """
        cValides=self.jeu.coupsPossibles(C)
        joueur = C["Courant"]
        nextCoup= self.decision(C,cValides,self.profondeur,joueur)
        return nextCoup
    
    def decision(self,C,listecoup,profondeur,joueur):
        """
        Selectionne le meilleur coup parmi les coups possibles
        selon les estimations de ces derniers
        """
        bestmove=None
        ev = float("-inf")
        bestmove_Tab=[]
        for i in listecoup :
            testEv, _ = self.estimation(C, i, joueur,joueur, profondeur)
            if(testEv>ev):
                bestmove =i
                ev =testEv
                bestmove_Tab=[i]
            elif(testEv==ev):
                bestmove_Tab.append(i)

        return bestmove 
    
    def estimation(self,C,coup,tour,joueur,profondeur) :
        """
        Realise l'estimation du coup avec l'approche MiniMax
        """
        #Joue le coup sur une copie de la config
        copie= deepcopy(C)
        tour = self.jeu.joueurCourant(copie)
        copieApCoup=self.jeu.joueLeCoup(copie,coup)
        lcv=self.jeu.coupsPossibles(copieApCoup)
        aqui= self.jeu.joueurCourant(copieApCoup)
        listeseval=[] 
        listesConfig = []
        #Test victoire
        if (self.jeu.estFini(copieApCoup)) :
            eval=self.evaluation(copieApCoup, joueur)
            return eval, copieApCoup
        else :
            if (profondeur==0) :
                eval=self.evaluation(copieApCoup, joueur)
                return eval, copieApCoup
            if (aqui==joueur):    #On est dans un MAX
                #On estime les divers coups et on fait remonter le max
                for cou in lcv:
                    res, tmp = self.estimation(copieApCoup,cou,tour,joueur,profondeur-1)
                    listeseval.append(res)
                    listesConfig.append(tmp)
                return max(listeseval), listesConfig[np.argmax(listeseval)]
            else :      #On est dans un MIN
                #On estime les divers coups et on fait remonter le min
                for cou in lcv:
                    res, tmp = self.estimation(copieApCoup,cou,tour,joueur,profondeur-1)
                    listeseval.append(res)
                    listesConfig.append(tmp)
                return min(listeseval), listesConfig[np.argmin(listeseval)]
    
    def evaluation(self,C,tour):
        """
        appel a la fonction d'evaluation du jeu
        """
        if(tour==1):
            return self.jeu.f1(C)
        else:
            return self.jeu.f2(C)

class Grundy():
    """
    Implémentation de Grundy
    """
    def __init__(self, g, m):
        # tableau de valeurs de Grundy
        self.vals = np.ones([m+1]*g, dtype=int)
        # Etat initial
        init = [0]*g
        # liste de coups possibles
        coupPossible = []
        for i in range(g):
            for j in range(1, m+2):
                coupPossible.append((i, j))

        # Récupération de tous les états
        ouvert = [init]
        ferme = []
        while ouvert:
            etat = ouvert[0]
            ouvert.remove(etat)
            # Si l'état n'est pas encore traité
            if etat not in ferme:
                ferme.append(etat)
                # On construit les états enfants atteignable depuis l'état en cours de traitement
                for i, j in coupPossible:
                    if etat[i]+j <= m:
                        newEtat = etat[:]
                        newEtat[i] += j
                        if newEtat not in ferme:
                            ouvert.append(newEtat)

        # Récupération des enfants pour chaque état
        list_enfants = dict()
        for etat in ferme:
            enfants = []
            for i, j in coupPossible:
                newEtat = etat[:]
                if etat[i]-j >= 0:
                    newEtat = etat[:]
                    newEtat[i] -= j
                    enfants.append(tuple(newEtat))
            list_enfants[tuple(etat)] = enfants
        
        # Récupération des parents pour chaque état
        list_parents = dict()
        for etat in ferme:
            parent = []
            for i, j in coupPossible:
                newEtat = etat[:]
                if etat[i]+j <= m:
                    newEtat = etat[:]
                    newEtat[i] += j
                    parent.append(tuple(newEtat))
            list_parents[tuple(etat)] = parent

        # Calcul des valeurs de Grundy
        ouvert = [tuple(init)]
        ferme = []
        while ouvert:
            etat = ouvert[0]
            ouvert.remove(etat)
            if etat not in ferme:
                ferme.append(etat)
                vals_enfant = set()
                enfants = list_enfants[etat]
                # Récupération des valeurs de Grundy de ses états enfants
                for enfant in enfants:
                    vals_enfant.add(self.vals[enfant])
                vals_enfant = list(vals_enfant)
                # S'il a au moins un enfant
                if len(vals_enfant) > 0:
                    vals_enfant.sort()
                    for i in range(vals_enfant[-1]+2):
                        if i not in vals_enfant:
                            self.vals[etat] = i
                            break
                parents = list_parents[etat]
                for parent in parents:
                    if parent not in ouvert:
                        ouvert.append(parent)

class StrategieAllumettes(Strategie):
    """
    Represente la strategie optimale pour le jeu des allumettes
    """
    def __init__(self, jeu:Allumettes):
        super().__init__(jeu)
        self.grundy = Grundy(jeu.g, jeu.m).vals
    
    def choisirProchainCoup(self, C):
        """
        Choisit le coup qui entre dans le noyau s'il existe,
        sinon choisit aléatoirement un coup
        """
        cValides=self.jeu.coupsPossibles(C)
        etatsPossible = []
        etatCurrent = C['Plateau'][:]
        # récupération des valeurs de Grundy
        for i, j in cValides:
            newEtatPossible = etatCurrent[:]
            newEtatPossible[i] -= j
            etatsPossible.append(((i, j), tuple(newEtatPossible)))

        for coupPossible, etatPossible in etatsPossible:
            # si la valeur de grundy est 0 c'est un noyau
            if self.grundy[etatPossible] == 0:
                return coupPossible
        
        # il n'y a pas d'état qui est un noyau, on choisit aléatoirement
        nextCoup=random.choice(cValides)
        return nextCoup
