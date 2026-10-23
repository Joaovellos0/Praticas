from django.contrib import admin
from .models import Marca, Guitarra, ImagemGuitarra


# Register your models here.
class ImagemGuitarraInline(admin.TabularInline):
    model = ImagemGuitarra
    extra = 1


class GuitarraAdmin(admin.ModelAdmin):
    list_display = ("modelo", "marca", "preco", "disponibilidade")
    list_filter = ("marca", "disponibilidade")
    search_fields = ("modelo", "marca__marca", "madeiras", "captadores")
    inlines = [ImagemGuitarraInline]
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("marca", "modelo", "preco", "disponibilidade", "descricao")
        }),
        ("Imagens", {
            "fields": ("ilustracao", "banner")
        }),
        ("Especificações Técnicas", {
            "fields": ("madeiras", "captadores", "ponte_trastes", "acabamento"),
            "description": "Especificações detalhadas para exibição na página de detalhes do produto."
        }),
    )


admin.site.register(Marca)
admin.site.register(Guitarra, GuitarraAdmin)
