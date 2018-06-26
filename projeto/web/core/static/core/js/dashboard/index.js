$cotent = $("#content");

function addMatrizCurricular($template, i) {
  setTimeout(function(){
    $cotent.append($template.html());
  }, 500 * i);
}

$(document).ready(function(){
  $.get( "/dashboard/getMatrizesCurriculares", function( matrizesCurriculares ) {
    if (matrizesCurriculares.length === 0) {

    }
    else {
      $("#spinner").fadeOut(0, function(){
        $("#content").fadeIn(400, function(){
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
            $template.find(".matrizCurricular").addClass('animated slideInUp');

            addMatrizCurricular($template, i);
          }
        });
      });
    }
  });
});
