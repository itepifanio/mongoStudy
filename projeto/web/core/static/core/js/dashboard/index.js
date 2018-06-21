$(document).ready(function(){
  $.get( "/dashboard/getMatrizesCurriculares", function( matrizesCurriculares ) {
    $cotent = $("#content");
    if (matrizesCurriculares.length === 0) {

    }
    else {
      for(var i = 0; i < matrizesCurriculares.length; i++) {
        var $template = $("#templateMatrizCurricular").clone();
        $template.find(".curso").text(matrizesCurriculares[i].curso);
        $template.find(".value-turno").text(matrizesCurriculares[i].turno);
        $template.find(".value-ano").text(matrizesCurriculares[i].ano);
        if (matrizesCurriculares[i].enfase) {
          $template.find(".value-enfase").text(matrizesCurriculares[i].enfase);
        }
        else {
          $template.find(".enfase").css("display", "none");
        }

        $template.find(".matrizCurricular").attr("href", "/dashboard/disciplinas?id-matriz-curricular=" + matrizesCurriculares[i].id)
        $cotent.append($template.html());
      }
    }

    $("#spinner").fadeOut(0, function(){
      $("#content").fadeIn(400);
    });
  });
});
