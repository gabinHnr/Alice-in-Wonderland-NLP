def decoupage(file_name):
    with open(file_name, "r", encoding="utf-8") as book: # on ouvre le fichier text entier
        text_brut = book.read()

    ligne = text_brut.splitlines()  # on le separe en ligne
    print(Get_Content(text_brut))
    Marker = "chapter " # on cherche les chapter
    # MarkerEnd = "the end"
    # Add_File_Chapter(file_name, 5)
    compteur = 0        # compteur pour connaitre le chapitre em cours
    lst_ligne= []
    mot_flagg = "IVXLCDM"
    for i, line in enumerate(ligne):        # on va verifier dans chaque ligne 
        clean = line.strip()
        if len(clean) != 0 and len(clean) < 10 and all(c in "IVXLCDM" for c in clean):
            Add_File_Chapter(file_name, compteur, lst_ligne)
            compteur+=1
            lst_ligne = []

        elif Marker in line.lower():
            # print(repr(line))    # pour verifier a quoi ressembler vrqaiment une ligne
            if clean.count(" ") < 2:
                Add_File_Chapter(file_name, compteur, lst_ligne)
                compteur+=1
                lst_ligne = []
        lst_ligne.append(line)
    Add_File_Chapter(file_name, compteur, lst_ligne)


def Add_File_Chapter(file_name, Numero, text):
    # on remove le dernier element du file_name
    file_name = file_name[:file_name.rfind("/")]
    file_name = f"{file_name}/Chapter_{Numero}.txt"
    with open(file_name, "w", encoding="utf-8") as livre:
        # text = str(text)
        text = "\n".join(text)
        livre.write(text)


def Get_Content(lines):
    marker = "Contents"
    collecting = False
    contents = []
    print(type(lines))
    for line in lines:
        if marker in line:
            collecting = True
            print("oui")
            continue


        if collecting and line.strip() == "":
            break


        if collecting:
            contents.append(line)

    return contents



# decoupage("../cache/Moby-Dick; or, The Whale/Moby-Dick; or, The Whale.txt")