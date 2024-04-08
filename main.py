from Morpion import Morpion
from StrategieAleatoire import StrategieAleatoire
from StrategieHumaine import StrategieHumaine


def unepartie(nomJeu, Affichage=False):
    if(nomJeu=="Morpion"):
        Jeu = Morpion()
    else:
        Jeu = Morpion()
    
    joueur1=strat1(Jeu)
    joueur2=strat2(Jeu)
    conf= Jeu.Config
    while(not Jeu.estFini(conf)):
        Ccopy=conf.copy()
        jCourant=Ccopy["Courant"]
        if(Affichage):
            print("TOUR DU JOUEUR "+str(jCourant))
            Jeu.afficheJeu()
        if(jCourant==1):
            nextCoup=joueur1.choisirProchainCoup(Ccopy)
        else:
            nextCoup=joueur2.choisirProchainCoup(Ccopy)
        Ccopy=Jeu.joueLeCoup(Ccopy,nextCoup)
        conf=Ccopy
        Jeu.Config=conf
        conf=Jeu.Config
    
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
        j1[win]+=1
    if(AfficheMin):
        print("J1 a fait "+str(j1[1])+"/"+str(nbparties)+" Victoire(s), "+str(j1[2])+"/"+str(nbparties)+" Defaite(s), "+str(j1[0])+"/"+str(nbparties)+" Nul(s)")
    return

game="Morpion"   
nbpart=20    
strat1=StrategieHumaine
strat2=StrategieAleatoire

unepartie(game,True)

        