$(".nav-link").on("click", function() {
    let pane = ["recap", "outil1", "Ex1", "links"];     // tableau contenant les id des éléments à manipuler (cibles)
    let nb = Number($(this).attr("id"));                // récupération et conversion du chiffre servant d'identifiant à l'élément déclencheur
    //console.log(nb);
    for (let i = 0; i < pane.length; i++) {
        // Pour chaque position du tableau, on s'assure que le contenu lié n'est plus affiché
        // si ladite position ne correspond pas à l'id déclecheur
        if (i != nb) {
            $("#"+pane[i]).removeClass("active show");
            $("#"+i).removeClass("active");
        }
    }
    $("#"+pane[nb]).addClass("active show");            // affichage du contenu lié à l'id cible
    $("#"+nb).addClass("active");
});