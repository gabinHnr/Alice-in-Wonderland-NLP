import csv
import argparse
import requests


# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.tokenization import tokenize_data
from Modules.normalize import run_normalize

# fonction d'initialisation qui permet d'initialiser tout ce qu'on na besoin pour le code
def init():
    parser = argparse.ArgumentParser()

    VariableType = parser.add_mutually_exclusive_group()
    VariableType.add_argument('-lexdiv', metavar='ID', type=int, nargs="+", help='lexdiv parameters follow by id')







# fonction qui nous permnet d'avoir notre dictionnaire demande pour le lexdiv
def lexdiv():
    Dict_lexdiv = {}
    txt = tokenize_data("The little yellow duck !")
    print(run_normalize(txt))




lexdiv()