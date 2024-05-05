from Morpion import Morpion
from Allumettes import Allumettes
from StrategieAleatoire import StrategieAleatoire
from StrategieHumaine import StrategieHumaine
from StrategieMiniMax import StrategieMiniMax
from StrategieAllumettes import StrategieAllumettes
from time import *
import numpy as np

def unepartie(nomJeu,strategie1=StrategieAleatoire,strategie2=StrategieAleatoire, Affichage=False):
    if(nomJeu=="Morpion"):
        Jeu = Morpion()
    if(nomJeu=="Allumettes"):
        Jeu = Allumettes(g,m)
    else:
        Jeu = Morpion()
    
    if strategie1 == StrategieMiniMax:
        joueur1=strategie1(Jeu, profondeur)
    else:
        joueur1=strategie1(Jeu)
    if strategie2 == StrategieMiniMax:
        joueur2=strategie2(Jeu, profondeur)
    else:
        joueur2=strategie2(Jeu)
    conf= Jeu.Config
    while(not Jeu.estFini(conf)):
        Ccopy=conf.copy()
        jCourant=Ccopy["Courant"]
        if(jCourant==1):
            nextCoup=joueur1.choisirProchainCoup(Ccopy)
        else:
            nextCoup=joueur2.choisirProchainCoup(Ccopy)
        Ccopy=Jeu.joueLeCoup(Ccopy,nextCoup)
        conf=Ccopy
        Jeu.Config=conf
        conf=Jeu.Config
        if(Affichage):
            print("TOUR DU JOUEUR "+str(jCourant))
            print("coup joue : ",nextCoup)
            Jeu.afficheJeu()
    
    if(Affichage):
        Jeu.afficheJeu()
    if(not Jeu.egalite):
        winner=Jeu.Config["Courant"]
    else:
        winner=0
    if(Affichage):
        if(not Jeu.egalite):
            print ("Vainqueur J"+str(winner))
        else:
            print ("Match Nul")
    
    #Jeu.afficheJeu()
    return winner,Jeu.Config

def nparties (nomJeu,nbparties,strategie1=StrategieAleatoire,strategie2=StrategieAleatoire,AfficheMin=False,AfficheMax=False):
    #Victoires j1,j2
    #  [N,V,D]
    j1=[0,0,0]
    for i in range(0,nbparties):
        win,conf=unepartie(nomJeu,strategie1,strategie2,AfficheMax)
        if(AfficheMin):
            print("partie ",i+1," finie J1")
        j1[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j1[1])+"/"+str(nbparties)+" Victoire(s), "+str(j1[2])+"/"+str(nbparties)+" Defaite(s), "+str(j1[0])+"/"+str(nbparties)+" Nul(s) en J1")
    j2=[0,0,0]
    for i in range(0,nbparties):
        win,_=unepartie(nomJeu,strategie2,strategie1,AfficheMax)
        if(AfficheMin):
            print("partie ",i+1," finie J2")
        j2[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j2[2])+"/"+str(nbparties)+" Victoire(s), "+str(j2[1])+"/"+str(nbparties)+" Defaite(s), "+str(j2[0])+"/"+str(nbparties)+" Nul(s) en position de J2")
    
    return j1,j2

