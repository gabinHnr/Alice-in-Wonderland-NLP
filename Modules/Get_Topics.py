import nltk
import string
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("fr_core_news_md")
stop_words = stopwords.words("english")



def Get_topics(File):
    """
    Fonction qui permet de recuperer pour chaque chapitre d'un livre son top 10 des mots les plus presents, pour cela on se base sur nltk avec frqdist,
    la fonction se charge egalement de fournir les vecteurs qui serviront pour trouver des livres similaire plus tard

    La fonction prend en argument un fichier (en locurence un chapitre d'un livre)

    Le return --> la liste des top 10 ddes frquence de mot dans ;e chapitre ainsi que les vecteurs de ce chapitre
    """
    # on ouvrre le fichier
    lst_word = []
    with open(File, "r", encoding="utf-8") as book:
        text_brut = book.read()
    
    text_brut = text_brut.split()

    
    # on retire les ponctuation, les pesaces inutile, ...
    remove = str.maketrans("", "", string.punctuation)
    nettoyee = [s.translate(remove) for s in text_brut]
    nettoyee = [s.replace("  ", "") for s in nettoyee]
    
    tp = []
    # on va basculer dans chaque ligne et verifier que on a pas de - si de " ou de mot CHAPTER et on ajoute a notre liste
    for s in nettoyee:
        if s.lower() not in stop_words:
            if '“' not in s and "—" not in s and len(s) > 2 and s != "CHAPTER":
                tp.append(s)

    # on calcule la frquence et on l'ajoute a notre liste
    frequence = nltk.FreqDist(tp)
    [lst_word.append(mots) for mots in frequence.most_common(10)]
    
    # on return nos infos
    return(lst_word, get_book_vector(lst_word, nlp))



import numpy as np

def get_book_vector(lst_word, nlp):
    """
    Cette fonction va generer une matrice (donc une liste de liste) avec les differents vecteurs de nos top 10 word pour chaque chapitre,
    cela va permettre de definir un vecteur generale pour comparer un livre A avec un livre B
    """
    vectors = [nlp(w[0]).vector for w in lst_word if nlp(w[0]).has_vector]
    
    if not vectors:
        return None
    

    book_vector = np.mean(vectors, axis=0)
    return(book_vector)