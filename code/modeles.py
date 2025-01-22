


# ----------------------------------------------------------------------------
#  Classe mère des modèles de p-Centre
# ----------------------------------------------------------------------------

class ModelesPCentre:
    #_______________________ Attributs _______________________
    def __init__(self, data: PCentreData):
        self.data = data
        self.solution = PCentreSolution()
        self.modele = None                  # destiné à contenir le modèle d'optimisation.

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacite: bool):                                            #bool capacité : oui ou non on utilise les capacités
        raise NotImplementedError("This method should be overridden by subclasses")    #méthode abstraite
    
    #_______________________ Méthode d'écriture du modèle dans un fichier _______________________
    def ecrire_modele(self, filename):
        if self.modele is None:
            raise ValueError("Model has not been built yet. Call build_model() first.")
        # Write the model to a .lp file
        #
        #
        #
        #
        #

    #_______________________ Méthode Résolution _______________________  
   
        

    #_______________________ Méthode Extraction de la Solution _______________________
    def extraire_solution(self):
        raise NotImplementedError("This method should be overridden by subclasses")