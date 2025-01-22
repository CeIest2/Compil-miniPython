import os
from pathlib import Path


def test_complet():
    # Récupère le chemin du dossier contenant le script
    dossier_script = Path(__file__).parent
    # Ajoute le chemin relatif vers "fichier_test"
    dossier = dossier_script / "fichier_test"

    # Vérifie si le dossier existe
    if not dossier.exists():
        print(f"Le dossier spécifié n'existe pas : {dossier}")
        return

    # Boucle sur tous les fichiers dans le dossier
    for fichier in dossier.iterdir():
        if fichier.is_file():
            print(fichier.name)





if __name__ == "__main__":
    test_complet()