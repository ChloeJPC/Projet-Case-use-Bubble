# ALAO-projet : Case-use Bubble

Projet en binôme pour les cours de TAL&ALAO et Java.
Chloé Choquet et Pauline Mas (M2 IDL)

## Application pour l'apprentissage de la langue allemande ##
La visée, le fonctionnement et les limites des modules développés dans le cadre de ce projet sont détaillés sur un wiki séparés : *(adresse à venir)*.

### Arborescence du projet ###

Afin que l'application fonctionne, il faut télécharger localement les éléments suivants:
- le dossier **appBubulle** (qui correspond à l'application)
- le dossier **bubullePro** (nom donné au projet global)
- le dossier **static** (qui contient notammet la mise en page CSS et les scripts)
- le dossier **templates** (qui contient les fichiers HTML)
- *manage.py* (fichier nécessaire pour la gestion du site)
- *db.sqlite3*

### Étapes d'installation ###
Cette application nécessite d’avoir Python installé sur la machine utilisée, de préférence Python 3. Effectuez les opérations suivantes dans votre terminal :
1. Installer pipenv sous python 3 avec la commande : `pip install pipenv` ou  `python -m pip install pipenv`
2. Se placer dans un dossier en local (à l’aide de `cd [cheminDossier]`)
3. Installer un environnement virtuel dans ledit dossier avec `pipenv shell` ou `python -m pipenv shell`
4. Entrer dans l’environnement créé si l’on ne s’y trouve pas déjà (même commande que pour l’installation)
5. Installer Django (version 3.2.9 utilisée dans ce projet) : `pip install Django`
6. Installer Spacy (de préférence la version 3.2.0) : `pip install -U spacy `
7. Importer le modèle de langue dédié à l’allemand : `python -m spacy download de_core_news_md`
8. Importer l’arborescence décrite ci-dessus

### Étapes de lancement ###
1. Se placer dans le dossier local à l’origine de l’arborescence du projet
2. Lancer l’environnement virtuel ( `python -m pipenv shell` )
3. Lancer le serveur django : `py manage.py runserver` ou `python manage.py runserver`
4. Ouvrir son navigateur à l’adresse http://127.0.0.1:8000/

### Le contenu spécifique au projet ###
Parmis les nombreux fichiers rassemblés sur ce projet Gitlab, voici ceux qui sur lesquels nos efforts se sont concentrés:
- *source_vb_speciaux.py* (dans le dossier **_Pretraitement-ressource**);
- *views.py* (dans le dossier **appBubulle**) : fonctions appelées à partir du site ;
- *urls.py* (dans le dossier **bubullePro**) : gestion de l’accès aux différentes pages et fonctions depuis le site ;
- *app-style.css* (dans le dossier **static/styles**) : esthétique spécifique au site ;
- *home.js*, *text-to-cat.js* et *Ex-a-trou.js* (dans le dossier **static/scripts**) : gestion des interactions entre le site, l’utilisateur et les fonctions python ;
- l’ensemble des fichiers HTML du dossier **templates** : mise en forme du site.

*source_vb_speciaux.py* est un court module python qui a été utilisé pour extraire des listes de verbes au format TXT à partir d’une source externe plus élaborée. Les tests et autres ajustements ont été réalisés par l’intermédiaire de fichiers python indépendants que sont *analyse_ttc_brouillon.py*, *exo_liste_der_brouillon.py* et *text_spacy_de.py*. Ces fichiers n’interviennent en aucun cas dans le fonctionnement du produit final.

Enfin, *vb_dat.txt*,*corpus.csv*, *det.csv* et *pron.csv* (dans le dossier **static**) sont des ressources que nous avons mises en forme et qui sont exploitées dans les fonctions de *views.py*.

### Ajouter des textes dans le corpus ###
Pour ajouter un texte dans l’exercice de texte à trous, il faut tout d’abord ouvrir le fichier *corpus.csv*. Pour une meilleure gestion du fichier, nous vous conseillons de l’ouvrir dans un tableur. Si vous ouvrez ce fichier dans un éditeur de texte, le symbole de séparation entre les colonnes est la tabulation.
Chaque ligne du fichier correspond à un texte. Si vous souhaitez écrire des commentaire dans le fichier, il est nécessaire de débuter la ligne pas un dièse (symbole `#`).
Un texte est représenté par 4 éléments :
- La première colonne correspond au titre du texte, qui sera affiché lors de l’exercice.
- La deuxième colonne correspond au niveau du texte, du cadre européen de référence pour les langues (CECRL). Attention, seuls les niveaux “A1”, “A2”, “B1” ou “B2” sont acceptés par le programme. Si vous entrez une autre valeur que les quatre susnommées, le texte ne sera pas pris en compte dans l'activité.
- La troisième colonne correspond à la source du texte. Elle n’est pas utilisée par le programme.
- La quatrième colonne correspond au contenu du texte. Le contenu entier du texte doit être contenu dans cette unique case, en aucun cas il ne doit être contenu sur deux lignes ou plus.

### Note concernant les fonctionnalités du site ###

L'outil de recherche interne à la barre de navigation ainsi que le formulaire de la page d'accueil du site ne sont actuellement pas fonctionnels. Le développement web n'étant pas en focus dans le cadre du projet, ces éléments n'ont qu'une visée purement esthétique au sein de la maquette réalisée. 
