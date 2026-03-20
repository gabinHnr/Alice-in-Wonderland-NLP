import csv
import argparse
import requests


# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book

# fonction d'initialisation qui permet d'initialiser tout ce qu'on na besoin pour le code
def init():
    parser = argparse.ArgumentParser()

    VariableType = parser.add_mutually_exclusive_group()
    VariableType.add_argument('-lexdiv', metavar='ID', type=int, nargs="+", help='lexdiv parameters follow by id')


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

download_book(Livre_infos, 11)



# fonction qui nous permnet d'avoir notre dictionnaire demande pour le lexdiv
def lexdiv():
    Dict_lexdiv = {}
    txt = tokenize_data("The little yellow duck !")
    print(run_normalize(txt))




lexdiv()