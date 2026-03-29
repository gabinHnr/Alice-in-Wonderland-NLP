# import nltk

# def run_postag(All_token):
#     tokens = All_token
#     # tokens = " ".join(All_token).split()
#     LstToken_base = []
#     LstToken_Finale = []
#     for token in tokens:
#         LstToken_base.append(token)
#             # print(token)
#     tagged = nltk.pos_tag(LstToken_base)
#     # print(tagged)
#     entities = nltk.chunk.ne_chunk(tagged)
#     for element in entities:
#         LstToken_Finale.append(element)
#     return(LstToken_Finale)

import spacy


nlp = spacy.load("en_core_web_sm")

def run_spacy_pipeline(text_brut):
    """
    Cette fonction va avoir pour but de definir les tag des mot d'un text, par exemple si un mot est une localisation, si c'est une personne, ...

    Prend en parametre un texte non normalize

    Return une liste avec le mot, sa nature (aj, verbe, ...) ainsi que son type donc si c'est une localisation, un prenom, etc
    """
    # text = " ".join(tokens)
    doc = nlp(text_brut)
    liste_taggee = [(token.text, token.ent_type_, token.pos_) for token in doc]
    return liste_taggee