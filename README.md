# Alice's Adventures In Wonderland

## Préambule

Le projet Alice's Adventures In Wonderland est un projet DATA, avec pour objectif de pouvoir récupérer les informations de livres via leur identifiant et leur contenu

Notre but est donc de récupérer, extraire et synthétiser les données d’un livre du projet Gutemberg, afin de construire des "cartes de livres" permettant d'avoir toutes les informations synthétisées en rapport avec ces dit-livres comme un rapide résumé, les différents personnages et lieux ou encore le thème du livre.

## Installer notre projet

Pour pouvoir utiliser notre projet, il faut d’abord savoir comment l’initialiser correctement.

Après avoir récupéré tous les fichiers de ce répertoire, ouvrez un terminal et placez-vous à la racine du projet.

Exécutez ensuite les commandes suivantes :

    python3 -m venv Myvenv
    source Myvenv/bin/activate
    pip install -r requirements.txt
    mkdir cache

Le fichier requirements.txt contient toutes les dépendances nécessaires au projet.

Si cette étape se déroule correctement, alors le projet est initialisé et prêt à être utilisé.

## Arborescence requise

Pour utiliser notre projet, il vous faut une arborescence spéciale afin de le faire fonctionner correctement. 
(À noter que cette arborescence est basée sur notre fichier `.gitignore` et peut être modifiée par vous-même.)

```
AliceinWonderland/
├── cache/
│   └── ... (fichiers relatifs aux livres)
│
├── Modules/
│   └── ... (Préprocessing des textes)
│
├── bookworm.py
├── pg_catalog.csv
```

## Utiliser notre projet

Pour pouvoir utiliser notre projet, ce n'est pas très compliqué. Il y a 6 éléments distinct permettant d'avoir différentes informations:

- --lexdiv permet de recuperer diverses informations issues de notre livres choisis comme le nombre de mots unique ou qui n'apparaissent qu'une seule fois.

- --topics permet d'avoir les 10 mots les plus utilisés dans chaques chapitres afin de comprendre le thème de chacun

- --entities sert à récupérer tous les personnages et lieux du livres

- --summary renvoie un court résumé du livre choisi. 

- --similar permet de trouver des livres similaires au livre que l'on a cherché.

- --card, ce dernier élément permet de faire un synthèse des précédent, et de créer une carte afin d'avoir toutes les informations regroupées en un seul endroit, afin d'avoir simplement tous ce que l'on recherche.

Pour utiliser ces différents élément, rien de plus simple il suffit d'executer cette commande

    python bookworm.py "--element" "ID du livre"

Exemple pour avoir le résumé du livre <u>"Alice au pays des merveilles"</u> qui porte l'ID 11 on fait : 

    python bookworm.py --summary 11

    >> Alice fell down the Rabbit-Hole after a White Rabbit with pink eyes . Alice tried to get out of a dark hall, but the locks were too large, or the key was too small . She came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key . She tried the little golden key in the lock, and to her great delight it fitted! Alice opened the door and found that it led into a small passage, not much . Alice’s Right Foot, Esq., near the Fender, is about to give her own feet a new pair of boots every Christmas

Mais on peu aussi le faire via un streamlit, un dashboard interactif !

Il vous suffit pour cela de faire la commande suivante :
```
streamlit run streamlit.py
```

Cela devrais vous ouvir une page internet avec comme URL :
```
http://localhost:8501
```

Sinon, il vous suffit de taper cette même URL dans votre navigateur, ou de faire "ctrl" + "click" sur cette URL présente dans votre terminal.

Une fois arrivé sur le streamlit, vous aurais une barre de recherche. Il vous suffit de taper le nom d'un livre ou simplement le début et de faire entrée pour avoir toutes les informations de ce livre.

``` 
"Alice's adventures in Wonderland" peut être recherché en tapant exactement son nom dans la barre de recherche, ou simplement en écrivant "Alice" dans celle-ci.
```

Vosu avez aussi le choix sur le choix du modèle de summary utilisé. si vous cocher la case modèle large. Le temps de chargement sera un peu plus lent mais vous permettra d'avoir un meilleur résumé du livre.