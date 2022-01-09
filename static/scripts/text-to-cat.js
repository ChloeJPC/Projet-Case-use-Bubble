// Fonctions liées à la page text-to-cat.html

function textDefault() {
    // Fonction qui permet de fournir un texte de démonstration lorsque l'utilisateur n'en a pas à disposition
    var texte = ["Zwei Königssöhne gingen einmal auf Abenteuersuche und gerieten in ein wildes, wüstes Leben, so dass sie gar nicht wieder nach Haus kamen. Der jüngste, welcher der Dummling hieß, machte sich auf und suchte seine Brüder. Aber als er sie endlich fand, verspotteten sie ihn, weil er mit seiner Einfalt sich durch die Welt schlagen wolle. Aber zu zweit könnten auch sie nicht durchkommen, obwohl sie doch viel klüger seien. So zogen sie alle drei miteinander fort und kamen an einen Ameisenhaufen.",
                "Als das geschehen war, fingen sie auf ein Zeichen insgesamt an, ihre Musik zu machen: Der Esel schrie, der Hund bellte, die Katze miaute und der Hahn krähte. Dann stürzten sie durch das Fenster in die Stube hinein, dass die Scheiben klirrten. Die Räuber fuhren bei dem entsetzlichen Geschrei in die Höhe, meinten nicht anders, als dass ein Gespenst herein käme, und flohen in größter Furcht in den Wald hinaus.",
                "Im Augenblick befand er sich auch dort und wollte in die Stadt hinein. Als er aber vors Tor kam, wollten ihn die Schildwachen nicht einlassen, weil er seltsame und doch so reiche und prächtige Kleider anhatte. Da ging er auf einen Berg, wo ein Schäfer hütete, tauschte mit diesem die Kleider, zog den alten Schäferrock an und ging also ungestört in die Stadt ein.",
                "Ein weiteres Teilgebiet der Sprachwissenschaft ist die Angewandte Linguistik. Diese kann ebenfalls Fragen behandeln, die sprachübergreifend formuliert sind, zum Beispiel wissenschaftliche Grundlagen des Sprachunterrichts im Bereich der Fremdsprachenlehrforschung oder Sprachtherapie in der Klinischen Linguistik. Die Psycholinguistik untersucht unter anderem den Spracherwerb des Kleinkinds und die kognitiven Prozesse, die ablaufen, wenn Menschen Sprache verarbeiten.",
                "Die Korpuslinguistik und die Quantitative Linguistik sind Gebiete, die in den letzten Jahrzehnten durch die Erweiterung der technischen Möglichkeiten im Bereich der maschinellen Sprachverarbeitung stark an Bedeutung gewonnen haben. Die Soziolinguistik, Medienlinguistik und Politolinguistik behandeln den öffentlichen Sprachgebrauch und den Übergangsbereich zu den Sozialwissenschaften."]
    var min = 0;                   // poition initiale dans le tableau de textes
    var max = texte.length - 1;    // dernière position dans le tableau de textes
    var choice = Math.floor(Math.random() * (max - min)) + min;    // choix aléatoire d'une position
    document.getElementById('inText').value = texte[choice];       // affichage du texte de la cellule choisie aléatoirement
}

async function sendText() {
    // ON RÉCUPÈRE LES VARIABLES À ENVOYER AU SERVEUR
    var inText = document.getElementById('inText').value;
    // On réinitialise de formulaire d'envoie
    document.getElementById('inText').value = "";
    
    // ON EMBALLE LA VARIABLE A ENVOYER DANS UN JSON
    var colis = {
        inText: inText
    }
    console.log('Envoi colis:',colis);

    // PARAMÈTRES DE LA REQUÊTE 1
    const requete = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(colis)
    };

    // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE 1
    const response = await fetch('/analyze_tok/', requete)
    const data = await response.json();
    console.log(data);

    var baseTTC = document.getElementById('baseTTC');
    baseTTC.innerHTML = ""; // vider la div si elle contenait déjà qqc
    indice = 0;             // initialisation de l'indice pour localiser les mots dans la séquence
    for (token in data.reponse) {
        // récupération de chaque token identifié (tokenTuple[0]) et de son cas éventuel (tokenTuple[1])
        // que l'on met en forme dans des balises span de manière à pouvoir l'isoler dans la page web
        var tokenTuple = data.reponse[token];
        baseTTC.innerHTML += '<span id="'+indice+'" class="'+tokenTuple[1]+'">' + tokenTuple[0] + '</span> ';
        indice += 1;                // incrémentation de  l'indice
    }
}

// Récupération d'info spécifiques au survole d'un mot (fonction appelée par un evenement sur 'body')
async function showInfo(indice) {
    // Préparation du JSON pour requête au script python
    var colis = {
        indice: indice
    }
    console.log('Envoi colis:',colis);

    // PARAMÈTRES DE LA REQUÊTE 2
    const requete2 = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(colis)
    };

    // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE 2
    const response2 = await fetch('/analyze_ttc/', requete2)
    const data2 = await response2.json();
    console.log(data2);

    outText = document.getElementById('outText');
    outText.innerHTML = data2.reponse ; // affichage de l'analyse retournée par le script python
}

// Evenement faisant appel à la fonction showInfo pour affichage
document.querySelector('body').addEventListener('click', function(event) {
    if (event.target.tagName.toLowerCase() === 'span') {
        if(event.target.className != "None" && event.target.className.length < 4) {   
            // si la balise span concerne bien un token (length<4) et que son contenu est concerné par une déclinaison,
            // on récupère l'identifiant et la classe pour obtenir les infos sur l'élément.
            showInfo(event.target.id);
        }
    }
})