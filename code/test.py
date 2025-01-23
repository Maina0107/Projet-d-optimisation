#test

import data as dt
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2
from solution import PCentreSolution

import pyomo.environ as pe
import pyomo.opt as po
from pyomo.core import quicksum


file = "/net/cremi/mboivent/Bureau/espaces/travail/S8/Projet_optimisation/Instances/n5p2i1"

myData = dt.PCentreData() 
myData.lecture(file)
myData.distances()
myData.tri_distances()
#myData.affichage()

modV1 = VersionRayon_1(myData)
modV1.creer_modele(False)
modV1.lancer(60)
# on doit modifier le statut dans lancer, si on a trouvé une sol ou pas
modV1.extraire_solution(False)

# Nom de l'instance  ,  version utilisée (1, 2 ou 3)  , capacité oui ou non  , si pas de capacité 0 sinon 1 ou 2
modV1.solution.ecriture_sol("n5p2i1", 2, False, 1)



