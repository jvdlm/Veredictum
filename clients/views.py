from django.contrib import messages
from django.contrib.messages import constants
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Clients


def clients(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    return render(
        request,
        "client_home.html",
        {"clients": Clients.objects.all()},
    )


def register_client(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        birthdate = request.POST.get("birthdate")
        document_id = request.POST.get("document_id")
        zip_code = request.POST.get("zip_code")
        adress = request.POST.get("adress")
        state = request.POST.get("states")
        city = request.POST.get("city")
        neighborhood = request.POST.get("neighborhood")
        role = request.POST.get("role")

        required = (
            name,
            number,
            birthdate,
            document_id,
            zip_code,
            adress,
            state,
            city,
            neighborhood,
            role,
        )
        if not all(required):
            messages.add_message(
                request,
                constants.ERROR,
                "Todos os campos são obrigatórios.",
            )
            return redirect(reverse("clients_register"))

        if Clients.objects.filter(name=name).exists():
            messages.add_message(request, constants.ERROR, "O nome já está em uso.")
            return redirect(reverse("clients_register"))

        if Clients.objects.filter(number=number).exists():
            messages.add_message(
                request,
                constants.ERROR,
                "O número de telefone já está em uso.",
            )
            return redirect(reverse("clients_register"))

        if Clients.objects.filter(document_id=document_id).exists():
            messages.add_message(
                request,
                constants.ERROR,
                "Este CPF/CNPJ já está registrado no sistema.",
            )
            return redirect(reverse("clients_register"))

        if Clients.objects.filter(zip_code=zip_code).exists():
            messages.add_message(request, constants.ERROR, "O CEP já está em uso.")
            return redirect(reverse("clients_register"))

        try:
            Clients.objects.create(
                name=name,
                number=number,
                birthdate=birthdate,
                document_id=document_id,
                zip_code=zip_code,
                adress=adress,
                state=state,
                city=city,
                neighborhood=neighborhood,
                role=role,
            )
        except IntegrityError:
            messages.add_message(
                request,
                constants.ERROR,
                "Não foi possível cadastrar: dados duplicados.",
            )
            return redirect(reverse("clients_register"))

        messages.add_message(request, constants.SUCCESS, "Cliente cadastrado com sucesso!")
        return redirect(reverse("clients_home"))

    return render(
        request,
        "client_register.html",
        {"ufs": Clients.UF_CHOICES},
    )


def edit_client(request, client_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    client = get_object_or_404(Clients, id=client_id)

    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        birthdate = request.POST.get("birthdate")
        document_id = request.POST.get("document_id")
        zip_code = request.POST.get("zip_code")
        adress = request.POST.get("adress")
        state = request.POST.get("state")
        city = request.POST.get("city")
        neighborhood = request.POST.get("neighborhood")
        role = request.POST.get("role")

        if not all(
            (name, number, birthdate, document_id, zip_code, adress, state, city, neighborhood, role)
        ):
            messages.add_message(
                request,
                constants.ERROR,
                "Todos os campos são obrigatórios.",
            )
            return redirect(reverse("client_edit", args=[client_id]))

        dup_doc = (
            Clients.objects.filter(document_id=document_id).exclude(pk=client.pk).exists()
        )
        if dup_doc:
            messages.add_message(
                request,
                constants.ERROR,
                "Este CPF/CNPJ já está registrado para outro cliente.",
            )
            return redirect(reverse("client_edit", args=[client_id]))

        client.name = name
        client.number = number
        client.birthdate = birthdate
        client.document_id = document_id
        client.zip_code = zip_code
        client.adress = adress
        client.state = state
        client.city = city
        client.neighborhood = neighborhood
        client.role = role
        client.save()

        messages.add_message(request, constants.SUCCESS, "Cliente atualizado com sucesso!")
        return redirect(reverse("clients_home"))

    return render(
        request,
        "edit_clients.html",
        {"client": client, "ufs": Clients.UF_CHOICES},
    )


def delete_client(request, client_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    client = get_object_or_404(Clients, id=client_id)
    client.delete()
    messages.add_message(request, constants.SUCCESS, "Cliente removido com sucesso!")
    return redirect(reverse("clients_home"))
