from Morpion import Morpion
from StrategieAleatoire import StrategieAleatoire
from StrategieHumaine import StrategieHumaine
from StrategieMiniMax import StrategieMiniMax

def unepartie(nomJeu, Affichage=False):
    if(nomJeu=="Morpion"):
        Jeu = Morpion()
    else:
        Jeu = Morpion()
    
    if strat1 == StrategieMiniMax:
        joueur1=strat1(Jeu, profondeur)
    else:
        joueur1=strat1(Jeu)
    if strat2 == StrategieMiniMax:
        joueur2=strat2(Jeu, profondeur)
    else:
        joueur2=strat2(Jeu)
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
    return winner

def unepartie(nomJeu,strategie1=StrategieAleatoire,strategie2=StrategieAleatoire, Affichage=False):
    if(nomJeu=="Morpion"):
        Jeu = Morpion()
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

def nparties (nomJeu,nbparties,AfficheMin=False,AfficheMax=False):
    #Victoires j1,j2
    #  [N,V,D]
    j1=[0,0,0]
    for i in range(0,nbparties):
        win=unepartie(nomJeu,AfficheMax)
        print("partie ",i+1," finie")
        j1[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j1[1])+"/"+str(nbparties)+" Victoire(s), "+str(j1[2])+"/"+str(nbparties)+" Defaite(s), "+str(j1[0])+"/"+str(nbparties)+" Nul(s)")
    return win,j1


def nparties (nomJeu,nbparties,strategie1=StrategieAleatoire,strategie2=StrategieAleatoire,AfficheMin=False,AfficheMax=False):
    #Victoires j1,j2
    #  [N,V,D]
    j1=[0,0,0]
    for i in range(0,nbparties):
        win,conf=unepartie(nomJeu,strategie1,strategie2,AfficheMax)
        print("partie ",i+1," finie J1")
        j1[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j1[1])+"/"+str(nbparties)+" Victoire(s), "+str(j1[2])+"/"+str(nbparties)+" Defaite(s), "+str(j1[0])+"/"+str(nbparties)+" Nul(s) en J1")
    j1=[0,0,0]
    for i in range(0,nbparties):
        win,_=unepartie(nomJeu,strategie2,strategie1,AfficheMax)
        print("partie ",i+1," finie J2")
        j1[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j1[2])+"/"+str(nbparties)+" Victoire(s), "+str(j1[1])+"/"+str(nbparties)+" Defaite(s), "+str(j1[0])+"/"+str(nbparties)+" Nul(s) en position de J2")
    
    return win,j1

def moySurnparties (nomJeu,nbparties,nbrepet,AfficheMin=False,AfficheMax=False):
    winlist=[]

    for i in range (nbrepet):
        winner,scores=nparties(nomJeu,nbparties,AfficheMin,AfficheMax)
        winlist.append(scores[1])
        print("|BATCH ",i," fini|")
    sum=0
    acc=0
    for w in winlist :
        sum+=w
        acc+=nbparties
    print("Pourcentage de victoires ",(sum/acc)*100,"%")
    return

game="Morpion"   
nbpart=20    
repetition=4
profondeur=5
strat1=StrategieMiniMax
#strat1=StrategieHumaine
#strat1=StrategieAleatoire
#strat2=StrategieHumaine
strat2=StrategieMiniMax
#strat2=StrategieAleatoire
#unepartie(game,strategie1=StrategieHumaine,strategie2=StrategieMiniMax,Affichage=True)
nparties(game, nbparties=nbpart,strategie1=StrategieMiniMax,strategie2=StrategieMiniMax, AfficheMin=True)
#moySurnparties (game, nbparties=nbpart,nbrepet=repetition, AfficheMin=True)
#unepartie(game,strategie1=StrategieMiniMax,strategie2=StrategieMiniMax,Affichage=True)   