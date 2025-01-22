import argparse
import pyomo.environ as po
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

    # Charger les données
    data = PCentreData()
    data.lecture(args.cheminVersInstance)
    data.p = args.nbToOpen

    # Choisir la version du modèle
    if args.version == 1:
        modele = VersionClassique(data)
    elif args.version == 2:
        modele = VersionRayon_1(data)
    elif args.version == 3:
        modele = VersionRayon_2(data)

    # Créer le modèle
    print("Création du modèle...")
    modele.creer_modele(capacite=(args.withCapacity == 1))



    # Nommer les fichiers de sortie
    instance_name = f"n{args.nbNodes}p{args.nbToOpen}i{args.indexOfInstance}"
    solution_file = f"{args.dossierSolution}/{instance_name}_v{args.version}c{args.withCapacity}.sol.txt"

    model_file = None

    if args.dossierModele:
        model_file = f"{args.dossierModele}/{instance_name}_v{args.version}c{args.withCapacity}.lp.txt"

    # Écrire le modèle dans un fichier si nécessaire
    if model_file:
        print(f"Écriture du modèle dans {model_file}...")
        modele.ecrire_modele(model_file)

    # Configurer et résoudre le modèle
    solver_name = 'gurobi'
    solver = po.SolverFactory(solver_name)
    if not solver.available():
        print(f"Erreur : Le solveur {solver_name} n'est pas disponible.")
        return

    if solver_name == 'appsi_highs':
        solver.options['time_limit'] = args.tempsLimte
        solver.options['mip_rel_gap'] = 1e-4
        solver.options['mip_abs_gap'] = 0.99
    elif solver_name == 'cbc':
        solver.options['seconds'] = args.tempsLimte
        solver.options['ratioGap'] = 1e-4
        solver.options['allowableGap'] = 0.99
    elif solver_name == 'gurobi':
        solver = po.SolverFactory(solver_name, solver_io="python")
        solver.options["TimeLimit"] = args.tempsLimte
        solver.options["MIPGap"] = 1e-4
        solver.options["MIPGapAbs"] =0.99

    print("Résolution du modèle...")    

    results = solver.solve(modele.modele, tee=True)

    # Vérifier si une solution a été trouvée
    if (results.solver.status == po.SolverStatus.ok) and (results.solver.termination_condition == po.TerminationCondition.optimal):
        print("Solution optimale trouvée.")
        modele.extraire_solution()
        modele.solution.ecriture_sol(instance_name, args.version, args.withCapacity == 1)
    elif results.solver.termination_condition == po.TerminationCondition.infeasible:
        print("Le problème est irréalisable.")
        PCentreSolution().ecriture_sol(instance_name, args.version, args.withCapacity == 1, irrealizable=True)
    else:
        print(f"Le solveur a rencontré une erreur : {results.solver.termination_condition}")


if __name__ == "__main__":
    main()