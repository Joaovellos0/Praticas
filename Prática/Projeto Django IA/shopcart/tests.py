from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Marca, Guitarra
from shopcart.cart import Cart


class ShopCartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.marca = Marca.objects.create(marca="Ibanez", slug="ibanez")
        self.guitarra = Guitarra.objects.create(
            marca=self.marca,
            modelo="Prestige RGA",
            descricao="Guitarra top de linha",
            preco=Decimal("15000.00"),
            disponibilidade=True,
        )

    def test_carrinho_vazio_view(self):
        response = self.client.get(reverse("carrinho"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seu carrinho está vazio")

    def test_adicionar_ao_carrinho_ajax(self):
        response = self.client.get(
            reverse("adicionar_ao_carrinho", args=[self.guitarra.id]),
            {"ajax": "1"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_items"], 1)
        self.assertEqual(data["total_price"], 15000.0)

    def test_atualizar_e_remover_carrinho(self):
        # Adiciona
        self.client.get(reverse("adicionar_ao_carrinho", args=[self.guitarra.id]))
        
        # Aumenta quantidade
        response = self.client.get(
            reverse("atualizar_carrinho", args=[self.guitarra.id]),
            {"action": "increase", "ajax": "1"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_items"], 2)
        self.assertEqual(data["total_price"], 30000.0)

        # Remove
        response = self.client.get(
            reverse("remover_do_carrinho", args=[self.guitarra.id]),
            {"ajax": "1"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_items"], 0)
