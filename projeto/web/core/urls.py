from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("login", views.login, name="login"),
    path("init_session", views.init_session, name="init_session")
]
