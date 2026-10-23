from django.contrib import admin
from .models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "telefone", "cep", "cidade", "estado")
    search_fields = ("usuario__username", "usuario__email", "cep", "cidade", "logradouro")


admin.site.register(Usuario, UsuarioAdmin)
