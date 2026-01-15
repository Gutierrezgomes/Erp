from django.contrib import admin
from django.utils.html import format_html
# Importamos os modelos novos corretamente
from .models import Cliente, Fornecedor, PlanoContas, Lancamento

# --- Cadastros Básicos ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf_cnpj', 'telefone', 'email')
    search_fields = ('nome', 'cpf_cnpj')

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf_cnpj', 'telefone', 'email')
    search_fields = ('nome', 'cpf_cnpj')

# --- Financeiro ---

@admin.register(PlanoContas)
class PlanoContasAdmin(admin.ModelAdmin):
    # Substitui o antigo CategoriaAdmin
    list_display = ('codigo', 'nome', 'tipo', 'ativo')
    list_filter = ('tipo', 'ativo')
    search_fields = ('codigo', 'nome')
    ordering = ('codigo',)

@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao', 
        'plano_conta', 
        'valor_formatado', 
        'data_vencimento', 
        'tipo_badge', 
        'status_badge'
    )
    
    list_filter = (
        'status', 
        'tipo', 
        'data_vencimento', 
        'plano_conta'
    )
    
    search_fields = ('descricao', 'valor')
    date_hierarchy = 'data_vencimento'

    # Campos do formulário organizados
    fieldsets = (
        ('Dados Principais', {
            'fields': ('descricao', 'valor', 'tipo', 'plano_conta')
        }),
        ('Pessoas', {
            'fields': ('cliente', 'fornecedor'),
            'description': 'Selecione Cliente (se for receita) ou Fornecedor (se for despesa).'
        }),
        ('Datas e Status', {
            'fields': (('data_vencimento', 'data_pagamento'), 'status')
        }),
        ('Sistema', {
            'fields': ('origem_modulo', 'origem_id'),
            'classes': ('collapse',),
        }),
    )

    # --- Funções visuais para deixar o admin bonito ---

    @admin.display(description='Valor')
    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @admin.display(description='Tipo')
    def tipo_badge(self, obj):
        # Crédito = Verde, Débito = Vermelho
        cor = 'green' if obj.tipo == 'CREDITO' else 'red'
        label = 'Receita' if obj.tipo == 'CREDITO' else 'Despesa'
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 10px; font-size: 10px;">{}</span>',
            cor,
            label
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        cores = {
            'ABERTO': 'orange',
            'PAGO': 'green',
            'CANCELADO': 'gray',
        }
        cor = cores.get(obj.status, 'black')
        return format_html(
            '<strong style="color: {};">{}</strong>',
            cor,
            obj.get_status_display()
        )