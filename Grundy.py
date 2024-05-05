import numpy as np
import itertools

class Grundy():
    """
    """
    def __init__(self, g, m):
        self.vals = np.ones([m+1]*g, dtype=int)
        init = [0]*g
        coupPossible = []
        for i in range(g):
            for j in range(1, m+2):
                coupPossible.append((i, j))

        ouvert = [init]
        ferme = []
        while ouvert:
            etat = ouvert[0]
            ouvert.remove(etat)
            if etat not in ferme:
                ferme.append(etat)
                for i, j in coupPossible:
                    if etat[i]+j <= m:
                        newEtat = etat[:]
                        newEtat[i] += j
                        if newEtat not in ferme:
                            ouvert.append(newEtat)

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

        #print(vals)
        #print(coupPossible)
        #print(ferme)
        #print(list_enfants)
        #print(list_parents)

        ouvert = [tuple(init)]
        ferme = []

        while ouvert:
            etat = ouvert[0]
            #print("etat :", etat)
            ouvert.remove(etat)
            if etat not in ferme:
                ferme.append(etat)
                vals_enfant = set()
                enfants = list_enfants[etat]
                #print(etat, "enfants :", enfants)
                for enfant in enfants:
                    vals_enfant.add(self.vals[enfant])
                vals_enfant = list(vals_enfant)
                if len(vals_enfant) > 0:
                    vals_enfant.sort()
                    #print(etat, "vals_enfants :", vals_enfant)
                    for i in range(vals_enfant[-1]+2):
                        if i not in vals_enfant:
                            self.vals[etat] = i
                            break
                parents = list_parents[etat]
                for parent in parents:
                    if parent not in ouvert:
                        ouvert.append(parent)

        #print(self.vals)