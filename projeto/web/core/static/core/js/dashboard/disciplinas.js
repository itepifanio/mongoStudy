$(document).ready(function(){
  $.get( "/dashboard/cursos/disciplinas/get" + window.location.search, function(disciplinas) {
    $cotent = $("#content");
    if (disciplinas.length === 0) {

    }
    else {
      var semestres = []
      disciplinas.forEach(function(element, index, array) {
        if(semestres[element.semestre]) {
          semestres[element.semestre].push(element);
        }
        else {
          semestres[element.semestre] = [];
          semestres[element.semestre].push(element);
        }
      });

      semestres.forEach(function(semestre, index, array){
        if (index > 0) {
          var $templateSemestre = $("#templateSemestre").clone();
          $templateSemestre.find(".nome").text(index + "° Semestre");
          semestre.forEach(function(disciplina, i, a){
            $templateDisciplina = $("#templateDisciplina").clone();
            $templateDisciplina.find(".disciplina").text(disciplina.codigo + " - " + disciplina.nome);
            $templateDisciplina.find(".disciplina").attr("href", "/dashboard/cursos/disciplinas/estatisticas?id-disciplina=" + disciplina.id);
            $templateSemestre.find(".disciplinas").append($templateDisciplina.html());
          })

          $("#content").append($templateSemestre.html());
        }
      });

      $("#spinner").fadeOut(0, function(){
        $("#content").fadeIn(400);
      });
    }
  });
});
