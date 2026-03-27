import nltk
import string
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("fr_core_news_md")
stop_words = stopwords.words("english")

def Get_topics(File):
    lst_word = []
    with open(File, "r", encoding="utf-8") as book:
        text_brut = book.read()
    
    text_brut = text_brut.split()

    

    remove = str.maketrans("", "", string.punctuation)
    nettoyee = [s.translate(remove) for s in text_brut]
    nettoyee = [s.replace("  ", "") for s in nettoyee]
    tp = []
    for s in nettoyee:
        if s.lower() not in stop_words:
            if '“' not in s and "—" not in s and len(s) > 2 and s != "CHAPTER":
                tp.append(s)

    frequence = nltk.FreqDist(tp)
    [lst_word.append(mots) for mots in frequence.most_common(10)]
    
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