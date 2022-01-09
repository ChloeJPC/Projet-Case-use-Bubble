// Fonctions liées à la page Ex-a-trou.html

// ID des div utilisées pour écrire le résultat des fonctions
txtListDer = document.getElementById('txtListDer'); // contient l'exo avec les listes déroulante
titreTxt = document.getElementById('titreTxt'); // titre du texte + Niveau du texte
dropA1 = document.getElementById('dropA1'); // menu déroulant des textes niveau A1
dropA2 = document.getElementById('dropA2');
dropB1 = document.getElementById('dropB1');
dropB2 = document.getElementById('dropB2');

// Fonction charger un exercice
 async function loadEx(indice) {
   // ON RÉCUPÈRE LES VARIABLES À ENVOYER AU SERVEUR
   var inText = indice; // Indice du texte du corpus que l'on souhaite pour l'exercice
       // ON EMBALLE LA VARIABLE A ENVOYER DANS UN JSON
   var colis = {
       inText: inText
   }
   // PARAMÈTRES DE LA REQUÊTE 
   const requete = {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(colis)
   };
       // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE 1 - texte
   const response = await fetch('/txtExo/', requete)
   const data = await response.json();
   console.log(data);
   txtListDer.innerHTML = data.reponse[0]; // code HTML de l'ex à trous (str)
   $nbListes = data.reponse[1]; // nombre de listes déroulantes de l'exo (int)

       // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE 2 - [niveau, titre, indice]
   const response2 = await fetch('/titreNiv/', requete)
   const data2 = await response2.json();
   console.log(data2);
   titreTxt.innerHTML = "Niveau "+data2.reponse[0]+" - "+data2.reponse[1];
   $indTxtActuel = data2.reponse[2];
};

// Fonction pour obtenir le nombre de textes du corpus
async function getNbTxt() {
    // PARAMÈTRES DE LA REQUÊTE 
    const requete = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    };
    // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE - nb de textes
    const response = await fetch('/nbTextes/', requete)
    const data = await response.json();
    console.log("Nombre de textes : "+data.reponse);
    $nbTextes = data.reponse; // nombre de textes dans le corpus (int)
};

// Fonction pour créer les listes des textes par niveau dans des dropdowns
async function menuDer(){
    // PARAMÈTRES DE LA REQUÊTE 
    const requete = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    };
    // ENVOI ET RÉCUPÉRATION DE LA RÉPONSE - dropdowns
    const response = await fetch('/dropdowns/', requete)
    const data = await response.json();
    dropA1.innerHTML = data.reponse[0]; 
    dropA2.innerHTML = data.reponse[1];
    dropB1.innerHTML = data.reponse[2];
    dropB2.innerHTML = data.reponse[3];
}

// Fonction à appliquer au chargement de la page
function loadPage() {
    loadEx(0); // 1er exercice
    getNbTxt(); // nb de textes du corpus
    menuDer(); // afficher les textes par niveau dans des dropdowns
  }

// Lancer le premier exercice au chargement de la page
document.addEventListener('DOMContentLoaded', loadPage()); 

// Passer au texte suivant
$("#autreTxt").on({		// bouton "Changer de texte/Texte suivant"
    "click" : function(){
        txtListDer.innerHTML = "Chargement en cours"
        titreTxt.innerHTML = ""
        $nextInd = $indTxtActuel + 1;
        if ($nextInd >= $nbTextes) {
            $nextInd = 0;   // si on est arrivé au dernier texte, on recommence au premier
        }
        loadEx($nextInd);
        $("#autreTxt").val("Changer de texte");
        $("#autreTxt").css('background-color', '#F3969A') // rose saumon
    }
});


// Réinitialiser les listes (afficher la première option par défaut + enlever les V ou X)
$("#reinitBouton").on({		// bouton "Réinitialiser"
    "click" : function(){
        $('.selectList').prop("selectedIndex",0)
        $('.coches').text("");
    }
});

// Valider les réponses selectionnées
$("#validerBouton").on({		// bouton "Valider"
    "click" : function(){
        for (let i = 1; i <= $nbListes; i++){ 
            if ($("#"+i).val()=="c1") {
                $("#coche"+i).text("✅"); // afficher V pour une bonne réponse
            } else if ($("#"+i).val()=="c0") {
                $("#coche"+i).text("❌"); // affichger X pour une muvaise répone
            } else {
                $("#coche"+i).text(""); // ne rien afficher quand on a la première option selectionnée (avec toutes les réponses possibles)
            }
        }
        // si toutes les réponses sont bonnes on propose de passer au texte suivant
        var $toutBon = true
        for (let i = 1; i <= $nbListes; i++){
            if ($("#"+i).val()!="c1") {
                $toutBon = false;
            } 
        }
        if ($toutBon){
            $("#autreTxt").val("Texte Suivant");
            $("#autreTxt").css('background-color', '#6CC3D5') // bleu
        }
    }
});