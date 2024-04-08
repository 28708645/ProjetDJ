class JeuSequentiel:
    """
    Represente un jeu sequentiel, a somme
    nulle, a information parfaite
    """

    def __init__(self):
        self.Config={}
        self.Config["Plateau"]=[]
        self.Config["NbCoup"]=0
        self.Config["Courant"]=2
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
        pass
    
    def f1(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 1
       """
       pass
    
    def f2(self, C):
       """
       Rend la valeur de l’evaluation de la
       configuration C pour le joueur 2
       """
       pass
    
    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        la configuration C
        """
        pass
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
    
    def getCurrentConfig(self):
        return self.Config