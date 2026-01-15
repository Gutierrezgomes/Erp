// Dados simulados (Mock) baseados no seu Models.py simples
const lancamentos = [
    { id: 1, descricao: "Venda de Serviço", valor: 1500.00, tipo: "R", data: "2026-01-12", pago: true, categoria: "Serviços" },
    { id: 2, descricao: "Material de Escritório", valor: 200.00, tipo: "D", data: "2026-01-13", pago: true, categoria: "Despesas" },
    { id: 3, descricao: "Internet", valor: 120.00, tipo: "D", data: "2026-01-20", pago: false, categoria: "Contas Fixas" },
    { id: 4, descricao: "Consultoria Extra", valor: 800.00, tipo: "R", data: "2026-01-25", pago: false, categoria: "Serviços" },
];

// Formatação Moeda
const formatarMoeda = (val) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

document.addEventListener("DOMContentLoaded", () => {
    carregarDados();
});

function carregarDados() {
    let receitas = 0;
    let despesas = 0;
    let vencidas = 0;

    const tbody = document.getElementById("tabela-corpo");
    tbody.innerHTML = ""; // Limpa tabela

    lancamentos.forEach(item => {
        // Cálculos
        if (item.tipo === 'R') receitas += item.valor;
        else despesas += item.valor;

        if (!item.pago && item.tipo === 'D' && new Date(item.data) < new Date()) {
            vencidas++;
        }

        // Renderiza Linha da Tabela
        const tr = document.createElement("tr");
        const badgeClass = item.pago ? 'bg-pago' : 'bg-pendente';
        const textoStatus = item.pago ? 'PAGO' : 'PENDENTE';
        
        // Ícone visual na tabela (Verde p/ Receita, Vermelho p/ Despesa)
        const corValor = item.tipo === 'R' ? '#2ecc71' : '#e74c3c';
        const sinal = item.tipo === 'R' ? '+' : '-';

        tr.innerHTML = `
            <td><span class="badge ${badgeClass}">${textoStatus}</span></td>
            <td><strong>${item.descricao}</strong></td>
            <td>${item.categoria}</td>
            <td>${item.data.split('-').reverse().join('/')}</td>
            <td style="color: ${corValor}; font-weight: bold;">${sinal} ${formatarMoeda(item.valor)}</td>
        `;
        tbody.appendChild(tr);
    });

    // Atualiza Cards
    document.getElementById("receitas-mes").innerText = formatarMoeda(receitas);
    document.getElementById("despesas-mes").innerText = formatarMoeda(despesas);
    document.getElementById("saldo-atual").innerText = formatarMoeda(receitas - despesas);
    document.getElementById("contas-vencidas").innerText = vencidas;
}