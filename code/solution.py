#! usr/bin/python
# -*- coding: utf-8 -*-

#Nommer le fichier dans lequel est écrite la solution : 
#n2p1i1_v1c1.sol.txt : solution de l'intance n2p1i1 avec version 1 et avec capacité
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

    def __init__(self, ouverture_installation : List[int] = None, affectation_client : List[int] = None, val_fonction : int = 0, statut : bool = False):

        self.ouverture_installation = ouverture_installation if ouverture_installation is not None else []

        self.affectation_client = affectation_client if affectation_client is not None else []

        self.val_fonction = val_fonction

        self.statut = statut


    #_______________________ Méthodes _______________________

        
    def ecriture_sol(self, instance_name: str, version: int, capacite: bool, irrealizable: bool = False):
        """
        Écrit la solution dans un fichier texte avec un nom adapté aux paramètres.

        :param instance_name: Nom de l'instance (par ex. "n2p1i1").
        :param version: Version du modèle (par ex. 1 ou 2).
        :param capacite: Booléen indiquant si la capacité est utilisée (True/False).
        """
        # Construire le nom du fichier en fonction des paramètres
        capacity_flag = "c1" if capacite else "c0"
        filename = f"{instance_name}_v{version}{capacity_flag}.sol.txt"
        
        try:
            with open(filename, "w") as file:
                if irrealizable:
                    # En cas de problème irréalisable, écrire -1 sur les trois lignes
                    file.write("-1 -1 -1\n")
                    file.write("-1 -1 -1\n")
                    file.write("-1\n")
                else:
                    # Ligne 1 : Indicateur d'ouverture des installations (0 ou 1)
                    ouverture_ligne = " ".join(str(int(i in self.ouverture_installation)) for i in range(len(self.affectation_client)))
                    file.write(ouverture_ligne + "\n")
                    
                    # Ligne 2 : Affectations des clients aux installations
                    affectations_ligne = " ".join(str(affectation) for affectation in self.affectation_client)
                    file.write(affectations_ligne + "\n")
                    
                    # Ligne 3 : Valeur de la fonction objectif
                    file.write(f"{self.val_fonction:.2f}\n")

        except Exception as e:
            print(f"Erreur lors de l'écriture de la solution : {e}")
