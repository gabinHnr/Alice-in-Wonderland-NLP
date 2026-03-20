import csv
import argparse
import requests
import json

# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book


from collections import Counter



# fonction d'initialisation qui permet d'initialiser tout ce qu'on na besoin pour le code
# def init():
parser = argparse.ArgumentParser()

VariableType = parser.add_mutually_exclusive_group()
VariableType.add_argument('--lexdiv', metavar='ID', type=int, nargs="+", help='lexdiv parameters follow by id')
args = parser.parse_args()





def Info_Book():
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
    Dict_lexdiv = {}
    ID = args.lexdiv[0]
    response = download_book(Livre_infos, ID)

    # print(Book)


    # with open()
    # response = requests.get(f'https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt')
    # response.raise_for_status()
    # content = response.text


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

if args.lexdiv:
    print(lexdiv())