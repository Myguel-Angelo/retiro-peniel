
document.addEventListener('DOMContentLoaded', function () {
    const filtroGrupo = document.getElementById('filtro-grupo');
    const filtroStatus = document.getElementById('filtro-status');
    const ordenarPor = document.getElementById('ordenar-por');
    const tabela = document.getElementById('lista-inscricoes');
    const linhasOriginais = Array.from(tabela.querySelectorAll('tr'));

    function aplicarFiltrosEOrdenacao() {
        const grupoSelecionado = filtroGrupo.value;
        const statusSelecionado = filtroStatus.value;
        const criterioOrdenacao = ordenarPor.value;

        // Filtra as linhas
        let linhasFiltradas = linhasOriginais.filter(linha => {
            const grupo = linha.getAttribute('data-grupo');
            const status = linha.getAttribute('data-status');

            const grupoOk = !grupoSelecionado || grupo === grupoSelecionado;
            const statusOk = !statusSelecionado || status === statusSelecionado;

            return grupoOk && statusOk;
        });

        // Ordena
        linhasFiltradas.sort((a, b) => {
            if (criterioOrdenacao === 'nome') {
                const nomeA = a.getAttribute('data-nome');
                const nomeB = b.getAttribute('data-nome');
                return nomeA.localeCompare(nomeB);
            } else if (criterioOrdenacao === 'data_inscricao') {
                const dataA = new Date(a.getAttribute('data-data'));
                const dataB = new Date(b.getAttribute('data-data'));
                return dataB - dataA; // Mais recente primeiro
            } else if (criterioOrdenacao === 'status') {
                const statusA = a.getAttribute('data-status');
                const statusB = b.getAttribute('data-status');
                return statusA.localeCompare(statusB);
            } else if (criterioOrdenacao === 'grupo') {
                const grupoA = a.getAttribute('data-grupo');
                const grupoB = b.getAttribute('data-grupo');
                return grupoA.localeCompare(grupoB);
            }
            return 0;
        });

        // Atualiza o DOM
        tabela.innerHTML = '';
        linhasFiltradas.forEach(linha => tabela.appendChild(linha));
    }

    // Eventos de mudança
    filtroGrupo.addEventListener('change', aplicarFiltrosEOrdenacao);
    filtroStatus.addEventListener('change', aplicarFiltrosEOrdenacao);
    ordenarPor.addEventListener('change', aplicarFiltrosEOrdenacao);

    // Inicializa
    aplicarFiltrosEOrdenacao();
});
