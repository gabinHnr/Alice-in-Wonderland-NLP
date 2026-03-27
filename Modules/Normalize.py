from nltk.stem import SnowballStemmer
import spacy

def run_normalize(Text, isSteam=False):
    """
    Fonction qui sert a normalize notre text, nous allons donc rendre conforme notre text

    Prend en argument un texte ainsi qu'in parametre optionnel isSteam qui est un autre mode de normalization
    /!\ A noter que isSteam consome beaocup plus de ressource, attention lors de son utilisation /!\
    
    La fonction renvoie le meme texte qu'en parametre mais normalize
    """
    # si y a --steam
    if isSteam == True:
        stemmer = SnowballStemmer("english")
        # on met tout en minuscule
        result = [stemmer.stem(token.lower()) for token in Text]
        return(result)
        
    # sinon on fait la lemmatisation
    else:
        nlp = spacy.load("en_core_web_sm")
        
        # on regroupe pour que spacy comprend le contexte
        doc = nlp(" ".join(Text))
        
        result = []
        for token in doc:
            lemma = token.lemma_
            
            # ici c'est pr garder la majuscule
            if token.text.istitle():
                lemma = lemma.capitalize()
            result.append(lemma)
            
        return(result)
