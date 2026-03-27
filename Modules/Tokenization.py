from nltk.corpus import stopwords
import string


def tokenize_data(Text, stop=False, punct=False, sent=False):
    """
    Cette fonction va servir pour tokenize nos texte, elle va prendre en argument un texte et le decouper en une lioste avec diferentes
    methode pour etre plius facilement conforme

    Prend en argument:
    Text --> un texte ne format str
    stop --> argument optionnel qui permet de retirer les stopwords
    punct --> argument optionnel qui permet de retirer les punctuation
    sent --> argument otpionnel, permnet de tokenizer avec des phrases et non des mots


    return --> une liste de token qui correspond a notre text
    """
    if punct:
        Text = Text.translate(str.maketrans('', '', string.punctuation))


    # ici on gere les tokens
    # on defini notre liste de stopword donc els the etc avec une librairie
    stop_words = stopwords.words("english")
    # on va split tt nos motss dans notre text
    LstToken = Text.split()
    # notre liste qui contient nos infos finales
    LstToken_final = []

    # si on veut sans les stop word
    if stop == True:
        # on parcour tout les mots de notre text
        for mot in LstToken:
            # on verifie qu'on veut ou non la ponctuation
            if punct == True:
                if mot not in string.punctuation:
                    # on verrifie qu'il est pas present dans notre liste de stopword, si c'est le cas on ne l'ajoute pas
                    if mot.lower() not in stop_words:
                        LstToken_final.append(mot)
            else:
                if mot.lower() not in stop_words:
                    LstToken_final.append(mot)

    else:
        # si on ne veut pas retirer les stopword on va quand meme verifier au cas nous ne voulons pas de la ponctuation
        if punct == True:
            for mot in LstToken:
                if mot not in string.punctuation:
                    LstToken_final.append(mot)
        else:
            for mot in LstToken:
                LstToken_final.append(mot)

    # on verifie si on veut sous forme de phrase ou sous forme de liste de mots
    if sent == False:
        # on print directement notre liste finale ccar on l'a deja split au dessus
        return(LstToken_final)
    else:
        # si on veut en phrase par contre omn va devoir la reconstruire en ajoutant les motds 1 par 1 avec un espace et on retire le dernier espaces comme une vrai phrase
        LstToken = []
        tp = ""
        for element in LstToken_final:
            tp += f"{element} "
        tp = tp[0:len(tp)-1]
        LstToken.append(tp)
        return(LstToken)