


def decoupage(file_name):
    with open(file_name, "r", encoding="utf-8") as book: # on ouvre le fichier text entier
        text_brut = book.read()
    
    ligne = text_brut.splitlines()  # on le separe en ligne
    Marker = "CHAPTER " # on cherche les chapter
    MarkerEnd = "THE END"
    # Add_File_Chapter(file_name, 5)
    compteur = 0        # compteur pour connaitre le chapitre em cours
    lst_ligne= []
    for i, line in enumerate(ligne):        # on va verifier dans chaque ligne 
        print(line)
        clean = line.strip()
        if Marker in line or MarkerEnd in line:
            # print(repr(line))    # pour verifier a quoi ressembler vrqaiment une ligne
            if clean.count(" ") < 2:
                Add_File_Chapter(file_name, compteur, lst_ligne)
                compteur+=1
                lst_ligne = []
        lst_ligne.append(line)        




def Add_File_Chapter(file_name, Numero, text):
    # on remove le dernier element du file_name
    file_name = file_name[:file_name.rfind("/")]
    file_name = f"{file_name}/Chapter_{Numero}.txt"
    with open(file_name, "w", encoding="utf-8") as livre:
        # text = str(text)
        text = "\n".join(text)
        livre.write(text)





# decoupage("../cache/Moby-Dick; or, The Whale/Moby-Dick; or, The Whale.txt")