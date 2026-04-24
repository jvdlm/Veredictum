from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from clients.models import Clients
from .models import Process


def create_test_client():
    return Clients.objects.create(
        name="Cliente Teste",
        number="11999999999",
        birthdate=timezone.now(),
        role="Pessoa Física",
        zip_code="01310-100",
        adress="Av. Paulista, 1000",
        state="SP",
        city="São Paulo",
        neighborhood="Bela Vista",
        document_id="123.456.789-00",
    )


def create_test_process(cliente, numero_cnj="0001234-56.2024.8.26.0001", status="em_andamento"):
    return Process.objects.create(
        tipo="Cível",
        titulo="Processo Teste",
        tipo_acao="Ação de Cobrança",
        cliente=cliente,
        contrario="Parte Contrária",
        numero_pasta="001",
        numero_cnj=numero_cnj,
        detalhes_pasta="Detalhes do processo",
        advogado="Dr. Advogado",
        push_andamentos="push@test.com",
        comarca="São Paulo",
        juiz="Dr. Juiz",
        risco="M",
        status=status,
        tribunal="TJSP",
        uf="SP",
        instancia="1",
        vara="1ª Vara Cível",
        valor_causa="10000.00",
        valor_possivel="8000.00",
        valor_provisionado="5000.00",
    )


class ProcessListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.cliente = create_test_client()
        self.process = create_test_process(self.cliente)

    def test_redireciona_nao_autenticado(self):
        response = self.client.get(reverse("processes"))
        self.assertRedirects(response, reverse("login"))

    def test_lista_processos_autenticado(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("processes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Processo Teste")

    def test_filtro_por_status(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("processes") + "?status=em_andamento")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Processo Teste")

    def test_filtro_status_sem_resultado(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("processes") + "?status=arquivado")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum processo encontrado")

    def test_filtro_por_titulo(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("processes") + "?busca=Processo Teste")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Processo Teste")


class ArchiveProcessTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.cliente = create_test_client()
        self.process = create_test_process(self.cliente, numero_cnj="9999999-99.2024.8.26.0001")

    def test_arquivar_processo(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("process_archive", args=[self.process.id]))
        self.process.refresh_from_db()
        self.assertEqual(self.process.status, "arquivado")
        self.assertRedirects(response, reverse("processes"))

    def test_arquivar_redireciona_nao_autenticado(self):
        response = self.client.get(reverse("process_archive", args=[self.process.id]))
        self.assertRedirects(response, reverse("login"))