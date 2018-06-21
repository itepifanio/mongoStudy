from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("authenticate", views.authenticate, name="authenticate"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/getMatrizesCurriculares", views.getMatrizesCurriculares, name="getMatrizesCurriculares"),
    path("dashboard/disciplinas", views.disciplinas, name="disciplinas"),
    path("dashboard/getDisciplinas", views.getDisciplinas, name="getDisciplinas"),
    path("dashboard/estatisticas", views.estatisticas, name="estatisticas")
]
