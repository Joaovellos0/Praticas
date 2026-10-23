from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("guitarra/<int:guitarra_id>/", views.detalhe_guitarra, name="detalhe_guitarra"),
    path("api/busca-guitarras/", views.buscar_guitarras, name="buscar_guitarras"),
]
