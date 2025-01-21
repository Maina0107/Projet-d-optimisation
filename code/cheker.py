#! usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from data import PCentreData
from solution import PCentreSolution

def checkSolution(data: PCentreData, sol: PCentreSolution, capa: bool) -> bool:
    #_______________ Implémenter le checker
    #
    #
    #
    #
    return True
    

def main():
    parser = argparse.ArgumentParser(description='Checker for PCentre solution.')
   
    parser.add_argument('-v', '--version', required=True, type=int, choices=[1, 2, 3], help='Version of the problem')
    parser.add_argument('-c', '--avecCapacite', required=True, type=int, choices=[0, 1], help='Capacity constraint')
    parser.add_argument('-d', '--cheminVersInstance', required=True, help='Path to the instance')
    parser.add_argument('-n', '--nbPoint', required=True, type=int, help='Number of nodes')
    parser.add_argument('-p', '--nbAouvrir', required=True, type=int, help='Number of facility to open')
    parser.add_argument('-i', '--indiceInstance', required=True, type=int, help='Index of the instance')
    parser.add_argument('-s', '--dossierSolution', required=True, help='Solution folder')
   

    args = parser.parse_args()

    print("************************** Infos for the Checker **************************")
    print(f"Version: {args.version}")
    print(f"With Capacity: {args.avecCapacite}")
    print(f"Path to Instance: {args.cheminVersInstance}")
    print(f"Number of Nodes: {args.nbPoint}")
    print(f"Number to Open: {args.nbAouvrir}")
    print(f"Index of Instance: {args.indiceInstance}")
    print(f"Solution Folder: {args.dossierSolution}")
    print("**************************************************************************")

     #___________________________Activation of the capacity constraint
    capacity = False
    if args.withCapacity == 1:
        capacity = True

    #__________________________ Load the data
    data = PCentreData()
    data.lireData(f'{args.cheminVersInstance}/n{args.nbNodes}p{args.nbToOpen}i{args.indexOfInstance}')
    
    #__________________________ Load the solution
    sol = PCentreSolution()
    sol.lireSolution(f'{args.dossierSolution}/n{args.nbNodes}p{args.nbToOpen}i{args.indexOfInstance}_v{args.version}.sol')
    

    #___________________________ Check the solution
    print(f'Check Done : {checkSolution(data, sol, capacity)}')

if __name__ == '__main__':
    main()
