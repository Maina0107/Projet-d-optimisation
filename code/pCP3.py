from modeles import ModelesPCentre

from data import PCentreData
import pyomo.environ as pe
from pyomo.core import quicksum



class VersionRayon_2(ModelesPCentre):
   #____________________________________Override virtuals methods  to create a p-center model

   def creer_modele(self, capacite: bool = False):

        data = self.data


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

            # on impose que u[k] vaut 0 i le nombre d’installations ouvertes dans le rayon Dk pour un client j est de 0
            model.c4 = pe.ConstraintList()
            for j in C:
                for k in K:
                    model.c4.add(quicksum(model.x[i] for i in F if data.matrice_distances[i,j] <= data.distances_triees[k]) >= model.u[k])

            # on imposent qu’il y existe un unique k tel que uk vaut 1
            model.c5 = pe.Constraint(expr = quicksum(model.u[k] for k in K) == 1)


            # Contrainte 6 (première version)
            # On assure que chaque client soit affecté à une installation dont la distance n’est pas supérieure au rayon de couverture
            model.c6 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c6.add( quicksum( data.distances_triees[k]*model.u[k] for k in K )   >= model.y[i,j]*data.matrice_distances[i,j])

            # Contrainte 6 (deuxième version)
            # 
            model.c6 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c6.add( (1 - quicksum(model.u[k] for k in K if data.matrice_distances[i,j] > data.distances_triees[k] ))>= model.y[i,j])


        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère