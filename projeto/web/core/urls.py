from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("authenticate", views.authenticate, name="authenticate"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/cursos/", views.cursos, name="cursos"),
    path("dashboard/cursos/get/", views.getCursos, name="getCursos"),
    path("dashboard/cursos/disciplinas/", views.disciplinas, name="disciplinas"),
    path("dashboard/cursos/disciplinas/get", views.getDisciplinas, name="getDisciplinas"),
    path("dashboard/cursos/disciplinas/estatisticas", views.estatisticas, name="estatisticas")
]
