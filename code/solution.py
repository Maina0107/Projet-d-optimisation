#! usr/bin/python
# -*- coding: utf-8 -*-

#Nommer le fichier dans lequel est écrite la solution : 
#n2p1i1_v1c1_1.sol.txt : solution de l'intance n2p1i1 avec version 1 et avec capacité
#n2p1i1_v2c0.sol.txt : solution de l'intance n2p1i1 avec version 2 et sans capacité

#Nommer fichier lp :
#n2p1i1_v1c1.lp.txt : solution de l'intance n2p1i1 avec version 1 et avec capacité
#n2p1i1_v2c0.lp.txt : solution de l'intance n2p1i1 avec version 2 et sans capacité

from numpy import ndarray
import numpy as np
from typing import List, Tuple
from math import sqrt


# ----------------------------------------------------------------------------
#  Class solution
# ----------------------------------------------------------------------------
class PCentreSolution:
    #_______________________ Attributs _______________________

    def __init__(self, ouverture_installation : List[int] = None, affectation_client : List[int] = None, val_fonction : float = 0):

        self.ouverture_installation = ouverture_installation if ouverture_installation is not None else []

        self.affectation_client = affectation_client if affectation_client is not None else []

        self.val_fonction = val_fonction


    #_______________________ Méthodes _______________________

        
    def ecriture_sol(self, filename: str):

        nb_noeuds = len(self.ouverture_installation)

        with open(filename, 'w') as file:
            # les ouvertures
            for i in range(nb_noeuds) :
                file.write(str(self.ouverture_installation[i]))
                if (i < nb_noeuds-1):   # pour ne pas avoir d'espace à la fin de la ligne
                    file.write(" ")
            file.write("\n") # ligne suivante
            # les affectations
            for j in range(nb_noeuds):
                file.write(str(self.affectation_client[j]))
                if (j < nb_noeuds-1):   # pour ne pas avoir d'espace à la fin de la ligne
                    file.write(" ")
            file.write("\n") # ligne suivante
            # la valeur de l'objectif
            file.write(str(self.val_fonction))
            


    def lecture_sol(self, sol_name: str):
        numero_ligne = 1
        with open(sol_name, "r") as fichier:
            for ligne in fichier:
                match numero_ligne:
                    # la première ligne est celle des ouvertures des installations
                    case 1:
                        self.ouverture_installation = list(map(int,ligne.split(" ")))
                    # la deuxième ligne est celle des affectations
                    case 2:
                        self.affectation_client = list(map(int,ligne.split(" ")))
                    # la troisième ligne est la valeur de l'objectif
                    case 3:
                        self.val_fonction = float(ligne)
                    case _:
                        raise ValueError("Le fichier solution n'a pas le bon nombre de lignes.")
                numero_ligne += 1