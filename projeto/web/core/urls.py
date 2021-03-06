from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("authenticate", views.authenticate, name="authenticate"),
    path("dashboard/matrizesCurriculares", views.matrizesCurriculares, name="matrizesCurriculares"),
    path("dashboard/getMatrizesCurriculares", views.getMatrizesCurriculares, name="getMatrizesCurriculares"),
    path("dashboard/disciplinas", views.disciplinas, name="disciplinas"),
    path("dashboard/getDisciplinas", views.getDisciplinas, name="getDisciplinas"),
    path("dashboard/getDisciplina", views.getDisciplina, name="getDisciplina"),
    path("dashboard/estatisticas", views.estatisticas, name="estatisticas")
]
