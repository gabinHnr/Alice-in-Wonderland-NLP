def decoupage(file_name):
    with open(file_name, "r", encoding="utf-8") as book: # on ouvre le fichier text entier
        text_brut = book.read()

    ligne = text_brut.splitlines()  # on le separe en ligne
    All_content = Get_Content(ligne)
    Lst_other_stop = All_content[0]

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


        for ele in Lst_other_stop:
            # tp = line.strip()
            tp = " ".join(line.split())
            eleCLear = " ".join(ele.split())
            if tp.lower() == eleCLear.lower():
                print(tp.lower(), eleCLear.lower())
                if i > All_content[1]:
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
    marker = "contents"
    collecting = False
    started = False 
    contents = []
    dernier_id = 0

    for i, line in enumerate(lines):
        clean = line.strip().lstrip("\ufeff")
        # print(clean)
        if clean.lower() == marker:
            print("debug1")
            collecting = True
            continue

        if collecting and not started and clean == "":
            print("debug continue")
            continue

        if collecting and started and clean == "":
            dernier_id = i
            print("debug end")
            break

 
        if collecting:
            contents.append(clean)
            started = True
    print("prijnt finale", contents)
    return [contents, dernier_id]
