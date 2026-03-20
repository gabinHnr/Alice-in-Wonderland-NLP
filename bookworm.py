import csv
import argparse
import requests
import json

# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book


from collections import Counter



# initisalisation de notyre parser
parser = argparse.ArgumentParser()

# nos actions
VariableType = parser.add_mutually_exclusive_group()
VariableType.add_argument('--lexdiv', metavar='ID', type=int, nargs="+", help='lexdiv parameters follow by id')

# notre nom pour les args
args = parser.parse_args()





def Info_Book():
    """
    Fonction qui permet de recuperer un dictionnaire contenant pour tout les livres du projet gutenberg une liste d'informations comme 
    le title, les authors, ...

    result --> Dictionnaire contrenant les inforamtions finale pour chaque text
    reader --> CSV contenant les informations sur les 75000 livres du projet Gutenbergs
    """
    reader = csv.DictReader(open('pg_catalog.csv'))
    result = {}
    for row in reader:
        key = row.pop('Text#')
        if key in result:
            pass
        result[key] = {}
        Mydico = result[key]
        # on va aller chercher pour chaque ID, le titre, l'author, le bookshelves et l'id
        Mydico.update({'id': key, 'title': row['Title'], 'authors': row['Authors'], 'bookshelves': row['Bookshelves']})
    return result


Livre_infos = Info_Book()




# fonction qui nous permnet d'avoir notre dictionnaire demande pour le lexdiv
def lexdiv():
    """
    Fonction permettant de recuperer diverses informations issu de notre livre tokenize

    "tok":int, # total number of word tokens
    "typ":int, # number of unique word tokens
    "hap":int, # number of word tokens occurring only once
    "ttr":float, # number of unique words tokens divided by number of word tokens
    "mwl":float, # mean number of characters per word token
    "mwf":float # number of word token divided by number of unique word tokens
    """
    Dict_lexdiv = {}
    ID = args.lexdiv[0]
    response = download_book(Livre_infos, ID)

    nameFIle = f"{response[1][:-4]}_token.txt"
    with open(nameFIle, "r", encoding="utf-8") as txt:
        tokens = json.load(txt)
        # print(tokens)

    tokens_unique = len(set(tokens))

    # calcul du nombre unique d'occurence pour 1 token
    nbr_unique_occurence = 0
    tp = Counter(tokens)
    for element in tp:
        if tp[element] == 1:
            nbr_unique_occurence += 1

    # calcule de la longueur moyenne
    length = []
    for mot in tokens:
        length.append(len(mot))
    longueur_moyenne = sum(length)/len(length)

    Dict_lexdiv["tok"] = len(tokens)
    Dict_lexdiv["typ"] = tokens_unique
    Dict_lexdiv["hap"] = nbr_unique_occurence
    Dict_lexdiv["ttr"] = tokens_unique/len(tokens)
    Dict_lexdiv["mwl"] = longueur_moyenne
    Dict_lexdiv["mwf"] = len(tokens)/tokens_unique


    return Dict_lexdiv


# SI on appelle notre argument dans le fichier
if args.lexdiv:
    print(lexdiv())