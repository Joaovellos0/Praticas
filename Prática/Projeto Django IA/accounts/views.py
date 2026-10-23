from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Usuario


def cadastrar(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        cep = request.POST.get("cep", "").strip()
        logradouro = request.POST.get("logradouro", "").strip()
        bairro = request.POST.get("bairro", "").strip()
        cidade = request.POST.get("cidade", "").strip()
        estado = request.POST.get("estado", "").strip()
        numero = request.POST.get("numero", "").strip()
        complemento = request.POST.get("complemento", "").strip()

        if not nome or not email or not senha:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios (Nome, E-mail e Senha).")
            return render(request, "cadastro.html", {"form_data": request.POST})

        if User.objects.filter(username=nome).exists():
            messages.error(request, "Este nome de usuário já está em uso. Por favor, escolha outro.")
            return render(request, "cadastro.html", {"form_data": request.POST})

        try:
            usuario = User.objects.create_user(username=nome, email=email, password=senha)
            Usuario.objects.create(
                usuario=usuario,
                telefone=telefone[:9],
                cep=cep,
                logradouro=logradouro,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                numero=numero,
                complemento=complemento,
            )
            messages.success(request, "Cadastro realizado com sucesso! Faça seu login.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Erro ao criar conta: {str(e)}")
            return render(request, "cadastro.html", {"form_data": request.POST})

    return render(request, "cadastro.html")


def logar(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        senha = request.POST.get("senha", "").strip()
        next_url = request.POST.get("next") or request.GET.get("next") or "home"

        is_ajax = (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            or request.POST.get("ajax") == "1"
        )

        usuario = authenticate(request, username=nome, password=senha)
        if usuario is not None:
            login(request, usuario)
            if is_ajax:
                return JsonResponse({"status": "success", "username": usuario.username, "redirect_url": next_url})
            messages.success(request, f"Bem-vindo de volta, {usuario.username}!")
            return redirect(next_url)
        else:
            msg_erro = "Usuário ou senha incorretos."
            if is_ajax:
                return JsonResponse({"status": "error", "message": msg_erro}, status=400)
            messages.error(request, msg_erro)
            return render(request, "login.html", {"nome": nome})
    
    return render(request, "login.html")


def deslogar(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("home")
