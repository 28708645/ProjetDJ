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
profondeur=4
strat1=StrategieMiniMax
#strat1=StrategieHumaine
#strat1=StrategieAleatoire
#strat2=StrategieHumaine
#strat2=StrategieMiniMax
strat2=StrategieAleatoire
#unepartie(game,True)
#nparties(game, nbparties=nbpart, AfficheMin=True)
moySurnparties (game, nbparties=nbpart,nbrepet=repetition, AfficheMin=True)   