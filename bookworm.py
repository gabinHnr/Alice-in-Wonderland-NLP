import csv
import argparse
import requests
import json
import nltk
from transformers import pipeline
import os
import pandas as pd
import sys

# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book
from Modules.similar import Upd_relation, Get_Similaire
from Modules.postag import run_spacy_pipeline
from Modules.decoupage import decoupage
from Modules.Get_Topics import Get_topics, get_book_vector


from collections import Counter

# initisalisation de notyre parser
parser = argparse.ArgumentParser()


def get_args():
    parser.add_argument("ID", type=int)
    VariableType = parser.add_mutually_exclusive_group()
    VariableType.add_argument('--lexdiv', action='store_true', help='lexdiv parameters follow by ID')
    VariableType.add_argument('--entities', action='store_true', help='entities parameters follow with ID')
    VariableType.add_argument('--summarize', action='store_true', help='summarize parameters follow with ID')
    VariableType.add_argument('--card', action='store_true', help='Card w/ all parameters follow with ID')
    VariableType.add_argument('--topics', action='store_true', help='topics parametres follow with ID')
    VariableType.add_argument('--similar', action='store_true', help='similar parameters follow with ID')

    # notre nom pour les args
    return(parser.parse_args())

import torch
import transformers
from transformers.pipelines import PIPELINE_REGISTRY


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
# on initialise notre variable Livre_infos pour quel soit accesible partout
Livre_infos = Info_Book()


def Info_Book_ID(ID):
    return Livre_infos.get(str(ID), None)



def Creat_relation():
    """
    FOnction qui permet de creer le csv de relation dans le cache si il n'existe pas deja
    """
    writepath = 'cache/relation.csv'

    if not os.path.exists(writepath):
        with open(writepath, 'w') as f:
            f.write("Book;Authors;Bookshelves;Vector;Similar")
    else:
        df = pd.read_csv(writepath, sep=";")
        df.to_csv(writepath, sep=';', index=False)
Creat_relation()






def lexdiv(ID):
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

    # on initialise le dictionnaire du lexdiv avec toute nos informations demandes
    Dict_lexdiv["tok"] = len(tokens)
    Dict_lexdiv["typ"] = tokens_unique
    Dict_lexdiv["hap"] = nbr_unique_occurence
    Dict_lexdiv["ttr"] = tokens_unique/len(tokens)
    Dict_lexdiv["mwl"] = longueur_moyenne
    Dict_lexdiv["mwf"] = len(tokens)/tokens_unique

    return Dict_lexdiv




def summary(ID):

    ## Initialisation des différentes variables
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

def longueur(response):
    """
    Fonction permettant de recuperer le nombre de fichier, de directory et le nom du fichier, d'un emplacement donne en parametre

    response -> parametre contenant l'emplacement d'un fichier ou directory aisni que le status de la reponse
    nameFile -> variable contenant notre emplacement sans la reponse du status
    return -> renvoie nombre de fichier =, de directory ainsi que le nom du fichier
    """
    nameFIle = f"{response[1]}"
    nameFIle = nameFIle.split("/")
    nameFIle = f"{nameFIle[0]}/{nameFIle[1]}"
    PATH = nameFIle
    files, dirs = 0, 0 # on initalise nos nombre
    # on va passer dans chaque fichier ou dossier
    for root, dirnames, filenames in os.walk(PATH):
        dirs += len(dirnames)
        files += len(filenames)
    
    return (files, dirs, nameFIle)



def Entities(ID):
    """
    FOnction qui permet de renvoyer un dictionnaiore contenant tout les personnages et lieux d'un livre donnee (avec ID)

    aucun parametre
    se sert de la fonction `download_book`
    se sert de la fonction `decoupage`
    se sert de la fonction `run_spacy_pipeline`
    
    return -> dictionnaire complet avec 2 cle, `characters` et `locations` contenant chacun des valeurs lies aux livre
    """
    # on initialise les dictionnaire
    Dict_entities = {}
    Lst_characters = []
    Lst_locations = []
    response = download_book(Livre_infos, ID)

    # on va decouper la reponse pour obtenir le fichier
    decoupage(response[1])
    


    Info_longueur = longueur(response)
    files = Info_longueur[0]
    nameFIle = Info_longueur[2]

    # on va prenjdre le nombre de fichier du directory -2 et en partant de 0, car nous avons tout les chaater + le livre ainsi que le fichier des tokens
    for i in range(1, files-2):
        with open(f"{nameFIle}/Chapter_{i}.txt", "r", encoding="utf-8") as book:
            text_brut = book.read()
        # on va aller faire la fonction pour obtenir une liste [token format txt, son type (adj, verbe, ...), son tag (Personnage, localisation, ..)]
        tag =  run_spacy_pipeline(text_brut)

        # on va parcourir notre liste, si le tag est bien une personne ou alors un lieux on l'ajoute
        for val in tag:
            if len(val[0]) > 3:
                if val[1] == 'PERSON':
                    if val[0] not in Lst_characters:
                        # if val[2] == "PROPN":
                        Lst_characters.append(val[0])
                if val[1] == "GPE" or val[1] == "LOC":
                    if val[0] not in Lst_locations:
                        Lst_locations.append(val[0])

    # on initalise nos dictionnaire
    Dict_entities["characters"], Dict_entities["locations"] = Lst_characters, Lst_locations
    return(Dict_entities)






def topics(ID):
    """
    Fonction qui permet de recuperer les 10 mots les plus poresent par chapitre, ce qui permet d'en deduire le topics du chapitre

    ne prend pas de parametre
    se sert de la fonction `download_book`
    se sert de la fonction `Get_topics`

    return --> renvoie un dictionnaire avec en cle le numero du chapitre, et en valeur uen liste des 10 mots les plus presents
    """
    Dico_mots = {}
    Dico_vecteurs = {}
    
    response = download_book(Livre_infos, ID)
    info_longueur = longueur(response)
    nbr_chap = info_longueur[0] - 2

    for i in range(1, nbr_chap):
        file_path = f"{info_longueur[2]}/Chapter_{i}.txt"
        
        mots, vecteur = Get_topics(file_path)
        
        Dico_mots[i] = mots
        Dico_vecteurs["vectors"] = vecteur
    
    return Dico_mots, Dico_vecteurs



def Similar(ID):
    Info = {}
    Info["info"] = Info_Book_ID(ID)
    Info["topics"] = topics(ID)
    return Get_Similaire(Info["info"], Info['topics'])






def Card(ID):
    Carte = {}
    Carte["info"] = Info_Book_ID(ID)
    Carte["lexdiv"] = lexdiv(ID)
    Carte["topics"] = topics(ID)
    Carte["entities"] = Entities(ID)
    Carte["summary"] = summary(ID)
    Upd_relation(Carte["info"], Carte['topics'])
    Carte["similar"] = Get_Similaire(Carte["info"], Carte['topics'])
    return (Carte)

def is_streamlit():
    return "streamlit" in sys.modules


if not is_streamlit():
    args = get_args()
# SI on appelle notre argument `--lexdiv` dans le fichier
    if args.lexdiv:
        print(lexdiv(args.ID))

    # SI on appelle notre argument `--entities` dans le fichier
    if args.entities:
        print(Entities(args.ID))

    if args.summarize:
        print(summary(args.ID))

    if args.card:
        print(Card(args.ID))
    # SI on appelle notre argument `--topics` dans le fichier
    if args.topics:
        print(topics(args.ID))

    # SI on appelle notre argument `--similar` dans le fichier
    if args.similar:
        print(Similar(args.ID))



