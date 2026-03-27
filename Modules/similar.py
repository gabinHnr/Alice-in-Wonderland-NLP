import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def Upd_relation(Book_Data, Topics_Data):
    """
    Cette fonction permet d'ajouter une nouvelle relation dans notre csv relation

    La fonction prend en parametre les informations du livre ainsi que ss informations sur son topic

    La fonction ne renvoie rien, elle met a jour le fichier relation,csv avec une nouvelle ligne contenant notre nouvelle entree pour le livre actuel
    """
    # on initialise nos data avec nos arguments
    dico_Vectors = Topics_Data[1]
    tt_vecteurs = list(dico_Vectors.values())
    # on fait la moyenne de notre matriuce de vecteur
    vecteur_Livre = np.mean(tt_vecteurs, axis=0)

    # on definie le vecteur du livre
    vBook = vecteur_Livre.reshape(1, -1)


    df = pd.read_csv('cache/relation.csv', sep=';')
    if not df.Book.isin([Book_Data['title']]).any():
        df.loc[len(df)] = {
        'Book': Book_Data['title'],
        'Authors': Book_Data['authors'],
        'Bookshelves': Book_Data['bookshelves'],
        'Vector': vBook,
        'Similar': ''
        }
    else:
        pass
    # Get_Similaire(Book_Data)
    df.to_csv("cache/relation.csv", sep=';', index=False)






def Bookshelves(raw):
    """
    Cette fonction sert a normalize notre Bookshelves, elle va transofmer les ':' en ; et va decouper tout les ';' pour obtenir une liste

    Prend en argument une string

    Renvoie une liste des mots de cette stringf
    """
    L = raw.replace(":", ";").split(";")
    L = [x.strip() for x in L if x.strip()]
    return L




def Get_Similaire(Book_Data, Topics_Data):
    """
    Fonction permettant de recuperer les livres similair au notre, la fonction se base sur un fichier CSV de relation, qui contient plusieurs
    infortmations, tel que l'auteur, le theme des livres, et les vecteur de similitude
    Notre recherche de livre similaire se base sur un pricnipe de pear, si le livre A et B sont similaire et que le livre C et similaire au C,
    alors C est similaire au A.

    Book_Data --> Information sur le livre actuelle, celui qu'on veut etudier
    Topics_Data --> Contient nos Top 10 word (inutile ici) et egalement notre matrice de vecteur
    return --> liste de tout les livres actuellement connu et similaire a notre livre
    """
    df = pd.read_csv('cache/relation.csv', sep=';') # on defini le DF
    df['Similar'] = df['Similar'].astype(object)    

    # on va recuperer notre listre de Bookshelves info propre en liste et sans les category
    Lst_Bookshelves_Book = Book_Data['bookshelves'].replace(":", ";").split(";")
    Lst_Bookshelves_Book = [x.strip() for x in Lst_Bookshelves_Book]
    Lst_Bookshelves_Book = [x for x in Lst_Bookshelves_Book if x != "Category"]

    
    liste_vecteurs = list(Topics_Data[1].values())  # on prend notre liste textuel dans le csv et on la transofmr en vrai liste
    vct_Book = np.mean(liste_vecteurs, axis=0).reshape(1, -1)   # on creer le vecteur moyen du livre
        
    Best_Score = (-1, -1)   # (Index, Score)
    Lst_Similar = []    #  liste de book similaire


    for i in range(len(df)):
        Score = 0   # contient notre score de similitude
        if df.loc[i, "Book"] != Book_Data["title"]:             # on verifie que on ne compare pas notre livre avec sa meme version dans le csv

            # on nettoie le Vector dans le csv car c'est pas une vrai liste c'est un carnage
            chaine_propre = df.loc[i, "Vector"].replace('[', '').replace(']', '').replace('\n', '')
            vct_Cible = np.fromstring(chaine_propre, sep=' ').reshape(1, -1)  # on definie le vecteur de notre livre qu'on vient de prendre du csv

            # on prend les bookshelvdses du livre qu'on vient de prendre
            Lst_Bookshelves_Livre_Actuel = Bookshelves(df.loc[i, "Bookshelves"])
            

            # si meme auteur on rajouter +0.2 de score
            if df.loc[i, "Authors"] == Book_Data["authors"]:
                Score += 0.2
            
            # si on trouve un sujet commun, c'est +0.2 par sujet
            for element in Lst_Bookshelves_Book:
                if element in Lst_Bookshelves_Livre_Actuel:
                    Score += 0.2
            
            # on fait ici notre score de similaritude
            Vecteur_score = cosine_similarity(vct_Book, vct_Cible)[0][0]
            
            # si le score des vecteur est plus haut que 0.85 alors on ajoute +0.8
            if Vecteur_score > 0.85:
                Score += 0.8
                # si entre 0.55 et 0.85 on met +0.3
            elif Vecteur_score > 0.55:
                Score += 0.3
                
            # on modifie le meilleur des score donc le meilleur livre
            if Score > Best_Score[1]:
                Best_Score = (i, Score)
            
            # si le score du livre est au dessus de 1 on considere que c'est un livre similaire donc on l'ajoute
            if Score > 1:
                Lst_Similar.append(df.loc[Best_Score[0], "Book"])
        
        else:
            Index_own = i   # sert a savoir quel est l'index du livre de base




    valeur_actuelle = str(df.loc[Index_own, 'Similar'])     # on prend notre liste de similaire actuelle pour le livre
    amis_existants_base = [] if valeur_actuelle == 'nan' or valeur_actuelle == "" else valeur_actuelle.split(',')   # on faire en sorte que si y a aucune valeur alors on initialise une liste vide (on verifi si c'est Nan ou "" car ca bug)

    
    titre_actuel = Book_Data["title"]
    groupe_new = list(set([titre_actuel] + amis_existants_base + Lst_Similar))  # on defini notre nouveau groupe similaire, avec les anciens, les nouveaux et le titre de celui actuel
    groupe_new = [x for x in groupe_new if x.strip() != ""]

    # on va basculer dans chaque livre du groupe
    for titre in groupe_new:
        idx = df[df['Book'] == titre].index # on prened l'index d'un livre du grp
        
        if not idx.empty:
            i = idx[0]
            
            # on fait pareil que au dessu, on va chercher ses livres existant et on gere si y a rien
            val = str(df.loc[i, 'Similar'])
            ses_amis_avant = [] if val == 'nan' or val == "" else val.split(',')
            
            # on va ajouter tout nos livre dans les autres livre
            tous_ses_amis = list(set(ses_amis_avant + groupe_new))
            
            # on retire le nom du propre livre c'est completement debile sinon
            if titre in tous_ses_amis:
                tous_ses_amis.remove(titre)
            
            # on va joindre notre nouvelle liste
            df.loc[i, 'Similar'] = ",".join(tous_ses_amis)

    # on save
    df.to_csv("cache/relation.csv", sep=';', index=False)


    print(f"Meilleur score trouvé : {Best_Score[1]} (Index: {Best_Score[0]})")
    print(df.loc[i, "Similar"])
    return df.loc[i, "Similar"]

