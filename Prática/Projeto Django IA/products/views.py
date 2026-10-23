from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Marca, Guitarra


def home(request):
    """
    View principal da loja.
    Consulta estritamente os objetos reais cadastrados no banco de dados.
    """
    # Novas adições: 3 guitarras reais mais recentes
    guitarras_adicionadas = Guitarra.objects.filter(disponibilidade=True).order_by("-id")[:3]

    # Carrossel Rotativo de Banners: todas as guitarras disponíveis com banner cadastrado
    guitarras_banner = list(
        Guitarra.objects.filter(disponibilidade=True)
        .exclude(banner="")
        .exclude(banner__isnull=True)
        .select_related("marca")
        .order_by("-id")
    )
    # Fallback se nenhuma tiver banner cadastrado
    if not guitarras_banner:
        mais_recente = (
            Guitarra.objects.filter(disponibilidade=True)
            .select_related("marca")
            .order_by("-id")
            .first()
        )
        if mais_recente:
            guitarras_banner = [mais_recente]

    # Para manter retrocompatibilidade com qualquer referência singular
    guitarra_banner = guitarras_banner[0] if guitarras_banner else None

    # Marcas para o filtro da Vitrine
    marcas = Marca.objects.all().order_by("marca")

    # Estrutura da Vitrine: TODAS as guitarras cadastradas por marca (sem trava de 9 ou 3 páginas),
    # agrupadas em páginas de exatamente 3 guitarras por bloco
    vitrine_marcas = []
    for marca in marcas:
        guitarras = list(
            Guitarra.objects.filter(marca=marca, disponibilidade=True).order_by("-id")
        )
        paginas = [guitarras[i : i + 3] for i in range(0, len(guitarras), 3)]
        vitrine_marcas.append(
            {
                "marca": marca,
                "total_guitarras": len(guitarras),
                "total_paginas": len(paginas),
                "paginas": paginas,
            }
        )

    return render(
        request,
        "home.html",
        {
            "guitarras_adicionadas": guitarras_adicionadas,
            "guitarra_banner": guitarra_banner,
            "guitarras_banner": guitarras_banner,
            "marcas": marcas,
            "vitrine_marcas": vitrine_marcas,
        },
    )


def buscar_guitarras(request):
    """
    Endpoint JSON leve para autocompletar da barra de pesquisa em tempo real.
    Filtra por nome do modelo ou nome da marca utilizando icontains.
    """
    termo = request.GET.get("q", "").strip()
    if not termo or len(termo) < 2:
        return JsonResponse({"resultados": []})

    guitarras = (
        Guitarra.objects.filter(disponibilidade=True)
        .filter(Q(modelo__icontains=termo) | Q(marca__marca__icontains=termo))
        .select_related("marca")
        .order_by("-id")[:8]
    )

    resultados = []
    for g in guitarras:
        resultados.append(
            {
                "id": g.id,
                "modelo": g.modelo,
                "marca": g.marca.marca,
                "nome_completo": f"{g.marca.marca} {g.modelo}",
                "preco": float(g.preco),
                "preco_formatado": f"R$ {g.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "imagem_url": g.ilustracao.url if g.ilustracao else "",
                "url": f"/guitarra/{g.id}/",
            }
        )

    return JsonResponse({"resultados": resultados})


def detalhe_guitarra(request, guitarra_id):
    """
    View de detalhe individual de uma guitarra cadastrada.
    Exibe dados técnicos, ilustrações, galeria e instrumentos relacionados da mesma marca
    paginados em blocos de até 3 guitarras.
    """
    guitarra = get_object_or_404(
        Guitarra.objects.select_related("marca"), id=guitarra_id
    )
    imagens_galeria = guitarra.imagens.all()
    
    # Todas as outras guitarras ativas da mesma marca
    guitarras_relacionadas_lista = list(
        Guitarra.objects.filter(marca=guitarra.marca, disponibilidade=True)
        .exclude(id=guitarra.id)
        .order_by("-id")
    )
    
    # Agrupadas em páginas de exatamente 3 guitarras por bloco
    paginas_relacionadas = [
        guitarras_relacionadas_lista[i : i + 3]
        for i in range(0, len(guitarras_relacionadas_lista), 3)
    ]

    return render(
        request,
        "detalhe.html",
        {
            "guitarra": guitarra,
            "imagens_galeria": imagens_galeria,
            "guitarras_relacionadas": guitarras_relacionadas_lista,
            "paginas_relacionadas": paginas_relacionadas,
            "total_paginas_relacionadas": len(paginas_relacionadas),
        },
    )
