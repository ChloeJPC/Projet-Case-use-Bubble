# Exercice texte à trous pour les débutants : choisir la bonne déclinaison d'un mot (liste déroulante)

import spacy, random
nlp = spacy.load("de_core_news_md")
# https://spacy.io/models/de
# https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/#Morphology


# Fonction Importer le corpus
def importCorpus (nomDuFicCorpus) :
    """Importer le corpus pour l'exercice à trous
    Entrée : chemin vers le fichier contenant le corpus
    Sortie : Tableau contenant [titre, niveau, source, contenu] pour chaque texte"""
    descFicCorpus = open(nomDuFicCorpus,"r",encoding="utf-8")
    corpus = []
    for ligne in descFicCorpus :   # pour chaque ligne dans le fichier
        # Une ligne correspond à un texte du corpus
        descTexte = [] # [titre, niveau, source, contenu]
        if ligne[0] != "#" and ligne !="\n": # si ce n'est pas une ligne de commentaires ou une ligne vide :
            ligne = ligne.rstrip()   # on enlève le \n de chaque ligne
            ligneSplit = ligne.split("\t")   # séparation de la ligne aux tabulations
            if len(ligneSplit) >= 4 and ligneSplit[1] in ["A1","A2","B1","B2"] : # vérification que la ligne ait au moins les 4 elts [titre, niveau, source, contenu] et un niveau autorisé
                descTexte = [ligneSplit[0],ligneSplit[1],ligneSplit[2], ligneSplit[3]]
                corpus.append(descTexte)
    descFicCorpus.close()
    return corpus

# Fonction Importer les pronoms
def importPron(nomDuFicPron):
    Sing = []
    Plur = []
    descFicPron = open(nomDuFicPron,"r",encoding="utf-8")
    readFic = descFicPron.readlines()
    for ligne in readFic :
        if ligne[0] != "#" and ligne !="\n": # si ce n'est pas une ligne de commentaires ou une ligne vide :
            ligne = ligne.rstrip()   # on enlève le \n de chaque ligne
            ligneSplit = ligne.split("\t")   # séparation de la ligne aux tabulations
            Sing.append(ligneSplit[0].split(",")) # ex : ["der","den","dem","dessen"]
            if len(ligneSplit)>1 :
                Plur.append([ligne[1].split(",")])
    descFicPron.close()
    pronoms = {"Sing":Sing, "Plur":Plur}
    return pronoms

# Fonction séparer le corpus par le niveau des textes
def listeNiveaux (nomDuFicCorpus) :
    """Lister les indices des textes du corpus par niveau
    Entrée : chemin vers le fichier contenant le corpus
    Sortie : Tableau avec 4 élements contenant pour chaque niveau (A1, A2, B1, B2) les indices des textes correspondant"""
    descFicCorpus = open(nomDuFicCorpus,"r",encoding="utf-8")
    cpt = 0 # numéro du texte
    indA1 = [] # tableau qui contiendra les indices des textes de niveau A1
    indA2 = []
    indB1 = []
    indB2 = []
    for ligne in descFicCorpus :   # pour chaque ligne dans le fichier
        # Une ligne correspond à un texte du corpus
        if ligne[0] != "#" and ligne !="\n": # si ce n'est pas une ligne de commentaires ou une ligne vide :
            ligne = ligne.rstrip()   # on enlève le \n de chaque ligne
            ligneSplit = ligne.split("\t")   # séparation de la ligne aux tabulations
            if len(ligneSplit) >= 4 and ligneSplit[1] in ["A1","A2","B1","B2"] : # vérification que la ligne ait au moins les 4 elts [titre, niveau, source, contenu] et un niveau autorisé
                if ligneSplit[1] == "A1" :
                    indA1.append(cpt) # on ajoute l'indice du texte au tableau de son niveau
                    cpt += 1 # on incrémente le cpt des indices
                elif ligneSplit[1] == "A2" :
                    indA2.append(cpt) 
                    cpt += 1
                elif ligneSplit[1] == "B1" :
                    indB1.append(cpt)
                    cpt += 1
                elif ligneSplit[1] == "B2" :
                    indB2.append(cpt)
                    cpt += 1
    descFicCorpus.close()
    niveaux =[indA1,indA2,indB1,indB2]
    return niveaux

