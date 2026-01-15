from django.db import models

# --- CADASTROS ---

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.nome

    class Meta:
        # CORREÇÃO: Use underline (_) em vez de ponto (.)
        db_table = 'cadastros_clientes' 
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'cadastros_fornecedores' # Correção aqui
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"


# --- FINANCEIRO ---

class PlanoContas(models.Model):
    TIPO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]

    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    class Meta:
        db_table = 'financeiro_plano_contas' # Correção aqui
        verbose_name = "Plano de Contas"
        verbose_name_plural = "Planos de Contas"


class Lancamento(models.Model):
    TIPO_LANCAMENTO_CHOICES = [
        ('CREDITO', 'Crédito (Receber)'),
        ('DEBITO', 'Débito (Pagar)'),
    ]

    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
    ]

    ORIGEM_CHOICES = [
        ('VENDAS', 'Vendas'),
        ('COMPRAS', 'Compras'),
        ('MANUAL', 'Manual'),
    ]

    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_LANCAMENTO_CHOICES, blank=True, null=True)
    
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    # FKs (Relacionamentos)
    plano_conta = models.ForeignKey(
        PlanoContas, 
        on_delete=models.PROTECT, 
        null=True, blank=True
    )

    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )

    fornecedor = models.ForeignKey(
        Fornecedor, 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )

    origem_modulo = models.CharField(max_length=50, choices=ORIGEM_CHOICES, blank=True, null=True)
    origem_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    class Meta:
        db_table = 'financeiro_lancamentos' # Correção aqui
        verbose_name = "Lançamento"
        verbose_name_plural = "Lançamentos"
        ordering = ['data_vencimento']