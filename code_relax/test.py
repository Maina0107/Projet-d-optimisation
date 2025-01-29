#test

import data as dt
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2
from solution import PCentreSolution

import time

import pyomo.environ as pe
import pyomo.opt as po
from pyomo.core import quicksum


file = "/net/cremi/mboivent/Bureau/espaces/travail/S8/Projet_optimisation/Instances/n300p30i1"

t1_debut = time.time()
myData = dt.PCentreData() 
myData.lecture(file)
myData.distances()
myData.tri_distances()
t1_fin =time.time()
#myData.affichage()

print("données lues : ", t1_fin-t1_debut)

modV1 = VersionRayon_2(myData)
t2_debut = time.time()
modV1.creer_modele(False)
t2_fin = time.time()

print("modèle créé : ", t2_fin-t2_debut)

modV1.lancer(120)
# on doit modifier le statut dans lancer, si on a trouvé une sol ou pas
modV1.extraire_solution(False)

# Nom de l'instance  ,  version utilisée (1, 2 ou 3)  , capacité oui ou non  , si pas de capacité 0 sinon 1 ou 2
modV1.solution.ecriture_sol("n300p30i1", 3, False, 0)



