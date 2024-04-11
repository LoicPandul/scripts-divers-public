import os
import re

def ajouter_bash_aux_blocs_code(chemin_dossier):
    regex_blocs_code = re.compile(r'```.*?```', re.DOTALL)

    for racine, _, fichiers in os.walk(chemin_dossier):
        for nom_fichier in fichiers:
            if nom_fichier.endswith('.md'):
                chemin_fichier = os.path.join(racine, nom_fichier)
                with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                    contenu_original = fichier.read()

                def remplacer_blocs(match):
                    bloc = match.group(0)
                    if bloc.startswith('```\n'):
                        return '```bash\n' + bloc[4:]
                    else:
                        return bloc

                nouveau_contenu = regex_blocs_code.sub(remplacer_blocs, contenu_original)

                if contenu_original != nouveau_contenu:
                    with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
                        fichier.write(nouveau_contenu)
                    
                    print(f'Le fichier "{nom_fichier}" a été mis à jour.')

if __name__ == '__main__':
    while True:
        chemin_dossier = input("Entrez le chemin vers le dossier à traiter : ").strip()
        if os.path.isdir(chemin_dossier):
            ajouter_bash_aux_blocs_code(chemin_dossier)
            print("Traitement terminé.")
        else:
            print("Le chemin fourni ne correspond pas à un dossier valide.")
        
        continuer = input("Traiter un autre dossier ? (oui/non) : ").strip().lower()
        if continuer != 'oui':
            print("Fin du programme.")
            break
