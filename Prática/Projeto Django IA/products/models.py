from django.db import models


# Create your models here.
class Marca(models.Model):
    marca = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.marca


class Guitarra(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=38)
    descricao = models.TextField()
    ilustracao = models.ImageField(upload_to="guitarras", blank=True, null=True)
    banner = models.ImageField(upload_to="banners", blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidade = models.BooleanField(default=True)
    madeiras = models.CharField(max_length=200, blank=True, null=True)
    captadores = models.CharField(max_length=200, blank=True, null=True)
    ponte_trastes = models.CharField(max_length=200, blank=True, null=True)
    acabamento = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"


class ImagemGuitarra(models.Model):
    guitarra = models.ForeignKey(
        Guitarra, on_delete=models.CASCADE, related_name="imagens"
    )
    imagem = models.ImageField(upload_to="guitarras/detalhes")

    def __str__(self):
        return f"   Imagem de {self.guitarra.modelo}"
