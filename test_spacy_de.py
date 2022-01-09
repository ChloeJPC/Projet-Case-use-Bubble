import spacy
nlp = spacy.load("de_core_news_md")
# https://spacy.io/models/de
# https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/#Morphology
# https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/annotation/tiger_introduction.pdf

def test1():
    doc = nlp("Ich helfe meiner kleinen Schwester.")
    #doc = nlp("Ich helfe meine kleine Schwester.")         # Version erronée ("meine" et "kleine" analysés comme 'Acc')
    print(doc.text)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.morph.get('Case'), token.morph.get('Number'))
        # token.morph donne l'ensemble des traits morphologiques

def test2():
    doc = nlp("Annalena, die neben dem Auto steht, ist eine Studentin.")
    print(doc.text)
    for token in doc:
        if(token.morph.get('Case') != []):
            print(token.text, token.lemma_, token.pos_, token.dep_, token.head, token.head.dep_, token.morph.get('Case'), token.morph.get('Gender'), token.morph.get('Number'))
            # "eine Studentin" est bien analysé par spacy comme étant du nominatif -> attribut du sujet après un verbe d'état
            # nk = noun kernel ; sb = subject
            # pd = predicate = prédicat de la phrase -> si c'est un nom, il est donc au nominatif (vb associé est copule)
            # token.head.dep_  = dépendance de la tête (DONC fonction du syntagme)

def test2_2():
    doc = nlp("Man habe den Fahrer des Diebstahls verdächtigt.")
    print(doc.text)
    for token in doc:
        if(token.morph.get('Case') != []):
            print(token.text, token.lemma_, token.pos_, token.dep_, token.head, token.head.dep_, token.morph.get('Case'), token.morph.get('Gender'), token.morph.get('Number'))
            # erreur d'analyse de Spacy : "des Diebstahls" est complément du verbe (pas du nom) dans ce cas

def test2_3():
    doc = nlp("Tom beschuldigte Maria des Diebstahls.")
    print(doc.text)
    for token in doc:
        if(token.morph.get('Case') != []):
            print(token.text, token.lemma_, token.pos_, token.dep_, token.head, token.head.dep_, token.head.i, token.morph.get('Case'), token.morph.get('Gender'), token.morph.get('Number'))
            # Même erreur que pour test2_2
            # token.head.i donne la position de la tête dans le texte en entrée (début = 0)

def test2_4():
    doc = nlp("Tom hat eine schöne Freundin.")
    print(doc.text)
    for token in doc:
        if(token.morph.get('Case') != []):
            print(token.text, token.lemma_, token.pos_, token.dep_, token.head, token.head.dep_, token.head.i, token.morph.get('Case'), token.morph.get('Gender'), token.morph.get('Number'))
            # token.head.i donne la position de la tête dans le texte en entrée (début = 0)
            # Freundin = dépendance syntaxique "oa"


def test3():
    doc = nlp("Annalena, die neben dem Pferd steht,  ist gestern in die Stadt gezogen.")
    doc2 = nlp("Annalena, die neben das Pferd steht, ist gestern in der Stadt gezogen.")
    for i in range(0, len(doc)):
        if(doc[i].morph.get('Case') != []):
            if(doc[i].morph.get('Case') != doc2[i].morph.get('Case')):
                print(doc[i].text, "\t", doc[i].pos_, "\t", doc[i].morph.get('Case'), "\t")
        else:
            print(doc[i].text, "\t", doc[i].pos_)

def test4():
    doc = nlp("Annalena, die neben dem Pferd steht,  ist gestern in die Stadt gezogen.")
    i = 0
    while doc[i].text != "Pferd":
        i += 1
    if i != 0 : 
        for i in range(i-2, i+1):
            print(doc[i].text, "\t", doc[i].pos_, "\t", doc[i].morph.get('Case'), "\t")

def test5(id):
    while Doc_nlp[id].dep_ in ("cj", "cd"):
        id +=1
    print(Doc_nlp[id].text, Doc_nlp[id].pos_, Doc_nlp[id].dep_)

Doc_nlp = nlp("Nun müsste er ihn , wenn zwölf Jahre herum wären, ausliefern.")
#Doc_nlp = nlp("Er war hier, weil er mit seiner Einfalt sich durch die Welt schlagen wolle.")
print(Doc_nlp.text)
for token in Doc_nlp :
    print(token.text, token.pos_, token.dep_, token.head, token.head.dep_, token.head.i)
#test5(4)