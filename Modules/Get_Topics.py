import nltk
import string
from nltk.corpus import stopwords



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
    Get_main_Topic(lst_word)
    return(lst_word)


def Get_main_Topic(Lst_word):
    import spacy
    from sklearn.cluster import KMeans




    # nlp = spacy.load("fr_core_news_md")

    # words = Lst_word

    # vectors = [nlp(w).vector for w in words]

    # kmeans = KMeans(n_clusters=2)
    # labels = kmeans.fit_predict(vectors)

    # for w, l in zip(words, labels):
    #     print(w, "→ cluster", l)