# DET
det = {
    "ein" : { # article indéfini
        "Sing" : {
            "Masc" : [
                "ein",      #Nom 0
                "einen",    #Acc 1
                "eines",    #Gen 2
                "einem",    #Dat 3
            ],
            "Fem" : [
                "eine",
                "eine",
                "einer",
                "einer",
            ],
            "Neut" : [
                "ein",
                "ein",
                "eines",
                "einem",
            ],
        }
    },
    "der" : {   # article défini
        "Sing" : {
            "Masc" : [
                "der",
                "den",
                "des",
                "dem",
            ],
            "Fem" : [
                "die",
                "die",
                "der",
                "der",
            ],
            "Neut" : [
                "das",
                "das",
                "des",
                "dem",
            ]
        },
        "Plur" : [
            "die",
            "die",
            "der",
            "den",
        ]
    },
    "mein" : { # adjectif possessif (mon)
        "Sing" : {
            "Masc" : [
                "mein",      
                "meinen",    
                "meines",    
                "meinem",    
            ],
            "Fem" : [
                "meine",
                "meine",
                "meiner",
                "meiner",
            ],
            "Neut" : [
                "mein",
                "mein",
                "meines",
                "meinem",
            ],
        },
        "Plur" : [
            "meine",
            "meine",
            "meiner",
            "meinen",
        ]
    },
    "dein" : { # adjectif possessif (ton)
        "Sing" : {
            "Masc" : [
                "dein",      
                "deinen",    
                "deines",    
                "deinem",    
            ],
            "Fem" : [
                "deine",
                "deine",
                "deiner",
                "deiner",
            ],
            "Neut" : [
                "dein",
                "dein",
                "deines",
                "deinem",
            ],
        },
        "Plur" : [
            "deine",
            "deine",
            "deiner",
            "deinen",
        ]
    },
    "sein" : { # adjectif possessif (son)
        "Sing" : {
            "Masc" : [
                "sein",      
                "seinen",    
                "seines",    
                "seinem",    
            ],
            "Fem" : [
                "seine",
                "seine",
                "seiner",
                "seiner",
            ],
            "Neut" : [
                "sein",
                "sein",
                "seines",
                "seinem",
            ],
        },
        "Plur" : [
            "seine",
            "seine",
            "seiner",
            "seinen",
        ]
    },
    "unser" : { # adjectif possessif (notre)
        "Sing" : {
            "Masc" : [
                "unser",      
                "unseren",    
                "unseres",    
                "unserem",    
            ],
            "Fem" : [
                "unsere",
                "unsere",
                "unserer",
                "unserer",
            ],
            "Neut" : [
                "unser",
                "unser",
                "unseres",
                "unserem",
            ],
        },
        "Plur" : [
            "unsere",
            "unsere",
            "unserer",
            "unseren",
        ]
    },
    "euer" : { # adjectif possessif (votre)
        "Sing" : {
            "Masc" : [
                "euer",      
                "eueren",    
                "eueres",    
                "euerem",    
            ],
            "Fem" : [
                "euere",
                "euere",
                "euerer",
                "euerer",
            ],
            "Neut" : [
                "euer",
                "euer",
                "eueres",
                "euerem",
            ],
        },
        "Plur" : [
            "euere",
            "euere",
            "euerer",
            "eueren",
        ]
    },
    "ihr" : { # adjectif possessif (leur)
        "Sing" : {
            "Masc" : [
                "ihr",      
                "ihren",    
                "ihres",    
                "ihrem",    
            ],
            "Fem" : [
                "ihre",
                "ihre",
                "ihrer",
                "ihrer",
            ],
            "Neut" : [
                "ihr",
                "ihr",
                "ihres",
                "ihrem",
            ],
        },
        "Plur" : [
            "ihre",
            "ihre",
            "ihrer",
            "ihren",
        ]
    },
    "dies" : { # adjectif démonstratif
        "Sing" : {
            "Masc" : [
                "dieser",      
                "diesen",    
                "dieses",    
                "diesem",    
            ],
            "Fem" : [
                "diese",
                "diese",
                "dieser",
                "dieser",
            ],
            "Neut" : [
                "dieses",
                "dieses",
                "dieses",
                "diesem",
            ],
        },
        "Plur" : [
            "diese",
            "diese",
            "dieser",
            "diesen",
        ]
    },
    "jen" : { # adjectif démonstratif
        "Sing" : {
            "Masc" : [
                "jener",      
                "jenen",    
                "jenes",    
                "jenem",    
            ],
            "Fem" : [
                "jene",
                "jene",
                "jener",
                "jener",
            ],
            "Neut" : [
                "jenes",
                "jenes",
                "jenes",
                "jenem",
            ],
        },
        "Plur" : [
            "jene",
            "jene",
            "jener",
            "jenen",
        ]
    },
    "derjenige" : { # adjectif démonstratif
        "Sing" : {
            "Masc" : [
                "derjenige",      
                "denjenigen",    
                "desjnenigen",    
                "demjenigen",    
            ],
            "Fem" : [
                "diejenige",
                "diejenige",
                "derjenigen",
                "derjenigen",
            ],
            "Neut" : [
                "dasjenige",
                "dasjenige",
                "desjenigen",
                "demjenigen",
            ],
        },
        "Plur" : [
            "diejenigen",
            "diejenigen",
            "derjenigen",
            "denjenigen",
        ]
    },
    "derselbe" : { # adjectif démonstratif
        "Sing" : {
            "Masc" : [
                "derselbe",      
                "denselben",    
                "desselben",    
                "demselben",    
            ],
            "Fem" : [
                "dieselbe",
                "dieselbe",
                "derselben",
                "derselben",
            ],
            "Neut" : [
                "dasselbe",
                "dasselbe",
                "desselben",
                "demselben",
            ],
        },
        "Plur" : [
            "dieselben",
            "dieselben",
            "derselben",
            "denselben",
        ]
    },
    "kein" : { # article indéfini
        "Sing" : {
            "Masc" : [
                "kein",      
                "keinen",    
                "keines",    
                "keinem",    
            ],
            "Fem" : [
                "keine",
                "keine",
                "keiner",
                "keiner",
            ],
            "Neut" : [
                "kein",
                "kein",
                "keines",
                "keinem",
            ],
        },
        "Plur" : [
            "keine",
            "kein",
            "keinr",
            "keinen",
        ]
    },
    "alle" : { # adjectif indéfini
        "Sing" : {
            "Masc" : [
                "aller",      
                "allen",    
                "alles",    
                "allem",    
            ],
            "Fem" : [
                "alle",
                "alle",
                "aller",
                "aller",
            ],
            "Neut" : [
                "alles",
                "alles",
                "alles",
                "allem",
            ],
        },
        "Plur" : [
            "alle",
            "alle",
            "aller",
            "allen",
        ]
    },
}

