from django.urls import path
from . import views

urlpatterns = [
    path("teste/<int:id_componente_curricular>", views.listaProfessores, name="teste")
]
