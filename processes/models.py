from django.db import models

from clients.models import Clients


class Process(models.Model):
    RISCO_CHOICES = (
        ("B", "Baixo"),
        ("M", "Médio"),
        ("A", "Alto"),
    )

    STATUS_CHOICES = (
        ("em_andamento", "Em andamento"),
        ("suspenso", "Suspenso"),
        ("arquivado", "Arquivado"),
        ("encerrado", "Encerrado"),
    )

    UF_CHOICES = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    )

    INSTANCIA_CHOICES = (
        ("1", "Primeira Instância"),
        ("2", "Segunda Instância"),
        ("3", "Tribunais Superiores"),
    )

    tipo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    tipo_acao = models.CharField(max_length=200)
    cliente = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        related_name="processos",
    )
    contrario = models.CharField(max_length=200)
    numero_pasta = models.CharField(max_length=100)
    numero_cnj = models.CharField(max_length=100, unique=True)
    detalhes_pasta = models.TextField()
    advogado = models.CharField(max_length=200)
    push_andamentos = models.CharField(max_length=200)
    comarca = models.CharField(max_length=200)
    juiz = models.CharField(max_length=200)
    risco = models.CharField(max_length=1, choices=RISCO_CHOICES, default="M")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="em_andamento",
    )
    tribunal = models.CharField(max_length=200)
    uf = models.CharField(max_length=2, choices=UF_CHOICES, default="SP")
    instancia = models.CharField(max_length=1, choices=INSTANCIA_CHOICES, default="1")
    vara = models.CharField(max_length=200)
    valor_causa = models.DecimalField(max_digits=10, decimal_places=2)
    valor_possivel = models.DecimalField(max_digits=10, decimal_places=2)
    valor_provisionado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo
