import argparse
import pyomo.environ as pe
from pyomo.core import quicksum
from data import PCentreData
from solution import PCentreSolution

from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2


#chemin relatif vers le fichier (l'utilisation .. permet de revenir au dossier parent)
datafileName = 'data_CWFL/cap41.txt'

#ouverture du fichier, le ferme automatiquement à la fin et gère les exceptions


def main():
    parser = argparse.ArgumentParser(description='Solver script')
    parser.add_argument('-v', '--version', required=True, type=int, choices=[1, 2, 3], help='Version of the solver')
    parser.add_argument('-c', '--withCapacity', required=True, type=int, choices=[0, 1], help='Capacity constraint')
    parser.add_argument('-d', '--cheminVersInstance', required=True, help='Path to the instance')
    parser.add_argument('-t', '--tempsLimte', required=True, help='Limit time of the solver')
    parser.add_argument('-n', '--nbNodes', required=True, type=int, help='Number of nodes')
    parser.add_argument('-p', '--nbToOpen', required=True, type=int, help='Number of facility to open')
    parser.add_argument('-i', '--indexOfInstance', required=True, type=int, help='Index of the instance')
    parser.add_argument('-s', '--dossierSolution', required=True, help='Solution folder')
    parser.add_argument('-m', '--dossierModele', required=False, help='Model folder')

    args = parser.parse_args()

    print("************************** Infos for the Solver **************************")
    print(f"Version: {args.version}")
    print(f"With Capacity: {args.withCapacity}")
    print(f"Path to Instance: {args.cheminVersInstance}")
    print(f"Time Limit: {args.tempsLimte}")
    print(f"Number of Nodes: {args.nbNodes}")
    print(f"Number to Open: {args.nbToOpen}")
    print(f"Index of Instance: {args.indexOfInstance}")
    print(f"Solution Folder: {args.dossierSolution}")
    print(f"Model Folder: {args.dossierModele}")
    print("**************************************************************************")

    #___________________________A  Corps d'éxécution du run

    

if __name__ == "__main__":
    main()