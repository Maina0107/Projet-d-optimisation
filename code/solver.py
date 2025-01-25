import argparse

from data import PCentreData
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2

from pCP1_1 import VersionClassique_1
from pCP2_1 import VersionRayon_1_1
from pCP3_1 import VersionRayon_2_1

import time


def main():
    parser = argparse.ArgumentParser(description='Solver script')
    parser.add_argument('-v', '--version', required=True, type=int, choices=[1, 2, 3], help='Version of the solver')
    parser.add_argument('-c', '--avecCapacite', required=True, type=int, choices=[0, 1, 2], help='Capacity constraint')
    #parser.add_argument('-vc', '--versionCapacite', required=True, type=int, choices=[0, 1, 2], help='Version capacity constraint')
    parser.add_argument('-d', '--cheminVersInstance', required=True, help='Path to the instance')
    parser.add_argument('-t', '--tempsLimte', required=True, help='Limit time of the solver')
    parser.add_argument('-n', '--nbPoints', required=True, type=int, help='Number of nodes')
    parser.add_argument('-p', '--nbAouvrir', required=True, type=int, help='Number of facility to open')
    parser.add_argument('-i', '--indiceInstance', required=True, type=int, help='Index of the instance')
    parser.add_argument('-s', '--dossierSolution', required=True, help='Solution folder')
    parser.add_argument('-r', '--fichierResultat', required=True, help='Result file')

    args = parser.parse_args()

    print("************************** Infos for the Solver **************************")
    print(f"Version: {args.version}")
    print(f"With Capacity: {args.avecCapacite}")
    print(f"Path to Instance: {args.cheminVersInstance}")
    print(f"Time Limit: {args.tempsLimte}")
    print(f"Number of Nodes: {args.nbPoints}")
    print(f"Number to Open: {args.nbAouvrir}")
    print(f"Index of Instance: {args.indiceInstance}")
    print(f"Solution Folder: {args.dossierSolution}")
    print(f"Results file: {args.fichierResultat}")
    print("**************************************************************************")

    #___________________________Activation of the capacity constraint
    capacity = False
    if args.avecCapacite >= 1:
        capacity = True

    #__________________________ Load the data
    data = PCentreData()
    data.lecture(f'{args.cheminVersInstance}/n{args.nbPoints}p{args.nbAouvrir}i{args.indiceInstance}')
    data.distances()
    data.tri_distances()
    
    #__________________________ Create the model
    if args.version == 1 and args.avecCapacite <= 1:
        model = VersionClassique(data)
    elif args.version == 1 and args.avecCapacite == 2 :
        model = VersionClassique_1(data)
    elif args.version == 2 and args.avecCapacite <= 1:
        model = VersionRayon_1(data)
    elif args.version == 2 and args.avecCapacite == 2 :
        model = VersionRayon_1_1(data)
    elif args.version == 3 and args.avecCapacite <= 1:
        model = VersionRayon_2(data)
    else:
        model = VersionRayon_2_1(data)
    

    start_time = time.time()
    model.creer_modele(capacity)
    end_time = time.time()
    model.temps_creation = round(end_time - start_time, 5)

    #__________________________ Solve the model
    model.lancer(args.tempsLimte)

    #__________________________ Save the solution
    model.extraire_solution(capacity)
    model.solution.ecriture_sol(f'{args.dossierSolution}/n{args.nbPoints}p{args.nbAouvrir}i{args.indiceInstance}_v{args.version}c{args.avecCapacite}.sol', args.version, capacity, args.avecCapacite)

    #__________________________ write results in dataBase file
    with open(args.fichierResultat, 'a') as f:
        f.write(f'{args.nbPoints} {args.nbAouvrir} {args.indiceInstance} {args.version} {args.avecCapacite} {model.erreur} {model.statut} {model.etat} {model.temps_creation} {model.temps} {model.gap} {model.obj} {model.obj_upper} {model.obj_lower}\n')

if __name__ == "__main__":
    main()
