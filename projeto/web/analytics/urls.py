from django.urls import path
from analytics import views

urlpatterns = [
    path("dashboard/listaProfessores/<int:id_componente_curricular>", views.listaProfessores, name="listaProfessores"),
    path("dashboard/jsonProfessor/<int:id_componente_curricular>/detalhe/<int:siape>", views.jsonProfessor, name="jsonProfessor"),
    path("dashboard/detalhesProfessor/<int:id_componente_curricular>/detalhe/<int:siape>", views.detalhesProfessor, name="detalhesProfessor")
]
