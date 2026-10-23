from django.urls import path
from . import views

urlpatterns = [
    path("carrinho/", views.carrinho, name="carrinho"),
    path("carrinho/adicionar/<int:guitarra_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("carrinho/remover/<int:guitarra_id>/", views.remover_do_carrinho, name="remover_do_carrinho"),
    path("carrinho/atualizar/<int:guitarra_id>/", views.atualizar_carrinho, name="atualizar_carrinho"),
    path("carrinho/limpar/", views.limpar_carrinho, name="limpar_carrinho"),
]
