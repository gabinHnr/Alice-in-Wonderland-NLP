import os
import requests

def download_book(Dico_info, ID):
    file_name = f"{Dico_info[str(ID)]['title']}.txt"
    
    # on verifie qu'il existe pas deja
    if os.path.exists(file_name):
        print(f"Livre {ID} déjà présent localement.")
        return

    # on le telecharge
    try:
        response = requests.get(f'https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt')
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"Erreur pendant download : {e}")
        return

    # on place nos marker car on connait la ligne du ***STart ... ***
    ligne = content.splitlines() # le splitlines ici ca sert a transofmne tt nos phrases en liste de phrase
    Start_index = 0
    End_index = len(ligne)

    # nos marker present dans chaque livre
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    for i, line in enumerate(ligne):
        if start_marker in line:
            Start_index = i + 1 # on prend cjuste apres la ligne
        if end_marker in line:
            End_index = i # on s'arrete juste avant le marker
            break

    # on reecrit par dessus
    with open(file_name, "w", encoding="utf-8") as livre:
        # truc de barbare mais on recolle toute nos phrases de notre liste de phrases ensemble si elles sont comprises entre la ligne de debut e de fin et on met un \n car dans une liste de phrase on a plus d'espace
        clean_content = "\n".join(ligne[Start_index:End_index])
        # on reecrit
        livre.write(clean_content)