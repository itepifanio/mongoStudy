$(document).ready(function(){
  $.get( "/dashboard/cursos/get", function( cursos ) {
    $cotent = $("#content");
    if (cursos.length === 0) {

    }
    else {
      for(var i = 0; i < cursos.length; i++) {
        var $template = $("#templateCurso").clone();
        $template.find(".nome").text(cursos[i].curso);
        $template.find(".matricula").text(cursos[i].matricula);
        $template.find(".ingresso").text(cursos[i].ingresso);
        $template.find(".curso").attr("data-curso-id", cursos[i].id);
        $template.find(".curso").attr("data-discente-id", cursos[i].discente);
        $template.find(".curso").attr("href", "/dashboard/cursos/disciplinas?discente-id=" + cursos[i].discente + "&curso-id=" + cursos[i].id)
        $cotent.append($template.html());
      }
    }

    $("#spinner").fadeOut(0, function(){
      $("#content").fadeIn(400);
    });
  });
});
