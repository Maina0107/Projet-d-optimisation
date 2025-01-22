#! usr/bin/python
# -*- coding: utf-8 -*-

from numpy import ndarray
import numpy as np
from typing import List, Tuple
from math import sqrt

# ----------------------------------------------------------------------------
#  data structure
# ----------------------------------------------------------------------------

        
class PCentreData:
    
    def __init__(self, p : int = 0, nb_installations: int = 0, nb_clients: int = 0, abscisse_client : List[int] = None, ordonnee_client : List[int] = None, 
                 abscisse_installation : List[int] = None, ordonnee_installation : List[int] = None, capacites : List[int] = None, demandes : List[int] = None, 
                 distances_triees : List[float] = None, matrice_distances : ndarray = None):
        
        # Initialisation des attributs
        self.p = p 
        self.nb_installations = nb_installations       
        self.nb_clients = nb_clients             
        self.abscisse_client = abscisse_client if abscisse_client is not None else []
        self.ordonnee_client = ordonnee_client if ordonnee_client is not None else []
        self.abscisse_installation = abscisse_installation if abscisse_installation is not None else []
        self.ordonnee_installation = ordonnee_installation if ordonnee_installation is not None else []
        self.capacites = capacites          
        self.demandes = demandes              
        self.matrice_distances = matrice_distances
        self.distances_triees = distances_triees


    def lecture(self, dataFile):

        try:
            with open(dataFile, "r") as file:
                # lecture de la 1ère ligne et séparation des éléments de la ligne
                # dans un tableau en utilisant l'espace comme séparateur
                line = file.readline()  
                lineTab = line.split()
                
                # la valeur de la 1ère case indique le nombre de noeuds (F=C) 
                # (attention de penser à convertir la chaîne de caractère en un entier)
                self.nb_clients = int(lineTab[0])
                self.nb_installations = int(lineTab[0])
    
                # la valeur de la 2ème case correspond au nombre d'installations à ouvrir (p)
                self.p = int(lineTab[1])
                
                # pour chaque ligne contenant les informations sur les noeuds
                self.abscisse_client =[]
                self.abscisse_installation = []
                self.ordonnee_client = []
                self.ordonnee_installation = []
                self.capacites = []
                self.demandes = []


                for i in range(self.nb_clients):
                    # lecture de la ligne suivante et séparation des éléments de la ligne
                    # dans un tableau en utilisant l'espace comme séparateur
                    line = file.readline()
                    lineTab = line.split()
                    
                    # ajout de l'élément de la 1ère case au tableau qui contient les abscisses 
                    self.abscisse_client.append(int(lineTab[0]))
                    self.abscisse_installation.append(int(lineTab[0]))
                    # ajout de l'élément de la 2ème case au tableau qui contient les ordonnées 
                    self.ordonnee_client.append(int(lineTab[1]))
                    self.ordonnee_installation.append(int(lineTab[1]))
                    # ajout de l'élément de la 3ème case au tableau qui contient les capacités
                    self.capacites.append(int(lineTab[2]))
                    # ajout de l'élément de la 4ème case au tableau qui contient les demandes
                    self.demandes.append(int(lineTab[3]))   
        
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{dataFile}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    def distances(self):

        self.matrice_distances = np.zeros((self.nb_clients, self.nb_installations))

        for i in range (self.nb_clients) : 
            for j in range (self.nb_installations) :
                self.matrice_distances[i, j] = round(sqrt((self.abscisse_client[i] - self.abscisse_installation[j])**2 + (self.ordonnee_client[i] - self.ordonnee_installation[j])**2),2)


    def tri_distances(self):

        self.distances_triees = []

        self.distances_triees = self.matrice_distances[np.tril_indices(self.matrice_distances.shape[0])]
        self.distances_triees = np.unique(self.distances_triees)
        self.distances_triees = np.sort(self.distances_triees)

    
    def affichage(self):
        
        print("Installations :", self.nb_installations)
        print("Clients :", self.nb_clients)
        print("Abscisses :", self.abscisse_client)
        print("Ordonnées :", self.ordonnee_client)
        print("Capacités :", self.capacites)
        print("Demandes :", self.demandes)

        print("Matrice des distances : ", self.matrice_distances)

        print("Distances triées : ", self.distances_triees)

