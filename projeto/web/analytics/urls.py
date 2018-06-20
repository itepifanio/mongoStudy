from django.urls import path
from analytics import views

urlpatterns = [
    path("listaProfessores/<int:id_componente_curricular>", views.listaProfessores, name="listaProfessores"),
    path("jsonProfessor/<int:id_componente_curricular>/detalhe/<int:siape>", views.jsonProfessor, name="jsonProfessor"),
    path("detalhesProfessor/<int:id_componente_curricular>/detalhe/<int:siape>", views.detalhesProfessor, name="detalhesProfessor")
]
