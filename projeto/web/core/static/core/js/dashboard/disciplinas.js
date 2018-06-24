$(document).ready(function(){
  $('.tabs').tabs();

  $.get( "/dashboard/getDisciplinas" + window.location.search + "&tipo=obrigatorias", function(disciplinas) {
    if (disciplinas.length === 0) {

    }
    else {
      $("#obrigatorias .spinner").fadeOut(0, function(){
        $("#obrigatorias .content").fadeIn(400, function() {
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
                $templateDisciplina.find(".disciplina").attr("href", "listaProfessores/" + disciplina.id);
                $templateSemestre.find(".disciplinas").append($templateDisciplina.html());
              });

              $templateSemestre.find(".semestre-wrapper").addClass('animated slideInUp');

              setTimeout(function(){$("#obrigatorias .content").append($templateSemestre.html());}, 500 * index);
            }
          });
        });
      });
    }
  });

  $(".tabs .tab").on("click", function(e){
    if($(this).data("tipo") === "optativas") {
      if ($("#optativas .content").is(':empty')) {
        $("#optativas .spinner").css("display", "block");
        $.get( "/dashboard/getDisciplinas" + window.location.search + "&tipo=optativas", function(disciplinas) {
          if (disciplinas.length === 0) {

          }
          else {
            var semestres = []
            disciplinas.forEach(function(disciplina, index, array) {
              $templateDisciplina = $("#templateDisciplina").clone();
              $templateDisciplina.find(".disciplina").text(disciplina.codigo + " - " + disciplina.nome);
              $templateDisciplina.find(".disciplina").attr("href", "/dashboard/estatisticas" +  window.location.search + "&id-disciplina=" + disciplina.id);

              $("#optativas .content").append($templateDisciplina.html());
            });

            $("#optativas .spinner").fadeOut(0, function(){
              $("#optativas .content").fadeIn(400);
            });
          }
        });
      }
    }
  })
});
