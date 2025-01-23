from modeles import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre):

    def __init__(self, data):
        super().__init__(data)
    
    #____________________________________Override virtuals methods to create a p-center model

    def creer_modele(self, capacite):

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_1")

        F = range(self.data.nb_installations)
        C = range(self.data.nb_clients)

        # variables
        # x_i vaut 1 si l'installation i est ouverte, 0 sinon
        model.x = pe.Var(F, name="x", domain=pe.Binary, bounds=(0,1))
        # y_ij vaut 1 si le client j est affecté à l'installation i, 0 sinon
        model.y = pe.Var(F, C, name="y", domain=pe.Binary, bounds=(0,1))
        # D vaut la plus grande distance entre un client et son installation
        model.D = pe.Var(name="D", domain=pe.NonNegativeReals)

        # objectif : minimiser la plus grande distance
        model.obj = pe.Objective(expr = model.D, sense = pe.minimize)


        # contraintes

        # on ouvre au plus p installations
        model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= self.data.p))

        # on doit affecter chaque client à exactement 1 installation
        model.c2 = pe.ConstraintList()
        for j in C:
            model.c2.add(quicksum(model.y[i,j] for i in F) == 1)

        # on ne peut pas affecter un client à une installation si elle n'est pas ouverte
        model.c3 = pe.ConstraintList()
        for i in F:
            for j in C:
                model.c3.add(model.y[i,j] <= model.x[i])

        # D est plus grand que chaque distance
        model.c4 = pe.ConstraintList()
        for i in F:
            for j in C:
                model.c4.add(model.D >= self.data.matrice_distances[i,j]*model.y[i,j])

        # contraintes à rajouter si on veut prendre en compte les capacités
        if (capacite == True): 
            # contraintes de capacités
            model.c5 = pe.ConstraintList()
            for i in F:
                model.c5.add((quicksum(self.data.demandes[j] * model.y[i,j] for j in C )) <= self.data.capacites[i]*model.x[i])


        self.modele = model           # Va permettre d'enregistrer le modèle dans la classe mère




    def extraire_solution(self, capacite):
        # initialisation des vecteurs à -1, et de la valeur de l'objectif à -1 aussi
        self.solution.affectation_client = [-1]*self.data.nb_clients
        self.solution.ouverture_installation = [-1]*self.data.nb_installations
        self.solution.val_fonction = -1

        # si une solution a été trouvée, on modifie les valeurs
        if (self.statut == True):
            self.solution.val_fonction = pe.value(self.modele.obj)
            # c'est la même chose sans et avec les capacités
            for i in range(self.data.nb_installations):
                if (pe.value(self.modele.x[i]) >= 0.8):
                    self.solution.ouverture_installation[i] = 1
                else :
                    self.solution.ouverture_installation[i] = 0
                for j in range(self.data.nb_clients):
                    if (pe.value(self.modele.y[i,j]) >= 0.8):
                        self.solution.affectation_client[i,j] = i
