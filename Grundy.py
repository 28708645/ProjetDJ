import numpy as np

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