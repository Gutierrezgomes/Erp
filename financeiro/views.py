from django.shortcuts import render
from .models import Lancamento, PlanoContas
from django.utils import timezone
from django.db.models import Sum

def fina_view(request):
    hoje = timezone.now()
    
    # --- 1. CÁLCULO DO SALDO TOTAL ---
    total_entradas = Lancamento.objects.filter(
        tipo='CREDITO', 
        status='PAGO'
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    
    total_saidas = Lancamento.objects.filter(
        tipo='DEBITO', 
        status='PAGO'
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    
    saldo_atual = total_entradas - total_saidas

    # --- 2. MOVIMENTAÇÃO DO MÊS ATUAL ---
    receitas_mes = Lancamento.objects.filter(
        tipo='CREDITO', 
        status='PAGO',
        data_pagamento__month=hoje.month,
        data_pagamento__year=hoje.year
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    despesas_mes = Lancamento.objects.filter(
        tipo='DEBITO', 
        status='PAGO',
        data_pagamento__month=hoje.month,
        data_pagamento__year=hoje.year
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    # --- 3. CONTAS VENCIDAS ---
    contas_vencidas = Lancamento.objects.filter(
        tipo='DEBITO',
        status='ABERTO',
        data_vencimento__lt=hoje.date()
    ).count()

    # --- 4. LISTA DA TABELA ---
    lancamentos_recentes = Lancamento.objects.all().order_by('-data_vencimento')[:5]

    return render(request, 'index.html', {
        'saldo': saldo_atual,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'vencidas': contas_vencidas,
        'lancamentos': lancamentos_recentes,
        'hoje': hoje.date()
    })

def catego_view(request):
    # Buscamos os Planos de Contas para mostrar na tabela
    planos = PlanoContas.objects.all().order_by('codigo')
    
    return render(request, 'categorias.html', {
        'categorias': planos
    })
    
def lanca_view(request):
    # 1. Pega todos os lançamentos inicialmente
    dados = Lancamento.objects.all().order_by('-data_vencimento')
    
    # 2. Verifica se existe filtro na URL
    filtro_tipo = request.GET.get('tipo') 
    
    # 3. Aplica o filtro
    if filtro_tipo == 'receitas':
        dados = dados.filter(tipo='CREDITO')
    elif filtro_tipo == 'despesas':
        dados = dados.filter(tipo='DEBITO')
        
    # 4. Envia para o template correto
    return render(request, 'lancamentos.html', {
        'lancamentos': dados
    })