from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Guitarra
from .cart import Cart


def carrinho(request):
    cart = Cart(request)
    return render(
        request,
        "carrinho.html",
        {
            "cart": cart,
            "cart_total_items": len(cart),
            "cart_total_price": cart.get_total_price(),
        },
    )


def adicionar_ao_carrinho(request, guitarra_id):
    guitarra = get_object_or_404(Guitarra, id=guitarra_id)
    cart = Cart(request)
    quantidade = int(request.POST.get("quantidade", 1) if request.method == "POST" else request.GET.get("quantidade", 1))
    
    cart.add(guitarra=guitarra, quantidade=quantidade)

    mensagem = f"{guitarra.marca} {guitarra.modelo} adicionada ao carrinho!"

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.GET.get("ajax") == "1"
        or request.POST.get("ajax") == "1"
    )

    if is_ajax:
        return JsonResponse(
            {
                "status": "success",
                "message": mensagem,
                "total_items": len(cart),
                "total_price": float(cart.get_total_price()),
                "item_id": guitarra.id,
            }
        )

    messages.success(request, mensagem)
    next_url = request.POST.get("next") or request.GET.get("next") or request.META.get("HTTP_REFERER") or "carrinho"
    return redirect(next_url)


def remover_do_carrinho(request, guitarra_id):
    cart = Cart(request)
    cart.remove(guitarra_id)

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.GET.get("ajax") == "1"
        or request.POST.get("ajax") == "1"
    )

    if is_ajax:
        return JsonResponse(
            {
                "status": "success",
                "message": "Produto removido do carrinho.",
                "total_items": len(cart),
                "total_price": float(cart.get_total_price()),
                "item_id": guitarra_id,
            }
        )

    messages.info(request, "Produto removido do carrinho.")
    return redirect("carrinho")


def atualizar_carrinho(request, guitarra_id):
    guitarra = get_object_or_404(Guitarra, id=guitarra_id)
    cart = Cart(request)

    quantidade = request.POST.get("quantidade") or request.GET.get("quantidade")
    action = request.POST.get("action") or request.GET.get("action")

    if action == "increase":
        cart.add(guitarra=guitarra, quantidade=1)
    elif action == "decrease":
        cart.add(guitarra=guitarra, quantidade=-1)
    elif quantidade is not None:
        try:
            qtd = int(quantidade)
            if qtd > 0:
                cart.update(guitarra_id=guitarra.id, quantidade=qtd)
            else:
                cart.remove(guitarra_id)
        except ValueError:
            pass

    # Obter dados atualizados do item
    current_item = None
    for item in cart:
        if item["id"] == guitarra.id:
            current_item = item
            break

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.GET.get("ajax") == "1"
        or request.POST.get("ajax") == "1"
    )

    if is_ajax:
        return JsonResponse(
            {
                "status": "success",
                "total_items": len(cart),
                "total_price": float(cart.get_total_price()),
                "item_subtotal": float(current_item["subtotal"]) if current_item else 0.0,
                "item_quantidade": current_item["quantidade"] if current_item else 0,
                "item_id": guitarra.id,
            }
        )

    return redirect("carrinho")


def limpar_carrinho(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Seu carrinho foi esvaziado.")
    return redirect("carrinho")
