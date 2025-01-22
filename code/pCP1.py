from modeles import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre):

    #def __init__(self, data):
    #    super().__init__(data)
    
    #____________________________________Override virtuals methods to create a p-center model

    def creer_modele(self, capacite: bool = False):

        data = self.data

        # Création du modèle
        model = pe.ConcreteModel(name = "pCP_1")

        F = range(data.nb_installations)
        C = range(data.nb_clients)

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

        # D est plus grand que chaque distance
        model.c4 = pe.ConstraintList()
        for i in F:
            for j in C:
                model.c4.add(model.D >= data.matrice_distances[i,j]*model.y[i,j])

        # contraintes à rajouter si on veut prendre en compte les capacités
        if (capacite == True): 
            # contraintes de capacités
            model.c5 = pe.ConstraintList()
            for i in F:
                model.c5.add((quicksum(data.demandes[j] * model.y[i,j] for j in C )) <= data.capacites[i]*model.x[i])


        self.modele = model           #Va permettre d'enregistrer le modèle dans la classe mère


























    def resoudre_modele(self):
        
        if self.modele is None:
            raise ValueError("Le modèle n'a pas encore été créé. Appelez creer_modele() d'abord.")
        
        # Résoudre le modèle
        solver = pe.SolverFactory('glpk')                       ##ATTENTION, ON UTILISE QUEL SOLVEUR ????????
        resultat = solver.solve(self.modele, tee=True)
        
        # Vérifiez le statut de la solution
        if (resultat.solver.status == pe.SolverStatus.ok) and (resultat.solver.termination_condition == pe.TerminationCondition.optimal):
            print("Solution optimale trouvée.")
        else:
            print("Le solveur n'a pas trouvé de solution optimale.")


    def extraire_solution(self):

        if self.modele is None or self.modele.obj() is None:
            raise ValueError("Le modèle n'a pas encore été résolu ou aucune solution n'a été trouvée.")
        
        # Extraire les installations ouvertes
        solution_centres = [j for j in self.modele.installations if pe.value(self.modele.y[j]) == 1]
        
        # Extraire les affectations des clients aux installations
        affectations = [
            max(
                self.modele.installations,
                key=lambda j: pe.value(self.modele.x[i, j])
            )
            for i in self.modele.clients
        ]
        
        # Stocker la solution dans l'objet PCentreSolution
        self.solution = PCentreSolution(
            ouverture_installation=solution_centres,
            affectation_client=affectations,
            val_fonction=pe.value(self.modele.z)
        )
        
        print("Solution extraite avec succès.")
        print(f"Centres ouverts : {self.solution.ouverture_installation}")
        print(f"Affectations : {self.solution.affectation_client}")
        print(f"Valeur de la fonction objectif (distance max) : {self.solution.val_fonction}")

        
