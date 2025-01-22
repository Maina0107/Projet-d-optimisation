from modeles import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum


class VersionRayon_1(ModelesPCentre):

    def __init__(self, data):
        super().__init__(data)

    #____________________________________Override virtuals methods  to create a p-center model

    def creer_modele(self, capacite: bool = False):

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_2")

        F = range(self.data.nb_installations)
        C = range(self.data.nb_clients)
        K = range(1,len(self.data.distances_triees))   # z_k est défini pour k allant de 1 à K

        # variables
        # x_i vaut 1 si l'installation i est ouverte, 0 sinon
        model.x = pe.Var(F, name="x", domain=pe.Binary, bounds=(0,1))
        # z_k vaut 1 si le rayon de couverture est supérieur ou égal à Dk, 0 sinon
        model.z = pe.Var(K, name="z", domain=pe.Binary, bounds=(0,1))

        # objectif : minimiser la taille du rayon de couverture
        model.obj = pe.Objective(expr = (self.data.distances_triees[0] + quicksum((self.data.distances_triees[k] - self.data.distances_triees[k-1])*model.z[k] for k in K)), sense = pe.minimize)

        # contraintes

        # on ouvre au plus p installations
        model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= self.data.p))

        # vérification de la présence d'installations ouvertes dans un rayon pour chaque client
        model.c2 = pe.ConstraintList()
        for j in C:
            for k in K:
                model.c2.add((1 - quicksum(model.x[i] for i in F if self.data.matrice_distances[i,j] < self.data.distances_triees[k])) <= model.z[k])
        
        # variables et contraintes à rajouter si on veut prendre en compte les capacités
        if (capacite == True):
                
            # y_ij vaut 1 si le client j est affecté à l'installation i, 0 sinon
            model.y = pe.Var(F, C, name="y", domain=pe.Binary, bounds=(0,1))
            
            # on doit affecter chaque client à exactement 1 installation
            model.c3 = pe.ConstraintList()
            for j in C:
                model.c3.add(quicksum(model.y[i,j] for i in F) == 1)

            # on ne peut pas affecter un client à une installation si elle n'est pas ouverte
            model.c4 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c4.add(model.y[i,j] <= model.x[i])

            # capacités et demandes
            model.c5 = pe.ConstraintList()
            for i in F:
                model.c5.add((quicksum(self.data.demandes[j] * model.y[i,j] for j in C )) <= self.data.capacites[i]*model.x[i])

            # ATTENTION Contrainte pour la première formulation
            # pour ne pas affecter un client à une installation en dehors du rayon optimal
            model.c6 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c6.add( (self.data.distances_triees[0] + quicksum((self.data.distances_triees[k] - self.data.distances_triees[k-1])*model.z[k]  for k in K) ) 
                                 >= self.data.matrice_distances[i,j]*model.y[i,j] )

            # ATTENTION Contrainte pour la deuxième formulation
            # pour ne pas affecter un client à une installation en dehors du rayon optimal
            model.c6 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c6.add( quicksum(model.z[k] for k in K if self.data.matrice_distances[i,j] <= self.data.distances_triees[k]) >= model.y[i,j])


        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère