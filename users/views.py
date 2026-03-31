from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            messages.add_message(request, constants.ERROR, "As senhas não coincidem")
            return render(
                request,
                "register.html",
                {"username": username, "email": email},
            )

        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "Email já cadastrado")
            return render(request, "register.html", {"username": username})

        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "Nome já cadastrado")
            return render(request, "register.html", {"email": email})

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect("login")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("app")
        messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
        return render(request, "login.html", {"username": username})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    return render(request, "home.html")


def app(request):
    if request.user.is_authenticated:
        return render(request, "app.html", {"user": request.user})
    return redirect("home")
