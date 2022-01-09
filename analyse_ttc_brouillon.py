# Prérequis du brouillon
import spacy
nlp = spacy.load("de_core_news_md")
output = nlp("Zwei Königssöhne gingen einmal auf Abenteuersuche und gerieten in ein wildes, wüstes Leben, so dass sie gar nicht wieder nach Haus kamen. Der jüngste, welcher der Dummling hieß, machte sich auf und suchte seine Brüder. Aber als er sie endlich fand, verspotteten sie ihn, weil er mit seiner Einfalt sich durch die Welt schlagen wolle. Aber zu zweit könnten auch sie nicht durchkommen, obwohl sie doch viel klüger seien. So zogen sie alle drei miteinander fort und kamen an einen Ameisenhaufen.")
#output = nlp("Ich habe es mir gewünscht, aber mein Bruder hat den fahrrad meiner Mutter genommen.")
Doc_nlp = []
for token in output:
        # Construction de la structure retournée
        children = []                       # initialisation de la liste des dépendants du token
        if len(list(token.children)) > 0 :
            # construction de la liste d'indices des dépendants syntaxiques de chaque token
            for child in token.children:
                children.append(child.i)
        Doc_nlp.append({"text":token.text, "pos":token.pos_, "case":token.morph.get('Case'), "gender":token.morph.get('Gender'), "number":token.morph.get('Number'), "dep":token.dep_, "head_lemma":token.head.lemma_, "head_pos":token.head.pos_, "head_id":token.head.i, "children":children})

# Partie modifiée
#-----------------

# Sous-fonctions globales
def importFile(name):
    """Fonction d'importation de ressources textuelles avec un élément par ligne.
    Retourne une liste dont chaque cellule correspond à une ligne du fichier d'origine."""
    fileSource = open(name, encoding="utf8", mode='r')  # lecture du fichier renseigné
    contentFile = fileSource.readlines()                # récupération du contenu textuel
    liste = [ line.strip("\n") for line in contentFile] # division du contenu et insertion dans une liste
    fileSource.close()
    return liste

# Sous-fonctions appelées dans analyse_ttc()
def searchVB(id, kasus) :
    """Fonction de recherche et de traitement du verbe, intervient lorsque ce dernier détermine le cas.
    Prend la position du mot dans la chaine et ainsi que son cas en entrée.
    Retourne un booléen : True si le verbe repéré appartient au vocabulaire défini pour le cas renseigné, False sinon.
    """
    # récupérer la tête de dépendance (root) et même si c'est pas root, on vérifie directement si le lemme de cette tête est présent dans la liste
    if kasus == "Dat":
        if Doc_nlp[id]["pos"] == "NOUN" :
            lemmeVB = Doc_nlp[id]["head_lemma"]        # récupération du lemme de la tête
        else :                              # si le verbe n'est pas atteignable en dépendance directe (d)
            id_head = Doc_nlp[id]["head_id"]           # on récupère l'indice de la tête dans le document pour cherche la dépendance supérieure (d+1)
            lemmeVB = Doc_nlp[id_head]["head_lemma"]   # on récupère le lemme en tête de la dépendance d+1
        if lemmeVB in listDat :             # si on atteint le verbe en dépendance directe ou indirecte, on retourne vrai
            return True
    return False                            # retourne False par défaut

def searchHead(id) :
    """Fonction qui retourne l'indice de l'élément tête d'une chaine d'éléments conjoints.
    Prend l'indice d'un conjoint quelconque en entrée.
    Exemple : retournera l'indice de "rouge" dans "(le chat) rouge et noir et blanc"
    """
    while Doc_nlp[id]["dep"] in ("cj", "cd"):
        id +=1
    return id

def DET_found(id) :
    """Fonction qui retourne vrai en l'absence de déterminant dans les dépendants d'un token et faux sinon.
    Prend l'indice du token en entrée.
    """
    strong = False
    for child_i in Doc_nlp[id]["children"]:
        if Doc_nlp[child_i]["pos"] == "DET":
            strong = True
            exit
    return strong

# Importation des listes de verbes
listDat = importFile("static/vb_dat.txt")       # liste de verbes avec complément obligatoire au datif
#listGen = importFile("vb_gen_plus.txt")  # liste de verbes avec complément obligatoire au génitif

