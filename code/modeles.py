
from data import PCentreData
from solution import PCentreSolution

# ----------------------------------------------------------------------------
#  Classe mère des modèles de p-Centre
# ----------------------------------------------------------------------------

class ModelesPCentre:
    #_______________________ Attributs _______________________
    def __init__(self, mydata: PCentreData):
        self.data = mydata
        self.solution = PCentreSolution()
        self.modele = None                  # destiné à contenir le modèle d'optimisation.
        self.statut = False

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacite: bool):                                            #bool capacité : oui ou non on utilise les capacités
        raise NotImplementedError("This method should be overridden by subclasses")    #méthode abstraite
    
    #_______________________ Méthode d'écriture du modèle dans un fichier _______________________
    def ecrire_modele(self, filename):
        self.modele.write(f"{filename}.lp", io_options = {"symbolic_solver_labels":True})
        

    #_______________________ Méthode Résolution _______________________  
    #def lancer(self, tempsLimite:int):




    #_______________________ Méthode Extraction de la Solution _______________________
    def extraire_solution(self, capacite: bool):
        raise NotImplementedError("This method should be overridden by subclasses")