# chemin du fichier contenant le corpus
fichCorpus = "static/corpus.csv" # UNE SEULE FOIS

# Importer le corpus
corpus = importCorpus(fichCorpus)        # UNE SEULE FOIS
niveaux = listeNiveaux(fichCorpus)

# Mélanger l'ordre des textes /!\ A chaque charg de page exo/!\
def randomTxtCorpus(corpus) :  
    textesInd = [] # initialisation de la liste
    for i in range (0,len(corpus)) : 
        textesInd.append(i)
    random.shuffle(textesInd) # mélanger la liste
    return textesInd

#tests
print(niveaux)

# Sous-fonction : récupérer les tokens du texte dans un tableau
def analyseTokens(num) :
    global corpus
    texte = corpus[num] # [titre, niveau, source, contenu]
    contenu = texte[3] # on isole le contenu du texte
    doc = nlp(contenu)
    liste = []
    for token in doc:  
        if token.morph.get('Case') != [] : # si le token a un cas
            # [token, POStag, Lemme, Cas, Genre, Nombre]
            cas = str(token.morph.get('Case')) # pour éviter les tableaux dans le tableau 
            genre = str(token.morph.get('Gender')) #(ex :[zur, 'ADP', 'zur', ['Dat'], ['Fem'], ['Sing']])
            nb = str(token.morph.get('Number')) # 0 = token ; 1 = tag ; 2 = lemme ; 3= cas ; 4 = genre ; 5 = nombre
            liste.append([str(token), token.pos_,token.lemma_,cas[2:-2],genre[2:-2],nb[2:-2]])# enlève les ['']
        else :
            liste.append(str(token))
    return liste