def analyze_ttc(indice):
    """Fonction retournant l'analyse morphosyntaxique d'un mot dont on a renseigné l'indice"""
    #colis = json.loads(request.body)
    #indice = int(colis['indice'])       # récupération de l'indice du mot cliqué 
    global Doc_nlp                       # variable globale utilisée
    
    indice = int(indice)
    
    # dictionnaires d'étiquettes
    tabCas = {"Nom" : "nominatif", "Acc" : "accusatif", "Dat": "datif", "Gen": "génitif"}
    tabGenre = {"Fem" : "féminin", "Masc" : "masculin", "Neut": "neutre"}
    # initialisation de la réponse
    rep = ""
    # initialisatin des sous-chaines de caractères
    cas = ""
    genre = ""
    nb = ""

    # Analyse et rédaction de la réponse
    if Doc_nlp != [] and indice in range(0, len(Doc_nlp)):
        # Si l'indice existe dans la sortie spaCy (Doc_nlp), on récupère les infos du token correspondant

        # Mise en forme du cas repéré selon l'étiquette fournie par Spacy
        if len(Doc_nlp[indice]["case"]) != 0:
            if Doc_nlp[indice]["case"][0] in tabCas.keys(): # Doc_nlp[indice][3] contient ['Nom']
                etiquette = Doc_nlp[indice]["case"][0]
                cas = tabCas[etiquette]                     # récupération du cas dans le tableau associatif
        else : 
            cas = "cas inconnu"
        # Mise en forme du genre selon l'étiquette de Spacy
        if len(Doc_nlp[indice]["gender"]) != 0:
            if Doc_nlp[indice]["gender"][0] in tabGenre.keys():    # Doc_nlp[indice][4] contient ['Fem']
                etiquette = Doc_nlp[indice]["gender"][0]
                genre = tabGenre[etiquette]
        else :                                 # Certains mots tels que les pronoms (sich) ne possèdent pas nécessairement de genre
            genre = ""
        # Mise en forme du nombre selon l'étiquette de Spacy
        if Doc_nlp[indice]["number"] == "Sing":
            nb = "singulier"
        else : 	                               # sinon le nombre est "pluriel" par défaut
            nb = "pluriel"
        
        # Tests pour déterminer la cause du cas repéré par spacy
        # Récupération de l'indice de la tête syntaxique
        if Doc_nlp[indice]["dep"] == "cj":          # mot sélectionné suit une conjonction
            parent_id = searchHead(indice)          # on cherche la tête du premier conjoint
        else : 
            parent_id = Doc_nlp[indice]["head_id"]  # on garde la dépendance directe par défaut
        # 1) présence de préposition :
        if Doc_nlp[parent_id]["pos"] == "ADP":
            # si le mot est directement lié à une préposition par une dépendance
            rep += "La préposition précédente ('"+ Doc_nlp[parent_id]["text"] +"') détermine le cas. "
        elif Doc_nlp[parent_id]["head_pos"] == "ADP":      
            # vérification du lien indirect avec une préposition (ex: DET cliqué dans PREP+DET+NOM)
            head_cell = Doc_nlp[parent_id]["head_id"]
            rep += "La préposition précédente ('"+ Doc_nlp[head_cell]["text"] +"') détermine le cas. "
        # 2) Cas datif imposé par le verbe de rattachement :
        elif cas == "datif":
            if searchVB(indice, "Dat"):         # sous-fonction qui va chercher si le lemme du verbe correspond à un cas particulier
                rep += "Le verbe de rattachement détermine le cas. "
        # 3) Cas génitif 
        elif cas == "génitif":
            if Doc_nlp[indice]["dep"] == "ag" or Doc_nlp[parent_id]["dep"] =="ag":
                # Le mot sélectionné appartient à un syntagme complément du nom (d'après Spacy)
                rep += "Nous avons ici affaire à un complément du nom, autrement dit à un groupe de mot qui dénote la possession vis à vis du nom précédent. "
            else: 
                # On considère que le verbe est la cause du cas dans le contexte inverse
                rep += "Le verbe de rattachement détermine le cas. " 
        # 4) Cas nominatif (attribut du sujet)
        elif cas == "nominatif":
            if Doc_nlp[indice]["dep"] == "pd" or Doc_nlp[parent_id]["dep"] == "pd":
                # On vérifie la dépendance syntaxique du mot et de sa tête pour vérifier si syntagme = attribut du sujet (nominatif)
                rep += "Le verbe ne faisant ici que lier le sujet à une certaine spécification, il ne joue pas de rôle dans l'attribution du cas."
        # 5) Cas accusatif (complément direct du verbe)
        elif cas == "accusatif":
            rep += "Voici le contexte le plus courant dans lequel un verbe impose un cas de déclinaison : le complément direct (aussi appelé COD). "

        # completion de la chaine cas 
        if cas == "accusatif":
            cas = "à l'"+ cas
        else:
            cas = "au "+ cas

        # Fin de la réponse suivant si on a affaire à un nom, un pronom ou autre chose
        if Doc_nlp[indice]["pos"] == "NOUN": 
            rep += "Dans ce contexte, '" + Doc_nlp[indice]["text"] + "' est censé se décliner " + cas + ", mais sa forme le laisse peu transparaitre car il s'agit d'un nom (" + genre +" "+ nb +")."
        elif Doc_nlp[indice]["pos"] == "PRON":
            rep += "Dans ce contexte, '" + Doc_nlp[indice]["text"] + "' est décliné " + cas + ", et prend cette forme car il s'agit d'un pronom " + genre +" "+ nb +"."
        elif Doc_nlp[indice]["pos"] == "ADJ" and not DET_found(parent_id):
            rep += "Dans ce contexte, '" + Doc_nlp[indice]["text"] + "' est décliné " + cas + ". En l'absence de déterminant, ce mot hérite d'une marque de déclinaison dite 'forte' accordée avec un nom " + genre +" "+ nb +"."
        else:
            rep += "Dans ce contexte, '" + Doc_nlp[indice]["text"] + "' est décliné " + cas + " et prend cette forme car il s'accorde avec un nom " + genre +" "+ nb +"."
    else :  # Message d'erreur retourné en cas de token inconnu
        rep = "Error : out of Doc_nlp"

    # Préparation de la réponse pour JS
    reponse = {
        "reponse":rep
    }
    return rep
    #return JsonResponse(reponse)
#test 1 (nom)
print(Doc_nlp[10]["text"] + " "+ Doc_nlp[12]["text"] + " " + Doc_nlp[13]["text"])
#print(Doc_nlp[56][3])
#print(analyze_ttc(56))
# test 2 (det)
print(analyze_ttc(12))