from modeles import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum


#####
# on modifie la contrainte pour ne pas affecter un client à une installation en dehors du rayon optimal dans le cas avec capacité
# pour comparer les deux formulations
# ATTENTION, n'est utile que si on prend en compte les capacités
#####


class VersionRayon_2_1(ModelesPCentre):
   
    def __init__(self, data):
        super().__init__(data)

    #____________________________________Override virtuals methods  to create a p-center model

    def creer_modele(self, capacite):

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_3")

        F = range(self.data.nb_installations)
        C = range(self.data.nb_clients)
        K = range(len(self.data.distances_triees))   # u_k est défini pour k allant de 0 à K

        # variables
        # x_i vaut 1 si l'installation i est ouverte, 0 sinon
        model.x = pe.Var(F, name="x", domain=pe.NonNegativeReals, bounds=(0,1))
        # u_k vaut 1 si D[k] est le rayon de couverture optimale, 0 sinon 
        model.u = pe.Var(K, name="u", domain=pe.NonNegativeReals, bounds=(0,1))

        # objectif : minimiser la taille du rayon de couverture
        model.obj = pe.Objective(expr = quicksum(self.data.distances_triees[k]*model.u[k] for k in K), sense = pe.minimize)

        # contraintes

        # on ouvre au plus p installations
        model.c1 = pe.Constraint(expr=(quicksum(model.x[i] for i in F) <= self.data.p))

        # on impose que u[k] vaut 0 i le nombre d’installations ouvertes dans le rayon Dk pour un client j est de 0
        model.c2 = pe.ConstraintList()
        for j in C:
            for k in K:
                model.c2.add(quicksum(model.x[i] for i in F if self.data.matrice_distances[i,j] <= self.data.distances_triees[k]) >= model.u[k])
        
        # on impose qu’il existe un unique k tel que uk vaut 1
        model.c3 = pe.Constraint(expr = quicksum(model.u[k] for k in K) == 1)

        # variables et contraintes à rajouter si on veut prendre en compte les capacités
        if (capacite == True): 

            # y_ij vaut 1 si le client j est affecté à l'installation i, 0 sinon
            model.y = pe.Var(F, C, name="y", domain=pe.Binary, bounds=(0,1))

            # on doit affecter chaque client à exactement 1 installation
            model.c4 = pe.ConstraintList()
            for j in C:
                model.c4.add(quicksum(model.y[i,j] for i in F) == 1)

            # on ne peut pas affecter un client à une installation si elle n'est pas ouverte
            model.c5 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c5.add(model.y[i,j] <= model.x[i])

            # capacités et demandes
            model.c6 = pe.ConstraintList()
            for i in F:
                model.c6.add((quicksum(self.data.demandes[j] * model.y[i,j] for j in C )) <= self.data.capacites[i]*model.x[i])

            # pour ne pas affecter un client à une installation en dehors du rayon optimal
            model.c7 = pe.ConstraintList()
            for i in F:
                for j in C:
                    model.c7.add( quicksum( self.data.distances_triees[k]*model.u[k] for k in K ) >= model.y[i,j]*self.data.matrice_distances[i,j])

        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère
    




    def extraire_solution(self, capacite):
        # initialisation des vecteurs à -1, et de la valeur de l'objectif à -1 aussi
        self.solution.affectation_client = [-1]*self.data.nb_clients
        self.solution.ouverture_installation = [-1]*self.data.nb_installations
        self.solution.val_fonction = -1

        # si une solution a été trouvée, on modifie les valeurs
        if (self.statut == True):
            self.solution.val_fonction = pe.value(self.modele.obj)
            # si on a choisi de prendre en compte les capacités, la variable d'affectation existe
            if (capacite == True):
                for i in range(self.data.nb_installations):
                    if (pe.value(self.modele.x[i]) >= 0.8):
                        self.solution.ouverture_installation[i] = 1
                    else :
                        self.solution.ouverture_installation[i] = 0
                    for j in range(self.data.nb_clients):
                        if (pe.value(self.modele.y[i,j]) >= 0.8):
                            self.solution.affectation_client[j] = i
            # sinon, la variable n'existe pas et il faut choisir une installation ouverte à une distance inférieure ou égale au rayon optimal trouvé
            else:
                for i in range(self.data.nb_installations):
                    if (pe.value(self.modele.x[i]) >= 0.8):
                        self.solution.ouverture_installation[i] = 1
                    else :
                        self.solution.ouverture_installation[i] = 0
                for j in range(self.data.nb_clients):
                    # on affecte le client j à la première installation ouverte dans le rayon optimal
                    for i in range (self.data.nb_installations):
                        if (self.data.matrice_distances[i,j] <= pe.value(self.modele.obj) and pe.value(self.modele.x[i]) >= 0.8):
                            self.solution.affectation_client[j] = i
                            break