import csv
import argparse
import requests
import json
import nltk
from transformers import pipeline


# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book
from Modules.postag import run_spacy_pipeline
from Modules.decoupage import decoupage

from collections import Counter



# initisalisation de notyre parser
parser = argparse.ArgumentParser()

nltk.download('stopwords')
nltk.download('punkt')
nltk.download("punkt_tab")

# nos actions
parser.add_argument("ID", type=int)
VariableType = parser.add_mutually_exclusive_group()
VariableType.add_argument('--lexdiv', action='store_true', help='lexdiv parameters follow by ID')
VariableType.add_argument('--entities', action='store_true', help='entities parameters follow with ID')
VariableType.add_argument('--summarize', action='store_true', help='summarize parameters follow with ID')
VariableType.add_argument('--card', action='store_true', help='Card w/ all parameters follow with ID')


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
    ID = args.ID
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

def summary():

    ## Initialisation des différentes variables
    ID = args.ID
    download_livre = download_book(Livre_infos, ID)
    nameFile = download_livre[1].split("/")[1]

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    resume = []

    ## On parcourt les n-chapitres que l'on veut pour pouvoir faire un résumé.
    for k in range (1, 5):
        # On ouvre chaque chapitre à la fois
        with open(f"cache/{nameFile}/Chapter_{k}.txt", "r", encoding="utf-8") as txt:
            lecture = txt.read()

        # On "split" chaque chapitre pour éviter " C H A P T E R I . D o w n t h e R a b b i t - H o l e "
        seplecture = lecture.split()
        total = len(seplecture)

        ## Ceci permet de divisé le texte pour le résume en deux fois car sinon il y a un dépassement de mémoire.
        division = [
            " ".join(seplecture[0:total//2]),
            " ".join(seplecture[total//2:total:])
        ]

        # on parcourt donc les deux parties de la division et on ne prend que les 600 premiers caractères de chaque partie 
        # pour éviter le dépassement de mémoire
        for diviseur in division:
            reassemblage = " ".join(diviseur.split()[:600])
            result = summarizer(reassemblage, max_length=100, min_length=40, do_sample=False)

            resume.append(result[0]["summary_text"])

    # Enfin, on fait un résumé de tous les résumés pour avoir un "résumé final"
    resume_final = summarizer(" ".join(resume), min_length=80)
    return(resume_final[0]["summary_text"])
    

def Entities():


    Dict_entities = {}
    Lst_characters = []
    Lst_locations = []
    ID = args.ID
    response = download_book(Livre_infos, ID)

    decoupage(response[1])

    # nameFIle = f"{response[1]}"
    # with open(nameFIle, "r", encoding="utf-8") as book:
    #     text_brut = book.read()   
    

    # nameFIle = f"{response[1][:-4]}_token.txt"
    # with open(nameFIle, "r", encoding="utf-8") as txt:
    #     tokens = json.load(txt)

    # # print(tokens)
    # tag =  run_spacy_pipeline(text_brut)

    # for val in tag:
    #     # print(val)
    #     if val[1] == 'PERSON':
    #         if val[0] not in Lst_characters:
    #             # if val[2] == "PROPN":
    #             Lst_characters.append(val[0])
    #     if val[1] == "GPE" or val[1] == "LOC":
    #         if val[0] not in Lst_locations:
    #             Lst_locations.append(val[0])


    # Dict_entities["characters"], Dict_entities["locations"] = Lst_characters, Lst_locations
    # return(Dict_entities)


def Card():
    Carte = {}
    # Carte["info"] = lexdiv()
    Carte["lexdiv"] = lexdiv()
    # Carte["topics"] = lexdiv()
    Carte["entities"] = Entities()
    Carte["summary"] = summary()
    # Carte["similar"] = summary()
    return (Carte)

# SI on appelle notre argument `--lexdiv` dans le fichier
if args.lexdiv:
    print(lexdiv())

# SI on appelle notre argument `--entities` dans le fichier
if args.entities:
    print(Entities())

if args.summarize:
    print(summary())

if args.card:
    print(Card())