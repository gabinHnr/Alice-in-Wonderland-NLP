import re
import os

def decoupage(file_name): 
    """
    Cette fonction sert de decoupage pour n'importe quel livre du projet Gutemberg, elle permet de separer chaque texte en plusieurs fichier chacun,
    reprensentant un chapitre du livre en question.

    (Cette fonction a ete code avec une base de 45 livre, elle peut ne pas etre entierement fonctionnel pour les 75000 livres)

    Cette fonction prend en parametre un fichier .txt, celui du livre complet
    decoupage est dependante d'une autre fonction ``Get_Content`` ainsi que ``Add_File_Chapter``

    return --> Le return sont desa fichiers place dans le dossier cache et dans le sous dossier du livre correspondant, un chapitre 0 est cree et contient
    les informations comme la prephase, certains liens entre personnages, le sommaire, ... Ttout ce qui ne touche pas directement a l'histoire meme
    """
    with open(file_name, "r", encoding="utf-8") as book:
        text_brut = book.read()

    ligne = text_brut.splitlines()
    All_content = Get_Content(ligne)    # on va chercher le contenu de notre content
    fin_sommaire_id = All_content[1]    # on prend l'id finale du content, c'est a la ligne d'apres que l'histoire va debuter
    Contenu_sommaire = [titre.lower() for titre in All_content[0]]  # on prend les element du content
    


    compteur = 0
    lst_ligne = []
    
    # Ttout nos Regex, nerd de la guerre ici, permet de detecter differents paterns pour les chapitres
    
    # explication:
    """
    re.IGNORECASE --> permet d'ignore majuscule ou minuscule
    re.compile --> permet d'avoir la regle en une ois et c'est plus rapide et opti
    r'' --> permet d'avoir la ligne comme on la voit et sans les \n etc
    ^ --> permet de verifier que c'est bien le premier element de la ligne
    ce qui suit le chapeau c'est ce qu'on cehrche comme par exemple chapter
    \s --> permet de prendre n'importe quel espace donc va pouvoir avoir Chapter 1 ou bien Chapter  1, etc
    le () avec des numeros etc c'est pour detecter ensuite si il y a bie un chiffre latin ou romain
    | --> = ou
    \.? --> permet d'accepter si il y a un `.` ou non a la fin, donc chapter 1. est valide mais chapter 1 l'est aussi
    """
    chapter_pattern = re.compile(r'^chapter\s+([0-9]+|[ivxlcdm]+)\.?', re.IGNORECASE)
    roman_pattern = re.compile(r'^([ivxlcdm]+)\.$', re.IGNORECASE)
    book_pattern = re.compile(r'^book\s+([a-z]+|[ivxlcdm]+)$', re.IGNORECASE)

    # on va basculer dans chaque ligne de notre texte
    for i, line in enumerate(ligne):
        clean = line.strip()    
        clean = line.strip(" \t\n\r_*")     # uniquement pour le livre Call of Cthullhu car c'est embetant
        
        # on recherche des chapitres unioquement apres la fin du sommaire
        if i > fin_sommaire_id:
            
            is_new_chapter = False
            
            # si notre ligne clean matche avec le regex du chapitre alors on cut
            if chapter_pattern.match(clean):
                is_new_chapter = True
            
            # permet ici de verifier si on a pas uniquemnt un chiffre sur la ligne, dans certain lire c'est = a un nouveau chaputre qui commence
            elif re.match(r'^(\d+)\.', clean):
                is_new_chapter = True
                
            # si notre ligne clean matche avec le regex du romain alors on cut
            elif roman_pattern.match(clean):
                is_new_chapter = True
                
            # si notre ligne clean matche avec le regex du book alors on cut
            elif book_pattern.match(clean):
                is_new_chapter = True
                
            # on verifie car certain livre comme (Docteur Moreau) ont ca au debut
            elif clean.upper() == "INTRODUCTION.":
                is_new_chapter = True

            # on verifie que clean est present ou non dans le content
            elif clean.lower() in Contenu_sommaire and 0 < len(clean) < 60:
                is_new_chapter = True

            # Si on a un nouveau chaputre et que le contenu entre celui d'avant et mainteant n'est pas nul alors on va crrrer un nouveau fichier
            if is_new_chapter and len(lst_ligne) > 0:
                Add_File_Chapter(file_name, compteur, lst_ligne)
                compteur += 1
                lst_ligne = []

        # on ajoute la ligne actuelle
        lst_ligne.append(line)
        
    # une fois a la fin comme certain livre n'ont pas de End ont va simplement creer un dernier fichier depuis la derniere du chaputre precedent jusqu'a la fin
    if len(lst_ligne) > 0:
        Add_File_Chapter(file_name, compteur, lst_ligne)
        

def Add_File_Chapter(file_name, Numero, text):
    """
    Fonction qui permet de creer un fichier directement dans le bon emplacement selon le livre
    Prend en parametre le nom du fichier, le numero actuelle ainsi que le text a mettre dans ce fichier

    return --> un fichier avec le nom CHaputre_ suivi du numero actuel
    """
    # on va prendre le dossier
    dossier = os.path.dirname(file_name)
    if dossier == "": # petite safety pour verifier qu'on est bien au bon endroit
        dossier = "."

    # nouveau nom du chapitre
    name_chapter = os.path.join(dossier, f"Chapter_{Numero}.txt")
    
    with open(name_chapter, "w", encoding="utf-8") as livre:
        livre.write("\n".join(text))


def Get_Content(lines):
    """
    Fonction permettant de recuperer le contenu du content d'un livre, certains livre ne disponsent pas d'element generique pour connaitre le debut d'un 
    chapitre, nous allons alors recuperer le content du livre qui contient toute les parties du livre

    Prend en argument notre texte brut split, donc une liste des lignes du text
    return --> une liste des contenu du content ainsi que le dernier ID du content
    """
    # on initialise nos variable
    marker = "contents"
    collecting = False
    started = False 
    contents = []
    dernier_id = 0
    empty_lines_count = 0

    # on bascule dans chaque lignes du line
    for i, line in enumerate(lines):
        clean = line.strip().lstrip("\ufeff")   # on netoie pour retirer les choss non conforme
        
        # on va verifier si notre ligne est = a contents ou alors table of contents selon les livres
        if clean.lower() == marker or clean.lower() == "table of contents":
            collecting = True
            continue
        
        # si on est entrain de collecter nos lignes alors on va ajouter la ligne et si on a + de 3 lignes vide entre deux ca veut dire qu'on est a la fin
        if collecting:
            if clean == "":
                empty_lines_count += 1
                if started and empty_lines_count >= 3:
                    dernier_id = i
                    break
            else:
                contents.append(clean)
                started = True
                empty_lines_count = 0

    return [contents, dernier_id]