# Réflexion sur les choix effectués durant le projet

## Ce fichier va contenir notre réflexion par rapport aux choix effectués tout au long du projet.

Pour ce projet, nous avons mis l'accent sur l'optimisation et le temps d'exécution. Du début à la fin, nous avons choisi les technologies les moins lourdes et coûteuses pour faire exécuter nos différentes commandes.

### Tokenization

Pour tokenizer nos textes, nous sommes partis sur NLTK, un modèle très léger, moins performant et plus vieillissant mais tout à fait capable de tokenizer correctement nos textes de façon efficace. D'autres pistes comme Spacy avaient été explorées, mais la différence étant minime, nous avons gardé un temps d'exécution et de mémoire RAM plus court.

### POSTag

Pour les posttag, un problème s'est posé. Nous avions réalisé le postag avec NLTK : cela marche, mais malheureusement NLTK étant vieillissant, nous n'avions pas la reconnaissance de certains mots ajoutés récemment ou il y a quelques années, et une précision beaucoup trop approximative pour être viable.
Nous avons donc changé notre modèle pour utiliser Spacy, plus lourd mais toujours raisonnable. Cela nous permet d'avoir plus d'informations et de qualité, ce qui est nécessaire pour la suite.

### Normalisation

Pour normaliser nos textes, nous avons fait face au même problème : NLTK était peu viable quand l'option isSteam n'était pas demandée. Nous avons donc mixé : lorsque isSteam n'est pas demandé, nous utilisons Spacy, et lorsque nous voulons utiliser isSteam, nous utilisons NLTK.
Avec ce combo, les performances sont les plus minimales selon les cas de figure rencontrés.

### Topics

Maintenant nous allons rentrer dans le plus dur : les topics.
Pour les topics, nous avons opté pour un mix des deux. Pour la partie des top 10 des mots les plus présents, nous utilisons NLTK qui fait très bien le travail. Mais pour la partie des vecteurs, nous utilisons NLTK couplé avec NumPy pour obtenir une matrice de vecteurs. Nous verrons par la suite pourquoi nous voulons des vecteurs.


### Entities

Entities sert à trouver les personnages du livre ainsi que les localisations. C'est la partie la moins précise de notre projet. Par manque de temps mais également par choix, nous n'avons pas pu la rendre la plus précise possible. Pour la rendre extrêmement précise, cela demande une quantité de ressources absurde et non conforme à notre projet.

Pour améliorer son rendu, nous aurions pu faire un nettoyage "manuel" qui permettrait de retirer les aberrances qui ressortent dans plusieurs livres.

Pour entités, nous utilisons Spacy avec notamment `run_spacy_pipeline` pour régler le problème d'espace. Nous passons un à un nos chapitres et nous utilisons d'autres fonctions citées précédemment.

À noter que cette fonction est présente dans le fichier `bookeworm.py` et non dans un fichier séparé dans module pour plus de simplicité et à la demande d'un membre pédagogique.

### Similar

Pour continuer, nous allons voir similar. Similar étant l'une des deux fonctions les plus dures lors de ce projet. Il nous était demandé de ne réaliser les similar que pour 21 livres donnés. Nous trouvions cela dommage, nous sommes donc partis dans l'optique de pouvoir prendre le plus de livres possible.

Pour cela, nous avons créé un CSV qui fait office de table de référencement intelligente. Chaque ligne du CSV contient l'auteur, le livre, les thèmes de l'auteur et du livre concerné, ainsi qu'une matrice de vecteurs correspondant à un score, ainsi qu'une liste de livres similaires.

Nous nous sommes basés sur un principe de pair assez simple : si le livre A est similaire au livre B, alors si un livre C est similaire au livre A, alors C sera similaire au livre B.
Avec ce principe, nous n'avons pas besoin de parcourir tous nos livres. Nous utilisons une table de relation qui va se créer toute seule au fur et à mesure de l'utilisation de notre programme. À chaque nouveau livre, le programme va comparer les auteurs : s'ils sont identiques, il y a plus de chances d'être similaire ; les thèmes abordés ; et si la moyenne de la matrice est haute. Si la moyenne est > 0.85, alors le livre a de fortes chances d'être similaire, et on peut définir un score et mettre à jour toutes les relations où ce livre va être similaire.

L'exécution de similar n'est pas plus longue : elle est identique voire plus rapide que d'autres versions et permet d'être beaucoup plus efficace.
Pour cela, nous utilisons donc Pandas, Spacy et Sklearn principalement pour les vecteurs.

### Summary

La fonction summary est l'autre fonction la plus dure de ce projet. Nous voulions quelque chose de précis ou du moins qui renvoyait un résumé digne de ce nom. Il nous a fallu passé une bonne partie du projet pour réussir à avoir un modèle satisfaisant mais très lourd. Nous avons donc choisi de laisser le choix à l'utilisateur parmi le plus simple et rapide ou le plus précis mais plus lent.

Le summary plus rapide et moins précis se sert des 10 mots les plus présent dans le livre. Celui-ci sélectionne par la suite les phrases avec le score le plus élevé pour pouvoir faire un résumé. 

Le summary plus lours lui ce sert d'un modèle, qui permet, via de la tokenization, de faire un résumé beaucoup plus poussé.

### Card

Enfin la fonction Card permet elle de faire une synthèse de toutes les autres fonction , du moins tous les rassembler en un grand dictionnaire pour avoir toutes les informations d'un livre en un seul point qui est facile de compréhension.

Cette fonction permet aussi de faciliter la création de métadata.

## Cache et découpage

Pour tout notre projet, nous travaillons avec un cache : un dossier qui va sauvegarder des informations pour permettre une exécution plus rapide. Nous avons designé intelligemment notre cache : il contient un dossier pour chaque livre exécuté.
Dedans, nous trouvons une copie du livre téléchargé depuis internet, une liste des tokens du livre, ainsi que tous les chapitres découpés en fichiers et la card générée.

Nous avons donc dû designer une fonction de découpage qui gère le plus de cas possible pour couper tous les chapitres, car aucun n'est identique : certains ont des numéros romains, d'autres latins, d'autres aucun, etc.

## Streamlit

A la fin de notre projet, nous nous sommes vite rendu compte que malgré cette fonction Card, visualisé les élément était plutôt fastidieux. Nous avons donc décider de faire un streamlit interactif permettant de choisir un livre et d'avoir les informations claires de chaque fonction directement affiché sur l'écran de manière structurée et permettant une plus simple compréhension.

