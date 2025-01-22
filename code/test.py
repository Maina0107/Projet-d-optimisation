#test

import data as dt
from pCP1 import VersionClassique
from solution import PCentreSolution

file = "/net/cremi/mboivent/Bureau/espaces/travail/S8/Projet d'optimisation/Instances/n3p1i1"

myData = dt.PCentreData() 
myData.lecture(file)
myData.distances()
myData.tri_distances()
#myData.affichage()

modV1 = VersionClassique(myData)
modV1.creer_modele(False)
modV1.lancer(temps limite)
# on doit modifier le statut dans lancer, si on a trouvé une sol ou pas
modV1.extraire_solution(False)
# dans extraire, tester la valeur de statut. Si true c'est ok, sinon on met que des -1
#mysolution = PCentreSolution()
modV1.solution.ecriture_sol(filename)



