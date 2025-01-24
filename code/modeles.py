
from data import PCentreData
from solution import PCentreSolution

import pyomo.environ as pe
import pyomo.opt as po
from pyomo.core import quicksum
from pyomo.common.errors import PyomoException
import time 

# ----------------------------------------------------------------------------
#  Classe mère des modèles de p-Centre
# ----------------------------------------------------------------------------

class ModelesPCentre:
    #_______________________ Attributs _______________________
    def __init__(self, mydata: PCentreData, gap: float = -1, temps: float = -1, obj: float = -1, obj_upper: float = -1, obj_lower: float = -1, etat: bool = False):
        self.data = mydata
        self.solution = PCentreSolution()
        self.modele = None                  # destiné à contenir le modèle d'optimisation.
        self.statut = False
        self.gap = gap
        self.temps = temps
        self.obj = obj
        self.obj_upper = obj_upper
        self.obj_lower = obj_lower
        self.etat = etat 
        self.temps_creation = -1
        self.erreur = 'ras'


    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacite: bool):                                            #bool capacité : oui ou non on utilise les capacités
        raise NotImplementedError("This method should be overridden by subclasses")    #méthode abstraite
    
    #_______________________ Méthode d'écriture du modèle dans un fichier _______________________
    def ecrire_modele(self, filename):
        if self.modele is None:
            raise ValueError("Model has not been built yet. Call build_model() first.")
        
        #self.modele.write(f"{filename}.lp", io_options = {"symbolic_solver_labels":True})
        self.modele.write(filename, io_options = {"symbolic_solver_labels":True})
        

    #_______________________ Méthode Résolution _______________________  
    #lance la résolution du modèle avec le solveur souhaité tout en affichant son log
    def lancer(self, tempsLimite:int):  
        if self.modele is None:
            raise ValueError("Model has not been built yet. Call build_model() first.")      
        
        solver_name ='appsi_highs'

        if po.SolverFactory(solver_name).available():
            print("Solver " + solver_name + " is available.")
        else:
            print("Solver " + solver_name + " is not available.")

        # Création du solveur
        solver = po.SolverFactory(solver_name)
        solver.options['time_limit'] = tempsLimite
        solver.options['mip_rel_gap'] = 1e-6
        solver.options['mip_abs_gap'] = 0.99
        solver.options['threads'] = 2  # Utiliser 2 threads

        try : 

            start_time = time.time()
            results = solver.solve(self.modele,tee=True)  # Tee = True means that the solver log is print, set Tee = False to not display the log
            end_time = time.time()

            # Quel est le type de la solution retournée 
            if(results.solver.termination_condition == po.TerminationCondition.optimal):   # Solution optmiale trouvée
                self.statut = True
                self.etat = True
            elif(results.solver.termination_condition == po.TerminationCondition.maxTimeLimit):  # Solution trouvée mais temps limite atteint 
                self.statut = True
                self.etat = False
            else:
                self.statut = False 
                self.etat = False
                print("Pas de solution calculée dans le temps limite (ou problème non borné)")

        except ValueError as ve:
            print("ValueError capturé :", ve)
            self.erreur = ve
        except RuntimeError as re:
            print("RuntimeError capturé :", re)
            self.erreur = re
        except PyomoException as ae:
            print("Erreur liée à l'exécution de Highs :", ae)
            self.erreur = ae
        except FileNotFoundError as fe:
            print("Solveur Highs introuvable :", fe)
            self.erreur = fe
        except Exception as e:
            print("Autre erreur :", e)
            self.erreur = e

        # Save the results
        if self.status:
            self.temps = round(end_time - start_time, 3)
            self.obj = round(pe.value(self.modele.obj), 3)
            self.obj_upper = round(results.problem.upper_bound, 3)
            self.obj_lower = round(results.problem.lower_bound, 3)
            self.gap = 100 * abs(self.obj_upper - self.obj_lower)
            if self.obj_upper == 0:
                self.gap = self.gap / abs(self.obj_upper)
            self.gap = round(self.gap, 2)

        # Affichage du résultat
        print("\n----------------------------------")
        print(f'Temps de résolution (s) : {end_time - start_time:.4f} seconds')
        print(f'Status du solveur = {results.solver.status}')
        print(f'Status de la résolution = {results.solver.termination_condition}')
        print(f'Valeur de la fonction objectif = {pe.value(self.modele.obj)}')
        print(f'Meilleure borne inférieure sur la valeur de la fonction objectif: { results.problem.lower_bound}')
        print(f'Meilleure borne supérieure sur la valeur de la fonction objectif: { results.problem.upper_bound}')
        print("----------------------------------")
        print(f'Gap = {self.gap}')
        print(f'Temps = {self.temps}')
        print("----------------------------------")

    #_______________________ Méthode Extraction de la Solution _______________________
    def extraire_solution(self, capacite: bool):
        raise NotImplementedError("This method should be overridden by subclasses")