# Sous-fonction : créer les listes déroulantes
def listesDeroulantes(liste) :
    cptSelect = 0
    brutListesDer = []
    for elt in liste :
        if type(elt)==list : # savoir si l'elt est une liste, donc un mot qui se décline
            token = elt[0].lower()
            tag= elt[1]
            lemme = elt[2].lower() # les lemmes sont en minuscule dans les ressources
            cas = elt[3]
            genre = elt[4]
            nombre = elt[5]
            ### si on a un DET qui est dans le tableau det
            if tag == "DET" and lemme in det.keys():
                if lemme == "mein" : # pour ["dein","sein","unser","euer","ihr"] (ton, son, notre, votre, leur) le lemme est "mein" (mon)
                    if token[:3] == "dei" :
                        lemme = "dein"
                    elif token[:3] == "sei" :
                        lemme = "sein"
                    elif token[:3] == "uns" :
                        lemme = "unser"
                    elif token[:3] == "eue" :
                        lemme = "euer"
                    elif token[:3] == "ihr" :
                        lemme = "ihr"
                tablLemme = det[lemme] # on veut aller dans le tableau du lemme
                tablNombre = tablLemme[nombre] # on veut aller dans le tableau sing ou plur
                ### si singulier -> on va chercher le genre
                if nombre =="Sing" :
                    tablGenre = tablNombre[genre] # on veut aller dans le tableau masc, fem ou neutre
                    cptSelect += 1 # incrémentation du compteur qui compte le nombre de listes déroulantes
                    # création de la liste déroulante avec les différentes déclinaisons
                    listeDer = "\n<select class=\"selectList\" id=\""+str(cptSelect)+"\">\n"
                     # toutes les propositions
                    listeDer = listeDer + "\t<option>"+tablGenre[0]+"/"+tablGenre[1]+"/"+tablGenre[2]+"/"+tablGenre[3]+"</option>\n"
                    # nominatif
                    if cas =="Nom" : # indice 0 de tablGenre
                        listeDer = listeDer + "\t<option class=\"c1 Nom\" value=\"c1\">(nominatif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Nom\" value=\"c0\">(nominatif) "+tablGenre[0]+"</option>\n"
                    # accusatif
                    if cas =="Acc" : # indice 1 de tablGenre
                        listeDer = listeDer + "\t<option class=\"c1 Acc\" value=\"c1\">(accusatif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Acc\" value=\"c0\">(accusatif) "+tablGenre[1]+"</option>\n"
                    # génitif
                    if cas =="Gen" : # indice 2 de tablGenre
                        listeDer = listeDer + "\t<option class=\"c1 Gen\" value=\"c1\">(génitif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Gen\" value=\"c0\">(génitif) "+tablGenre[2]+"</option>\n"
                    # datif
                    if cas =="Dat" : # indice 3 de tablGenre
                        listeDer = listeDer + "\t<option class=\"c1 Dat\" value=\"c1\">(datif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Dat\" value=\"c0\">(datif) "+tablGenre[3]+"</option>\n"
                    listeDer = listeDer + "</select><span class=\"coches\" id=\"coche"+str(cptSelect)+"\"></span>\n"
                ### sinon pluriel -> pas de genre    
                else : 
                    cptSelect += 1 # incrémentation du compteur qui compte le nombre de listes déroulantes
                    # création de la liste déroulante avec les différentes déclinaisons
                    listeDer = "\n<select class=\"selectList\" id=\""+str(cptSelect)+"\">\n"
                    # toutes les propositions
                    listeDer = listeDer + "\t<option>"+tablNombre[0]+"/"+tablNombre[1]+"/"+tablNombre[2]+"/"+tablNombre[3]+"</option>\n"
                    # nominatif
                    if cas =="Nom" : # indice 0 de tablNombre
                        listeDer = listeDer + "\t<option class=\"c1 Nom\" value=\"c1\">(nominatif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Nom\" value=\"c0\">(nominatif) "+tablNombre[0]+"</option>\n"
                    # accusatif
                    if cas =="Acc" : # indice 1 de tablNombre
                        listeDer = listeDer + "\t<option class=\"c1 Acc\" value=\"c1\">(accusatif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Acc\" value=\"c0\">(accusatif) "+tablNombre[1]+"</option>\n"
                    # génitif
                    if cas =="Gen" : # indice 2 de tablNombre
                        listeDer = listeDer + "\t<option class=\"c1 Gen\" value=\"c1\">(génitif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Gen\" value=\"c0\">(génitif) "+tablNombre[2]+"</option>\n"
                    # datif
                    if cas =="Dat" : # indice 3 de tablNombre
                        listeDer = listeDer + "\t<option class=\"c1 Dat\" value=\"c1\">(datif) "+token+"</option>\n"
                    else :
                        listeDer = listeDer + "\t<option class=\"c0 Dat\" value=\"c0\">(datif) "+tablNombre[3]+"</option>\n"
                    listeDer = listeDer + "</select><span class=\"coches\" id=\"coche"+str(cptSelect)+"\"></span>\n"
                # écriture de la liste déroulante
                brutListesDer.append(listeDer)
            else : # sinon le DET (ou autre) n'est pas dans la ressource
                brutListesDer.append(elt[0]) # on ne garde que le token, on n'a pas de ressources pour sa déclinaison.
        else : # sinon ce n'est pas un mot qui se décline
            brutListesDer.append(elt)
    # création de la ligne <script> pour connaitre le nombre de listes déroulantes dans l'exercice
    NbListesDer = "\n<script type=\"text/javascript\">var $nbListes = "+str(cptSelect)+";</script>"
    # tableau à 2D avec le nombre de listes déroulantes + tokens et listes déroulantes
    brutListesDerNb = [brutListesDer,NbListesDer]
    return brutListesDerNb

