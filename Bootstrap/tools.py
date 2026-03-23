import csv
import argparse
import requests

# pr verifier si y a des stop word ou ponctuation
from nltk.corpus import stopwords
import string
import nltk 



# pr les tokens
from nltk.stem import WordNetLemmatizer
import spacy
from nltk.stem import SnowballStemmer


# pour le premier lancement il faut executer cette function
def init():
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('maxent_ne_chunker_tab')
    nltk.download('words')
    nltk.download('stopwords')
    nltk.download('wordnet')
    # python3 -m spacy download en_core_web_sm
# init()




# on va lire notre ficbier csv qui contient tt les infos de nos 75k livres
reader = csv.DictReader(open('pg_catalog.csv'))

# on va parcour nos infos et les ajouter dans un dictionnaire, voir plus bas les infos qu'on prend
result = {}
for row in reader:
    key = row.pop('Text#')
    if key in result:
        pass
    result[key] = {}
    Mydico = result[key]
    # on va aller chercher pour chaque ID, le titre, l'author, le bookshelves et l'id
    Mydico.update({'id': key, 'title': row['Title'], 'authors': row['Authors'], 'bookshelves': row['Bookshelves']})


# on defini nos argument, ceux la ne sont pas limite en nombre
parser = argparse.ArgumentParser()



# on defini nos argument:
parser.add_argument('-l', '--lower', action='store_true', help='lower')
parser.add_argument("--ID", help="id", type=int)
parser.add_argument('-postag', '--postag', nargs="+", help='tokenization')

# Pour nos Token:
parser.add_argument('-sentence', '--sent', action='store_true', help='Bool to pass token in sentence mode')
parser.add_argument('-stopWord', '--stop', action='store_true', help='Bool to remove stop word')
parser.add_argument('-punctualtion', '--punct', action='store_true', help='Bool to remove punctuation')
parser.add_argument('-stemming', '--stem', action='store_true', help='Bool to enable stemming')


# ici c'est les arguments principaux, on limite leurs utilisation a uniquement 1 par commande
VariableType = parser.add_mutually_exclusive_group()
VariableType.add_argument('-i', '--info', action='store_true', help='Increase output verbosity.')
VariableType.add_argument('-d', '--download', action='store_true', help='Download')
VariableType.add_argument('-n', '--clean', nargs="+", help='nettoyage')
VariableType.add_argument('-token', '--tokenize', nargs="+", help='tokenization')
VariableType.add_argument('-normalize', '--normalize', nargs="+", help='normalize')



# on renomme nos argument `args` pour plus de rapidite
args = parser.parse_args()




def get_info():
    # si on veut les onfromations, on prend les infos d'un de nos ID de notre dictionnaire
    print(result[str(args.ID)])



def download_book():
    # si on veut telecharger un livre
    # /!\ attention si le fichier existe deja ca va mettre une erreur il faut qu'il n'existe pas deja dans nos fichers /!\
    lineLst = []
    # on va request a l'url avec le bn id mis en parametre
    response = requests.request('GET', f'https://www.gutenberg.org/cache/epub/{args.ID}/pg{args.ID}.txt')
    # on le telecharge en fichier .txt avec comme nom le title du livre
    f = open(f"{result[str(args.ID)]['title']}.txt", "x")
    f.write(response.text)
    f.close()



def clean_data():
    # ici on met en forme si on veut le clean, on remove les espaces et si on met lower alors ca met en lower notre txt
    txt = " ".join(args.clean)
    # si on veut lower on lower
    if args.lower:
        txt = txt.lower()
        # on retire les pesaces et tab inutile
        text = ' '.join(txt.split())
        print(text)
    else:
        # on retire les pesaces et tab inutile
        text = ' '.join(txt.split())
        print(text)



def tokenize_data():
    # iic on gere les tokens
    # on defini notre liste de stopword donc els the etc avec une librairie
    stop_words = stopwords.words("english")
    # on va split tt nos motss dans notre text
    LstToken = " ".join(args.tokenize).split()
    # notre liste qui contient nos infos finales
    LstToken_final = []

    # si on veut sans les stop word
    if args.stop:
        # on parcour tout les mots de notre text
        for mot in LstToken:
            # on verifie qu'on veut ou non la ponctuation
            if args.punct:
                if mot not in string.punctuation:
                    # on verrifie qu'il est pas present dans notre liste de stopword, si c'est le cas on ne l'ajoute pas
                    if mot.lower() not in stop_words:
                        LstToken_final.append(mot)
            else:
                if mot.lower() not in stop_words:
                    LstToken_final.append(mot)

    else:
        # si on ne veut pas retirer les stopword on va quand meme verifier au cas nous ne voulons pas de la ponctuation
        if args.punct:
            for mot in LstToken:
                if mot not in string.punctuation:
                    LstToken_final.append(mot)
        else:
            for mot in LstToken:
                LstToken_final.append(mot)

    # on verifie si on veut sous forme de phrase ou sous forme de liste de mots
    if not args.sent:
        # on print directement notre liste finale ccar on l'a deja split au dessus
        print(LstToken_final)
    else:
        # si on veut en phrase par contre omn va devoir la reconstruire en ajoutant les motds 1 par 1 avec un espace et on retire le dernier espaces comme une vrai phrase
        LstToken = []
        tp = ""
        for element in LstToken_final:
            tp += f"{element} "
        tp = tp[0:len(tp)-1]
        LstToken.append(tp)
        print(LstToken)





def run_postag():
    tokens = " ".join(args.postag).split()
    LstToken_base = []
    LstToken_Finale = []
    for token in tokens:
        LstToken_base.append(token)
            # print(token)
    tagged = nltk.pos_tag(LstToken_base)
    # print(tagged)
    entities = nltk.chunk.ne_chunk(tagged)
    for element in entities:
        LstToken_Finale.append(element)
    print(LstToken_Finale)




def run_normalize():
    # si y a --steam
    if args.stem:
        stemmer = SnowballStemmer("english")
        # on met tout en minuscule
        result = [stemmer.stem(token.lower()) for token in args.normalize]
        print(result)
        
    # sinon on fait la lemmatisation
    else:
        nlp = spacy.load("en_core_web_sm")
        
        # on regroupe pour que spacy comprend le contexte
        doc = nlp(" ".join(args.normalize))
        
        result = []
        for token in doc:
            lemma = token.lemma_
            
            # ici c'est pr garder la majuscule
            if token.text.istitle():
                lemma = lemma.capitalize()
            result.append(lemma)
            
        print(result)






# ici on appelle nos function en fonction de si tel ou tel argument est donne
if args.info:
    get_info()

if args.download:
    download_book()

if args.clean:
    clean_data()

if args.tokenize:
    tokenize_data()

if args.postag:
    run_postag()

if args.normalize:
    run_normalize()