import os
import requests

import json

from Modules.Tokenization import tokenize_data


def download_book(Dico_info, ID):
    if os.path.exists(f"cache/{Dico_info[str(ID)]['title']}"):
        pass
    else:
        os.mkdir(f"cache/{Dico_info[str(ID)]['title']}")


    file_name = f"cache/{Dico_info[str(ID)]['title']}/{Dico_info[str(ID)]['title']}.txt"
    
    # on verifie qu'il existe pas deja
    if os.path.exists(file_name):
        print(f"Livre {ID} deja present localement.")
        print("Utilisation du cash.")
        return ["Succes", (f"cache/{Dico_info[str(ID)]['title']}/{Dico_info[str(ID)]['title']}.txt")]


    # on le telecharge
    try:
        response = requests.get(f'https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt')
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"Erreur pendant download : {e}")
        return "Error"

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
        make_token(Dico_info, ID, clean_content)
        # on reecrit
        livre.write(clean_content)
        
    return ["Succes", (f"cache/{Dico_info[str(ID)]['title']}/{Dico_info[str(ID)]['title']}.txt")]




def make_token(Dico_info, ID, Text):
    file_nom = f"cache/{Dico_info[str(ID)]['title']}/{Dico_info[str(ID)]['title']}_token.txt"
    with open(file_nom, "w", encoding="utf-8") as cache_token:
        toeknization = tokenize_data(Text, True, True)
        cache_token.write(json.dumps(toeknization))