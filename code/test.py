#test

import data as dt

file = "/net/cremi/mboivent/Bureau/espaces/travail/S8/Projet d'optimisation/Instances/n3p1i1"

myData = dt.PCentreData() 
myData.lecture(file)
myData.distances()
myData.tri_distances()
myData.affichage()

