from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Marca, Guitarra


class HomeProductsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.marca_ibanez = Marca.objects.create(marca="Ibanez", slug="ibanez")
        self.marca_fender = Marca.objects.create(marca="Fender", slug="fender")

        # Criar 11 guitarras Ibanez (deve gerar 4 páginas: 3, 3, 3, 2 - superando a antiga trava de 9)
        for i in range(1, 12):
            Guitarra.objects.create(
                marca=self.marca_ibanez,
                modelo=f"Prestige RG {i}",
                descricao=f"Descrição técnica da guitarra Ibanez {i}",
                preco=Decimal("12500.00"),
                disponibilidade=True,
            )

        # Criar 4 guitarras Fender (deve gerar 2 páginas: 3, 1)
        for i in range(1, 5):
            Guitarra.objects.create(
                marca=self.marca_fender,
                modelo=f"Stratocaster Ultra {i}",
                descricao=f"Descrição da Fender {i}",
                preco=Decimal("15000.00"),
                disponibilidade=True,
            )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ECOMMERCE DE GUITARRAS")
        self.assertContains(response, "PRODUTO EM DESTAQUE")
        self.assertContains(response, "VITRINE")
        self.assertContains(response, "Ibanez")
        self.assertContains(response, "Fender")

        vitrine = response.context["vitrine_marcas"]
        ibanez_data = next(vm for vm in vitrine if vm["marca"].marca == "Ibanez")
        # Confirma que TODAS as 11 guitarras foram carregadas (sem trava de 9)
        self.assertEqual(ibanez_data["total_guitarras"], 11)
        self.assertEqual(ibanez_data["total_paginas"], 4)
        self.assertEqual(len(ibanez_data["paginas"][0]), 3)
        self.assertEqual(len(ibanez_data["paginas"][1]), 3)
        self.assertEqual(len(ibanez_data["paginas"][2]), 3)
        self.assertEqual(len(ibanez_data["paginas"][3]), 2)

        # Fender com 4 guitarras: 2 páginas (3 e 1)
        fender_data = next(vm for vm in vitrine if vm["marca"].marca == "Fender")
        self.assertEqual(fender_data["total_guitarras"], 4)
        self.assertEqual(fender_data["total_paginas"], 2)
        self.assertEqual(len(fender_data["paginas"][0]), 3)
        self.assertEqual(len(fender_data["paginas"][1]), 1)

    def test_buscar_guitarras_autocomplete(self):
        # Query curta (< 2 caracteres)
        res_short = self.client.get(reverse("buscar_guitarras") + "?q=a")
        self.assertEqual(res_short.status_code, 200)
        self.assertEqual(res_short.json()["resultados"], [])

        # Query por marca
        res_brand = self.client.get(reverse("buscar_guitarras") + "?q=Ibanez")
        self.assertEqual(res_brand.status_code, 200)
        data_brand = res_brand.json()["resultados"]
        self.assertGreater(len(data_brand), 0)
        self.assertTrue(all("Ibanez" in item["marca"] for item in data_brand))
        self.assertIn("url", data_brand[0])
        self.assertIn("preco_formatado", data_brand[0])

        # Query por modelo
        res_model = self.client.get(reverse("buscar_guitarras") + "?q=Stratocaster")
        self.assertEqual(res_model.status_code, 200)
        data_model = res_model.json()["resultados"]
        self.assertEqual(len(data_model), 4)

    def test_detalhe_guitarra(self):
        guitarra = Guitarra.objects.filter(marca=self.marca_ibanez).first()
        response = self.client.get(reverse("detalhe_guitarra", args=[guitarra.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, guitarra.modelo)
        self.assertContains(response, "Ibanez")
        self.assertContains(response, "ADICIONAR AO CARRINHO")

        # 404 para ID inexistente
        response_404 = self.client.get(reverse("detalhe_guitarra", args=[99999]))
        self.assertEqual(response_404.status_code, 404)

    def test_cadastro_clean_header(self):
        response = self.client.get(reverse("cadastro"))
        self.assertEqual(response.status_code, 200)
        # Cabeçalho limpo não deve conter a barra de busca nem o menu nav no header
        self.assertNotContains(response, 'id="search"')
        self.assertNotContains(response, 'header_nav')
        self.assertContains(response, "header_clean")
        self.assertContains(response, "CRIE SUA CONTA NO MÙSIC SHOP")
        self.assertContains(response, "FINALIZAR CADASTRO")