# Sous-fonction : Séparer les phrases dans des paragraphes différents.
eosTokens = ['.','!','?','…']
def finDePhrase(listeDer) :
    global eosTokens
    eosHTML = "<p>" 
    listeDer0 = listeDer[0] # 1er elt du tableau contient les tokens et les listes déroulantes (2e : nb de listes déroulantes)
    for elt in listeDer0 :
        if len(elt)==1 and elt in eosTokens :
            eosHTML += elt+"</p>" # fermeture du parag. et ouverture du suivant.
            eosHTML += " "+"\n<p>"
        else :
            eosHTML += " "+elt
    if eosHTML[-3:] == "<p>" : # suppression d'un paragraphe qui ne serait pas fermé à la fin de eosHTML
        eosHTML = eosHTML[:-3]
    else : # sinon le dernier elt ne ferme pas le paragraphe
        eosHTML += "</p>"
    # ajout de la ligne <script> avec le nombre de listes déroulantes
    eosHTML += listeDer[1] 
    return eosHTML

# Fonction principale
def analyze_trou(numTxtCorpus) :
    listeTokens = analyseTokens(numTxtCorpus)
    listesDer = listesDeroulantes(listeTokens)
    finalHTML = finDePhrase(listesDer)
    return finalHTML


#TEST
#print(finDePhrase(listesDeroulantes(analyseTokens(corpus,5)),eosTokens))
# print(analyze_trou(3))


