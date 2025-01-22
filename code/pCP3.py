from modeles import ModelesPCentre

from data import PCentreData
import pyomo.environ as pe
from pyomo.core import quicksum



class VersionRayon_2(ModelesPCentre):
   #____________________________________Override virtuals methods  to create a p-center model

   def creer_modele(self, capacite: bool = False):

        data = self.data

        #A
        #A
        #A
        #A
        #A

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_3")

        F = range(data.nb_installations)
        C = range(data.nb_clients)
        K = range(len(data.distances_tiees))
        K_len = len(data.distances_tiees)

        # variables
        # x_i vaut 1 si l'installation i est ouverte, 0 sinon
        model.x = pe.Var(F, name="x", domain=pe.Binary, bounds=(0,1))

        # u_k vaut 1 si D[k] est le rayon de couverture optimale, 0 sinon 
        model.u = pe.Var(K, name="u", domain=pe.Binary, bounds=(0,1))

        # objectif : minimiser la taille du rayon de couverture
        model.obj = pe.Objective(expr = quicksum(data.distances_triees[k]*model.u[k] for k in K), sense = pe.minimize)

        if(capacite == False):

            # contraintes

            # on ouvre au plus p installations
            model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= data.p))

            # on impose que u[k] vaut 0 i le nombre d’installations ouvertes dans le rayon Dk pour un client j est de 0
            model.c2 = pe.ConstraintList()
            for j in C:
                for k in K:
                    model.c2.add(quicksum(model.x[i] for i in F if data.matrice_distances[i,j] <= data.distances_triees[k]) >= model.u[k])
            
            # on imposent qu’il y existe un unique k tel que uk vaut 1
            model.c3 = pe.Constraint(expr = quicksum(model.u[k] for k in K) == 1)


        else: 
                #ON DOIT IMPLÉMENTER LA VERSION AVEC LES CAPACITES !!!!!!!!!!!

        #A
        #A
        #A
        #A
        #A



        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère