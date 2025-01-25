#!/bin/bash

dossier_Instances="Instances"
dossier_Solutions="Solutions"
dossier_Experimentation="Experimentations"

###### ATTENTIOOOOOOON CREER LES DOSSIERS DANS Code !!!!!!!!!!!!!!!!!!!!!!!!!

Noeuds=(30) # Ensemble des valeur possible de n
# Les valeurs de p pour chaque n
P_5=(1 2 3) 
P_10=(1 2 3)
P_20=(2 5 6)
P_30=(3 7 10)
P_50=(5 12 16)

index=(1 2 3 4 5) # Ensemble des valeurs possibles de i
version=(1 2 3) # Les versions du problème
capacite=(0 1 2) # Les valeurs d'activation de la contrainte de capacité
TL=300  # Temps limite de résolution

for n in "${Noeuds[@]}"; do
    results_file="${dossier_Experimentation}/results_n${n}.txt"
    rm -f "$results_file" 
    echo "n p i v c erreur statut etat temps_creation temps gap obj obj_upper obj_lower" >> "${results_file}" # Entête du fichier de résultats
    mesP="P_${n}[@]"
    for p in "${!mesP}"; do
        for i in "${index[@]}"; do
            instance="${dossier_Instances}/n${n}p${p}i${i}"
            for v in "${version[@]}"; do
                for c in "${capacite[@]}"; do
                    echo "Résolution: Instance_n${n}p${p}i${i} Modèle_v${v}_c${c}"
                    python3 solver.py -v "${v}" -c "${c}" -d "${dossier_Instances}" -t "${TL}" -n "${n}" -p "${p}" -i "${i}" -s "${dossier_Solutions}" -r "${results_file}"
                done
            done
        done 
    done    
    echo "Fin de résolution du  groupe de ${n} noeuds"
done
