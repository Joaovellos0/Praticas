from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.logar, name="login"),
    path("logout/", views.deslogar, name="logout"),
    path("cadastro/", views.cadastrar, name="cadastro"),
]
