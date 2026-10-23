from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Usuario


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cadastro_render_e_header_condicional(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEqual(response.status_code, 200)
        # Oculta carrinho e usuário no header da página de cadastro
        self.assertNotContains(response, 'id="cart_badge"')
        self.assertNotContains(response, 'id="user_btn"')
        self.assertContains(response, "CRIE SUA CONTA NO MÙSIC SHOP")

    def test_cadastro_post_sucesso(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "nome": "guitarhero",
                "email": "hero@music.com",
                "senha": "password123",
                "telefone": "999998888",
                "pais": "Brasil",
                "estado": "SP",
                "cidade": "São Paulo",
                "bairro": "Pinheiros",
                "numero": "500",
                "complemento": "Apto 12",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="guitarhero").exists())
        self.assertTrue(Usuario.objects.filter(usuario__username="guitarhero").exists())

    def test_login_post_e_header_condicional(self):
        User.objects.create_user(username="testuser", password="secretpassword")

        # GET login
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="cart_badge"')
        self.assertNotContains(response, 'id="user_btn"')

        # POST login
        response = self.client.post(
            reverse("login"),
            {"nome": "testuser", "senha": "secretpassword"},
        )
        self.assertEqual(response.status_code, 302)
