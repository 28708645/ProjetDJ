from JeuSequentiel import JeuSequentiel
from Strategie import Strategie
class StrategieHumaine(Strategie):
    """
    Represente une strategie de jeu humaine pour tout jeu sequentiel
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
        return nextCoup