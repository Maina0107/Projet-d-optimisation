from modeles import ModelesPCentre

from data import PCentreData
import pyomo.environ as pe
from pyomo.core import quicksum


class VersionRayon_1(ModelesPCentre):
    #____________________________________Override virtuals methods  to create a p-center model

    def creer_modele(self, capacite: bool = False):

        data = self.data

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_2")

        F = range(data.nb_installations)
        C = range(data.nb_clients)
        K = range(len(data.distances_tiees))
        K_len = len(data.distances_tiees)

        # variables
        # x_i vaut 1 si l'installation i est ouverte, 0 sinon
        model.x = pe.Var(F, name="x", domain=pe.Binary, bounds=(0,1))

        # z_k vaut 1 si le rayon de couverture est supérieur ou égalb à Dk, 0 sinon 
        model.z = pe.Var(range(1,K), name="z", domain=pe.Binary, bounds=(0,1))

        # objectif : minimiser la taille du rayon de couverture
        model.obj = pe.Objective(expr = (data.distances_triees[0] + quicksum( (data.distances_triees[k] - data.distances_triees[k-1])*model.z[k] for k in range(1,K_len))), sense = pe.minimize)

        if(capacite == False):

            # contraintes
            # on ouvre au plus p installations
            model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= data.p))

            # vérification de la présence d'installations ouvertes dans un rayon pour chaque client
            model.c2 = pe.ConstraintList()
            for j in C:
                for k in K:
                    model.c2.add( (1 - quicksum(model.x[i] for i in F if data.matrice_distances[i,j] < data.distances_triees[k])) <= model.z[k])
            
        else: 
                
            # y_ij vaut 1 si le client j est affecté à l'installation i, 0 sinon
            model.y = pe.Var(F, C, name="y", domain=pe.Binary, bounds=(0,1))
            
            # on ouvre au plus p installations
            model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= data.p))

            # on doit affecter chaque client à exactement 1 installation
            model.c2 = pe.ConstraintList()
            for j in C:
                model.c2.add(quicksum(model.y[i,j] for i in F) == 1)

            # on ne peut pas affecter un client à une installation si elle n'est pas ouverte
            model.c3 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c3.add(model.y[i,j] <= model.x[i])

            # vérification de la présence d'installations ouvertes dans un rayon pour chaque client
            model.c4 = pe.ConstraintList()
            for j in C:
                for k in K:
                    model.c4.add( (1 - quicksum(model.x[i] for i in F if data.matrice_distances[i,j] < data.distances_triees[k])) <= model.z[k])


            # Contrainte pour la première formulation 

            model.c5 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c5.add( (data.distances_triees[0] + quicksum( (data.distances_triees[k] - data.distances_triees[k-1])*model.z[k]  for k in range(1,K_len)) ) 
                                 >= data.matrice_distances[i,j]*model.y[i,j] )
                    

            # Contrainte pour la deuxième formulation 
            model.c5 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c5.add( quicksum(model.z[k] for k in K if data.matrice_distances[i,j] <= data.distances_triees[k])  <= model.y[i,j])


        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère
    