#! usr/bin/python
# -*- coding: utf-8 -*-

#Nommer le fichier dans lequel est écrite la solution : 
#n2p1i1_v1c1.sol : solution de l'intance n2p1i1 avec version 1 et avec capacité
#n2p1i1_v2c0.sol : solution de l'intance n2p1i1 avec version 2 et sans capacité

#Nommer fichier lp :
#n2p1i1_v1c1.lp

from numpy import ndarray
import numpy as np
from typing import List, Tuple
from math import sqrt

# ----------------------------------------------------------------------------
#  Class solution
# ----------------------------------------------------------------------------
class PCentreSolution:
    #_______________________ Attributs _______________________

    def __init__(self, ouverture_installation : List[int] = None, affectation_client : List[int] = None, val_fonction : int = 0):

        self.ouverture_installation = ouverture_installation if ouverture_installation is not None else []

        self.affectation_client = affectation_client if affectation_client is not None else []

        self.val_fonction = val_fonction


    #_______________________ Méthodes _______________________

    def ecriture_sol(self) :

        
