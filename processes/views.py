from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.messages import constants
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from clients.models import Clients

from .models import Process


def process(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    qs = Process.objects.select_related("cliente").all()

    status_filter = request.GET.get("status") or ""
    risco_filter = request.GET.get("risco") or ""
    uf_filter = request.GET.get("uf") or ""
    busca = request.GET.get("busca") or ""

    if status_filter:
        qs = qs.filter(status=status_filter)
    if risco_filter:
        qs = qs.filter(risco=risco_filter)
    if uf_filter:
        qs = qs.filter(uf=uf_filter)
    if busca:
        qs = qs.filter(titulo__icontains=busca)

    return render(
        request,
        "processes.html",
        {
            "processes": qs,
            "status_filter": status_filter,
            "risco_filter": risco_filter,
            "uf_filter": uf_filter,
            "busca": busca,
            "status_choices": Process.STATUS_CHOICES,
            "risco_choices": Process.RISCO_CHOICES,
            "uf_choices": Process.UF_CHOICES,
        },
    )


def register_process(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        titulo = request.POST.get("titulo")
        tipo_acao = request.POST.get("tipo_acao")
        cliente_id = request.POST.get("cliente_id")
        contrario = request.POST.get("contrario")
        numero_pasta = request.POST.get("numero_pasta")
        numero_cnj = (request.POST.get("numero_cnj") or "").strip()
        detalhes_pasta = request.POST.get("detalhes_pasta")
        advogado = request.POST.get("advogado")
        push_andamentos = request.POST.get("push_andamentos")
        comarca = request.POST.get("comarca")
        juiz = request.POST.get("juiz")
        risco = request.POST.get("risco")
        status = request.POST.get("status")
        tribunal = request.POST.get("tribunal")
        uf = request.POST.get("uf")
        instancia = request.POST.get("instancia")
        vara = request.POST.get("vara")
        valor_causa = request.POST.get("valor_causa")
        valor_possivel = request.POST.get("valor_possivel")
        valor_provisionado = request.POST.get("valor_provisionado")

        required = (
            tipo,
            titulo,
            tipo_acao,
            cliente_id,
            contrario,
            numero_pasta,
            numero_cnj,
            detalhes_pasta,
            advogado,
            push_andamentos,
            comarca,
            juiz,
            risco,
            status,
            tribunal,
            uf,
            instancia,
            vara,
            valor_causa,
            valor_possivel,
            valor_provisionado,
        )
        if not all(required):
            messages.add_message(request, constants.ERROR, "Todos os campos são obrigatórios.")
            return redirect(reverse("process_register"))

        if Process.objects.filter(numero_cnj=numero_cnj).exists():
            messages.add_message(
                request,
                constants.ERROR,
                "Já existe um processo cadastrado com este número (CNJ).",
            )
            return redirect(reverse("process_register"))

        try:
            vals = [valor_causa, valor_possivel, valor_provisionado]
            valor_causa_d, valor_possivel_d, valor_provisionado_d = (
                Decimal(str(v).replace(",", ".")) for v in vals
            )
        except (InvalidOperation, ValueError):
            messages.add_message(
                request,
                constants.ERROR,
                "Os valores financeiros devem ser números válidos.",
            )
            return redirect(reverse("process_register"))

        if min(valor_causa_d, valor_possivel_d, valor_provisionado_d) < 0:
            messages.add_message(
                request,
                constants.ERROR,
                "Os valores financeiros não podem ser negativos.",
            )
            return redirect(reverse("process_register"))

        cliente = Clients.objects.filter(pk=cliente_id).first()
        if cliente is None:
            messages.add_message(request, constants.ERROR, "Cliente não encontrado.")
            return redirect(reverse("process_register"))

        try:
            Process.objects.create(
                tipo=tipo,
                titulo=titulo,
                tipo_acao=tipo_acao,
                cliente=cliente,
                contrario=contrario,
                numero_pasta=numero_pasta,
                numero_cnj=numero_cnj,
                detalhes_pasta=detalhes_pasta,
                advogado=advogado,
                push_andamentos=push_andamentos,
                comarca=comarca,
                juiz=juiz,
                risco=risco,
                status=status,
                tribunal=tribunal,
                uf=uf,
                instancia=instancia,
                vara=vara,
                valor_causa=valor_causa_d,
                valor_possivel=valor_possivel_d,
                valor_provisionado=valor_provisionado_d,
            )
        except IntegrityError:
            messages.add_message(
                request,
                constants.ERROR,
                "Não foi possível cadastrar: número de processo duplicado.",
            )
            return redirect(reverse("process_register"))

        messages.add_message(request, constants.SUCCESS, "Processo cadastrado com sucesso!")
        return redirect(reverse("processes"))

    return render(
        request,
        "process_register.html",
        {
            "riscos": Process.RISCO_CHOICES,
            "ufs": Process.UF_CHOICES,
            "instacias": Process.INSTANCIA_CHOICES,
            "statuses": Process.STATUS_CHOICES,
            "clients": Clients.objects.all(),
        },
    )


def edit_process(request, process_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    proc = get_object_or_404(Process.objects.select_related("cliente"), id=process_id)

    if request.method == "POST":
        proc.tipo = request.POST.get("tipo")
        proc.titulo = request.POST.get("titulo")
        proc.tipo_acao = request.POST.get("tipo_acao")
        cliente_id = request.POST.get("cliente_id")
        proc.contrario = request.POST.get("contrario")
        proc.numero_pasta = request.POST.get("numero_pasta")
        novo_cnj = (request.POST.get("numero_cnj") or "").strip()
        proc.detalhes_pasta = request.POST.get("detalhes_pasta")
        proc.advogado = request.POST.get("advogado")
        proc.push_andamentos = request.POST.get("push_andamentos")
        proc.comarca = request.POST.get("comarca")
        proc.juiz = request.POST.get("juiz")
        proc.risco = request.POST.get("risco")
        proc.status = request.POST.get("status")
        proc.tribunal = request.POST.get("tribunal")
        proc.uf = request.POST.get("uf")
        proc.instancia = request.POST.get("instancia")
        proc.vara = request.POST.get("vara")

        if Process.objects.filter(numero_cnj=novo_cnj).exclude(pk=proc.pk).exists():
            messages.add_message(
                request,
                constants.ERROR,
                "Já existe outro processo com este número (CNJ).",
            )
            return render(
                request,
                "edit_process.html",
                {
                    "process": proc,
                    "riscos": Process.RISCO_CHOICES,
                    "ufs": Process.UF_CHOICES,
                    "instacias": Process.INSTANCIA_CHOICES,
                    "statuses": Process.STATUS_CHOICES,
                    "clients": Clients.objects.all(),
                },
            )

        proc.numero_cnj = novo_cnj

        cliente = Clients.objects.filter(pk=cliente_id).first()
        if cliente is None:
            messages.add_message(request, constants.ERROR, "Cliente não encontrado.")
            return render(
                request,
                "edit_process.html",
                {
                    "process": proc,
                    "riscos": Process.RISCO_CHOICES,
                    "ufs": Process.UF_CHOICES,
                    "instacias": Process.INSTANCIA_CHOICES,
                    "statuses": Process.STATUS_CHOICES,
                    "clients": Clients.objects.all(),
                },
            )
        proc.cliente = cliente

        try:
            raw = [
                request.POST.get("valor_causa"),
                request.POST.get("valor_possivel"),
                request.POST.get("valor_provisionado"),
            ]
            normalized = [str(v).replace(",", ".") for v in raw]
            vc, vp, vpr = (Decimal(v) for v in normalized)
        except (InvalidOperation, ValueError):
            messages.add_message(
                request,
                constants.ERROR,
                "Os valores financeiros devem ser números válidos.",
            )
            return render(
                request,
                "edit_process.html",
                {
                    "process": proc,
                    "riscos": Process.RISCO_CHOICES,
                    "ufs": Process.UF_CHOICES,
                    "instacias": Process.INSTANCIA_CHOICES,
                    "statuses": Process.STATUS_CHOICES,
                    "clients": Clients.objects.all(),
                },
            )

        if min(vc, vp, vpr) < 0:
            messages.add_message(
                request,
                constants.ERROR,
                "Os valores financeiros não podem ser negativos.",
            )
            return render(
                request,
                "edit_process.html",
                {
                    "process": proc,
                    "riscos": Process.RISCO_CHOICES,
                    "ufs": Process.UF_CHOICES,
                    "instacias": Process.INSTANCIA_CHOICES,
                    "statuses": Process.STATUS_CHOICES,
                    "clients": Clients.objects.all(),
                },
            )

        proc.valor_causa = vc
        proc.valor_possivel = vp
        proc.valor_provisionado = vpr

        try:
            proc.save()
        except IntegrityError:
            messages.add_message(
                request,
                constants.ERROR,
                "Não foi possível salvar: número de processo duplicado.",
            )
            return render(
                request,
                "edit_process.html",
                {
                    "process": proc,
                    "riscos": Process.RISCO_CHOICES,
                    "ufs": Process.UF_CHOICES,
                    "instacias": Process.INSTANCIA_CHOICES,
                    "statuses": Process.STATUS_CHOICES,
                    "clients": Clients.objects.all(),
                },
            )

        messages.add_message(request, constants.SUCCESS, "Processo atualizado com sucesso!")
        return redirect(reverse("processes"))

    return render(
        request,
        "edit_process.html",
        {
            "process": proc,
            "riscos": Process.RISCO_CHOICES,
            "ufs": Process.UF_CHOICES,
            "instacias": Process.INSTANCIA_CHOICES,
            "statuses": Process.STATUS_CHOICES,
            "clients": Clients.objects.all(),
        },
    )


def delete_process(request, process_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    proc = get_object_or_404(Process, id=process_id)
    proc.delete()
    messages.add_message(request, constants.SUCCESS, "Processo removido com sucesso!")
    return redirect(reverse("processes"))


def process_reports(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    qs = Process.objects.select_related("cliente").all()
    status_filter = request.GET.get("status") or ""

    if status_filter:
        qs = qs.filter(status=status_filter)

    status_choices = Process.STATUS_CHOICES
    has_any = Process.objects.exists()

    return render(
        request,
        "process_reports.html",
        {
            "processes": qs,
            "status_filter": status_filter,
            "status_choices": status_choices,
            "has_any_processes": has_any,
        },
    )

def archive_process(request, process_id):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    proc = get_object_or_404(Process, id=process_id)
    proc.status = "arquivado"
    proc.save()
    messages.add_message(request, constants.SUCCESS, "Processo arquivado com sucesso!")
    return redirect(reverse("processes"))