def tempExecSurUnepartie(nomJeu,strategie1=StrategieAleatoire,strategie2=StrategieAleatoire,Affichage=False,AffichageTemps=False):
    if(nomJeu=="Morpion"):
        Jeu = Morpion()
    if(nomJeu=="Allumettes"):
        Jeu = Allumettes(g,m)
    else:
        Jeu = Morpion()
    
    chrono_Grundy1=0.0
    chrono_Grundy2=0.0
    if strategie1 == StrategieMiniMax:
        joueur1=strategie1(Jeu, profondeur)
    elif(strategie1== StrategieAllumettes):
        if(nomJeu != "Allumettes"):
            raise Exception("StrategieAllumettes utilisable que dans jeu Allumettes")
        chrono_Grundy_debut1=time()
        joueur1=strategie1(Jeu)
        chrono_Grundy_fin1=time()
        chrono_Grundy1=(chrono_Grundy_fin1-chrono_Grundy_debut1)
    else:
        joueur1=strategie1(Jeu)
    if strategie2 == StrategieMiniMax:
        joueur2=strategie2(Jeu, profondeur)
    elif(strategie2== StrategieAllumettes):
        if(nomJeu != "Allumettes"):
            raise Exception("StrategieAllumettes utilisable que dans jeu Allumettes")
        chrono_Grundy_debut2=time()
        joueur2=strategie2(Jeu)
        chrono_Grundy_fin2=time()  
        chrono_Grundy2=(chrono_Grundy_fin2-chrono_Grundy_debut2)  
    else:
        joueur2=strategie2(Jeu)
    conf= Jeu.Config
    chrono_List1=[]
    chrono_List2=[]

    chrono_partie_debut=time()
    while(not Jeu.estFini(conf)):
        Ccopy=conf.copy()
        jCourant=Ccopy["Courant"]
        if(jCourant==1):
            ###
            chrono_debut1=time()
            nextCoup=joueur1.choisirProchainCoup(Ccopy)
            chrono_fin1=time()
            chrono_List1.append(chrono_fin1-chrono_debut1)
            ###
        else:
            chrono_debut2=time()
            nextCoup=joueur2.choisirProchainCoup(Ccopy)
            chrono_fin2=time()
            chrono_List2.append(chrono_fin2-chrono_debut2)
        Ccopy=Jeu.joueLeCoup(Ccopy,nextCoup)
        conf=Ccopy
        Jeu.Config=conf
        conf=Jeu.Config
        if(Affichage):
            print("TOUR DU JOUEUR "+str(jCourant))
            Jeu.afficheJeu()
    ###
    chrono_partie_fin=time()
    if(Affichage):
        Jeu.afficheJeu()

    # Selection gagnant
    if(not Jeu.egalite):
        winner=Jeu.Config["Courant"]
    else:
        winner=0
    
    #Traitement temps
    tab1=np.array(chrono_List1)
    tab2=np.array(chrono_List2)
    mean1=np.mean(tab1)
    mean2=np.mean(tab2)

    if(AffichageTemps):
        print("Temps de la partie : ",(chrono_partie_fin-chrono_partie_debut)," secondes")
        print("Nb coups joues : ", len(Jeu.Config["History"])," coups")
        print("Temps moyen de reflexion pour joueur 1 : ",mean1," secondes")
        if((strategie1==StrategieAllumettes) and (nomJeu=="Allumettes") ):
            print("Temps de construction du Grundy pour joueur 1 :", chrono_Grundy1," secondes")
        print("Temps moyen de reflexion pour joueur 2 : ",mean2," secondes")
        if((strategie2==StrategieAllumettes) and (nomJeu=="Allumettes") ):
            print("Temps de construction du Grundy pour joueur 2 :", chrono_Grundy2," secondes")
    #Jeu.afficheJeu()
    return winner,Jeu.Config


def faceoff(nomJeu,nbparties,strategie1=StrategieAleatoire,listAdv=[StrategieAleatoire],strat1Str="",advStr=["StrategieAleatoire"],AfficheMin=False,AfficheMax=False):
    
    for i in range(len(listAdv)):
        adversaire=listAdv[i]
        adversaireNom=advStr[i]
        j1,j2=nparties(nomJeu,nbparties,strategie1,adversaire,AfficheMin,AfficheMax)
        print("+----- ",strat1Str," VS ",adversaireNom, " -----+")
        print(strat1Str, " Victoire(s) : ",j1[1],"/",nbparties," Defaite(s) : ",j1[2],"/",nbparties," Nul(s) : ",j1[0],"/",nbparties," en position de J1")
        print(strat1Str, " Victoire(s) : ",j2[2],"/",nbparties," Defaite(s) : ",j2[1],"/",nbparties," Nul(s) : ",j2[0],"/",nbparties," en position de J2")
        print("+------------------------------------------------+")
    return
#game="Morpion"  
game="Allumettes" 
nbpart=20    
repetition=4
profondeur=1
g=4
m=7
#strat1=StrategieMiniMax
#strat1=StrategieHumaine
strat1=StrategieAleatoire
#strat1=StrategieAllumettes
#strat2=StrategieHumaine
#strat2=StrategieMiniMax
#strat2=StrategieAleatoire
strat2=StrategieAllumettes
unepartie(game,strategie1=StrategieAllumettes,strategie2=StrategieMiniMax,Affichage=True)
#nparties(game, nbparties=nbpart,strategie1=StrategieMiniMax,strategie2=StrategieAllumettes, AfficheMin=True)
#moySurnparties (game, nbparties=nbpart,nbrepet=repetition, AfficheMin=True)
#unepartie(game,strategie1=StrategieMiniMax,strategie2=StrategieAleatoire,Affichage=True)
#unepartie(game,strat1,strat2,Affichage=True)  
#tempExecSurUnepartie(game,strategie1=StrategieAllumettes,strategie2=StrategieAleatoire,AffichageTemps=True) 

#faceoff(game,nbpart,strategie1=StrategieMiniMax,listAdv=[StrategieAleatoire,StrategieMiniMax,StrategieAllumettes],strat1Str="StrategieMiniMax",advStr=["StrategieAleatoire","StrategieMiniMax","StrategieAllumettes"],AfficheMin=False,AfficheMax=False)