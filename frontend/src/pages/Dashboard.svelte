
<script>
    import { onMount } from 'svelte';
    import StatCard from '../components/StatCard.svelte';

    /**
     * Estrutura retornada pela API de estatísticas do Django.
     * @typedef {Object} Estatisticas
     * @property {number} total_geral
     * @property {Record<string, number>} por_status
     * @property {Record<string, number>} por_tipo
     * @property {Record<string, number>} por_idioma
     * @property {Record<string, number>} por_semestre
     * @property {Record<string, number>} por_orientador
     * @property {Record<string, number>} por_coorientador
     * @property {Record<string, number>} por_curso
     * @property {Record<string, number>} por_departamento
     * @property {Record<string, number>} por_unidade_academica
     */

    const API_URL = 'http://127.0.0.1:8000/api/tccs/estatisticas/';

    /** @type {Estatisticas | null} */
    let estatisticas = null;

    let carregando = true;
    let erro = '';

    // Normaliza textos para facilitar a comparação dos status.
    // Exemplo: "Em Elaboração" e "em elaboracao" serão equivalentes.

    /**
     * @param {unknown} texto
     * @returns {string}
     */
    function normalizar(texto) {
        return String(texto ?? '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .trim();
    }

    // Busca a quantidade de TCCs de determinado status.

    /**
     * @param {Record<string, number> | undefined} porStatus
     * @param {string} nome
     * @returns {number}
     */
    function buscarStatus(porStatus, nome) {
        if (!porStatus) return 0;

        const entrada = Object.entries(porStatus)
            .find(([chave]) => normalizar(chave) === normalizar(nome));

        return entrada ? entrada[1] : 0;
    }

    // Indicadores do dashboard.

    $: total = estatisticas?.total_geral ?? 0;

    $: aprovados = buscarStatus(estatisticas?.por_status, 'Aprovado');

    $: enviados = buscarStatus(estatisticas?.por_status, 'Enviado');

    $: elaboracao = buscarStatus(estatisticas?.por_status, 'Em Elaboração');

    $: reprovados = buscarStatus(estatisticas?.por_status, 'Reprovado');

    $: taxaAprovacao = total > 0
        ? ((aprovados / total) * 100).toFixed(1)
        : '0.0';

    // Dados dos gráficos.

    $: status = Object.entries(estatisticas?.por_status ?? {});

    $: orientadores = Object.entries(
        estatisticas?.por_orientador ?? {}
    )
        .filter(([nome]) => nome && nome !== 'None')
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

    $: maiorTotalOrientador = Math.max(
        1,
        ...orientadores.map(([, quantidade]) => quantidade)
    );


    // Dados para as novas visualizações.

    $: tipos = Object.entries(estatisticas?.por_tipo ?? {})
        .filter(([, quantidade]) => quantidade > 0)
        .sort((a, b) => b[1] - a[1]);

    $: totalTipos = tipos.reduce(
        (soma, [, quantidade]) => soma + quantidade,
        0
    );

    $: cursos = Object.entries(estatisticas?.por_curso ?? {})
        .filter(([nome, quantidade]) => nome && nome !== 'None' && quantidade > 0)
        .sort((a, b) => b[1] - a[1]);

    $: maiorTotalCurso = Math.max(
        1,
        ...cursos.map(([, quantidade]) => quantidade)
    );

    $: semestres = Object.entries(estatisticas?.por_semestre ?? {})
        .filter(([nome, quantidade]) => nome && quantidade > 0)
        .sort(([a], [b]) => a.localeCompare(b));

    $: maiorTotalSemestre = Math.max(
        1,
        ...semestres.map(([, quantidade]) => quantidade)
    );

    // Cores do gráfico de rosca.

    const coresTipos = [
        '#204C43',
        '#397568',
        '#75A99A',
        '#D6A65D',
        '#6B91A1'
    ];

    $: donutStyle = (() => {
        if (totalTipos === 0) {
            return 'conic-gradient(#E8EEEA 0% 100%)';
        }

        let acumulado = 0;

        const fatias = tipos.map(([, quantidade], indice) => {
            const inicio = acumulado;
            acumulado += (quantidade / totalTipos) * 100;

            const cor = coresTipos[indice % coresTipos.length];

            return `${cor} ${inicio}% ${acumulado}%`;
        });

        return `conic-gradient(${fatias.join(', ')})`;
    })();

    // Consulta a API do Django.

    async function carregarEstatisticas() {
        carregando = true;
        erro = '';

        try {
            const resposta = await fetch(API_URL);

            if (!resposta.ok) {
                throw new Error(
                    `Erro ao consultar a API: ${resposta.status}`
                );
            }

            const dados = await resposta.json();

            estatisticas = /** @type {Estatisticas} */ (dados);

        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);

            erro = 'Não foi possível carregar os dados. Verifique se o servidor Django está funcionando.';

        } finally {
            carregando = false;
        }
    }

    // Carrega os dados automaticamente ao abrir o dashboard.

    onMount(() => {
        carregarEstatisticas();
    });
</script>

<svelte:head>
    <title>Dashboard | Gestão de TCCs</title>
</svelte:head>

<div class="dashboard">

    <!-- CABEÇALHO DA PÁGINA -->

    <div class="page-heading">
        <div>
            <span class="eyebrow">VISÃO GERAL</span>

            <h1>Dashboard</h1>

            <p>
                Acompanhe os indicadores e a situação dos trabalhos de conclusão.
            </p>
        </div>

        <button
            class="refresh-button"
            on:click={carregarEstatisticas}
            disabled={carregando}
        >
            ↻ Atualizar dados
        </button>
    </div>

    <!-- CARREGAMENTO -->

    {#if carregando}

        <div class="feedback">
            <div class="loader"></div>
            <p>Carregando indicadores...</p>
        </div>

    <!-- ERRO DE CONEXÃO -->

    {:else if erro}

        <div class="error-message">
            <p>{erro}</p>

            <button on:click={carregarEstatisticas}>
                Tentar novamente
            </button>
        </div>

    <!-- CONTEÚDO DO DASHBOARD -->

    {:else}

        <!-- CARDS DE INDICADORES -->

        
        <section class="stats-grid">

            <StatCard
                title="Total de TCCs"
                value={String(total)}
                description="Trabalhos cadastrados"
                icon="▤"
            />

            <StatCard
                title="Aprovados"
                value={String(aprovados)}
                description="Trabalhos aprovados"
                icon="✓"
            />

            <StatCard
                title="Em elaboração"
                value={String(elaboracao)}
                description="Em desenvolvimento"
                icon="◷"
                color="gold"
            />

            <StatCard
                title="Enviados"
                value={String(enviados)}
                description="Aguardando avaliação"
                icon="↗"
                color="blue"
            />

            <StatCard
                title="Reprovados"
                value={String(reprovados)}
                description="Trabalhos reprovados"
                icon="×"
                color="red"
            />

            <StatCard
                title="Taxa de aprovação"
                value={`${taxaAprovacao}%`}
                description="Aprovados sobre o total"
                icon="%"
            />

        </section>


        <!-- GRÁFICOS -->

        <section class="charts-grid">

            <!-- TCCs POR STATUS -->

            <div class="chart-card">

                <div class="chart-heading">
                    <div>
                        <h2>TCCs por status</h2>

                        <p>
                            Distribuição dos trabalhos cadastrados
                        </p>
                    </div>
                </div>

                {#if status.length > 0}

                    <div class="status-list">

                        {#each status as item}
                            <div class="status-item">

                                <div class="status-info">
                                    <span>
                                        {item[0] || 'Não informado'}
                                    </span>

                                    <strong>{item[1]}</strong>
                                </div>

                                <div class="progress-track">

                                    <div
                                        class="progress-fill"
                                        style={`width: ${total > 0 ? (item[1] / total) * 100 : 0}%`}
                                    ></div>

                                </div>

                            </div>
                        {/each}

                    </div>

                {:else}

                    <p class="empty-state">
                        Nenhum dado de status disponível.
                    </p>

                {/if}

            </div>

            <!-- TCCs POR ORIENTADOR -->

            <div class="chart-card">

                <div class="chart-heading">
                    <div>
                        <h2>TCCs por orientador</h2>

                        <p>
                            Orientadores com mais trabalhos cadastrados
                        </p>
                    </div>
                </div>

                {#if orientadores.length > 0}

                    <div class="orientador-list">

                        {#each orientadores as orientador}

                            <div class="orientador-item">

                                <div class="orientador-info">
                                    <span>{orientador[0]}</span>

                                    <strong>{orientador[1]}</strong>
                                </div>

                                <div class="progress-track">

                                    <div
                                        class="progress-fill orientador-fill"
                                        style={`width: ${(orientador[1] / maiorTotalOrientador) * 100}%`}
                                    ></div>

                                </div>

                            </div>

                        {/each}

                    </div>

                {:else}

                    <p class="empty-state">
                        Nenhum orientador com TCC cadastrado.
                    </p>

                {/if}

            </div>

        </section>


        <section class="extra-charts-grid">

            <!-- TCCs POR TIPO -->

            <div class="chart-card">
                <div class="chart-heading">
                    <div>
                        <h2>TCCs por tipo</h2>
                        <p>Distribuição por modalidade de trabalho</p>
                    </div>
                </div>

                {#if totalTipos > 0}
                    <div class="donut-content">
                        <div
                            class="donut-chart"
                            style={`background: ${donutStyle}`}
                        >
                            <div class="donut-center">
                                <strong>{totalTipos}</strong>
                                <span>Trabalhos</span>
                            </div>
                        </div>

                        <div class="donut-legend">
                            {#each tipos as tipo, i}
                                <div class="legend-item">
                                    <div class="legend-name">
                                        <span
                                            class="legend-dot"
                                            style={`background: ${coresTipos[i % coresTipos.length]}`}
                                        ></span>
                                        <span>{tipo[0]}</span>
                                    </div>
                                    <strong>{tipo[1]}</strong>
                                </div>
                            {/each}
                        </div>
                    </div>

                {:else}
                    <p class="empty-state">
                        Nenhum dado de tipo disponível.
                    </p>
                {/if}
            </div>

            <!-- TCCs POR CURSO -->

            <div class="chart-card">
                <div class="chart-heading">
                    <div>
                        <h2>TCCs por curso</h2>
                        <p>Quantidade de trabalhos por curso</p>
                    </div>
                </div>

                {#if cursos.length > 0}
                    <div class="bar-list">
                        {#each cursos as curso}
                            <div class="bar-item">
                                <div class="bar-info">
                                    <span>{curso[0]}</span>
                                    <strong>{curso[1]}</strong>
                                </div>

                                <div class="progress-track">
                                    <div
                                        class="progress-fill course-fill"
                                        style={`width: ${(curso[1] / maiorTotalCurso) * 100}%`}
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>

                {:else}
                    <p class="empty-state">
                        Nenhum dado de curso disponível.
                    </p>
                {/if}
            </div>

            <!-- TCCs POR SEMESTRE -->

            <div class="chart-card semester-card">
                <div class="chart-heading">
                    <div>
                        <h2>TCCs por semestre</h2>
                        <p>Distribuição dos trabalhos por período letivo</p>
                    </div>
                </div>

                {#if semestres.length > 0}
                    <div class="bar-list semester-list">
                        {#each semestres as semestre}
                            <div class="bar-item">
                                <div class="bar-info">
                                    <span>{semestre[0]}</span>
                                    <strong>{semestre[1]}</strong>
                                </div>

                                <div class="progress-track">
                                    <div
                                        class="progress-fill semester-fill"
                                        style={`width: ${(semestre[1] / maiorTotalSemestre) * 100}%`}
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>

                {:else}
                    <p class="empty-state">
                        Nenhum dado de semestre disponível.
                    </p>
                {/if}
            </div>
        </section>

        <!-- RESUMO GERAL -->

        <section class="summary-card">

            <div>
                <span class="summary-label">
                    RESUMO GERAL
                </span>

                <h2>Panorama dos trabalhos</h2>

                <p>
                    Atualmente existem
                    <strong>{total} TCC(s)</strong> cadastrados,
                    sendo
                    <strong>{aprovados} aprovado(s)</strong> e
                    <strong>{reprovados} reprovado(s)</strong>.
                </p>
            </div>

            <div class="summary-icon">
                ▦
            </div>

        </section>

    {/if}

</div>

<style>
    /* ESTRUTURA GERAL */

    .dashboard {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    /* CABEÇALHO */

    .page-heading {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 16px;
    }

    .eyebrow,
    .summary-label {
        color: var(--color-secondary);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
    }

    .page-heading h1 {
        font-size: 27px;
        margin: 4px 0;
    }

    .page-heading p,
    .chart-heading p {
        color: var(--color-text-secondary);
        font-size: 13px;
    }

    /* BOTÃO ATUALIZAR */

    .refresh-button {
        border: 1px solid var(--color-border);
        background: white;
        color: var(--color-primary);
        padding: 10px 14px;
        border-radius: var(--radius-sm);
        font-weight: 600;
        transition: background .2s ease;
    }

    .refresh-button:hover {
        background: var(--color-mint);
    }

    .refresh-button:disabled {
        opacity: .6;
        cursor: wait;
    }

    /* CARDS */

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
    }

    /* GRÁFICOS */

    .charts-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
    }

    .chart-card,
    .summary-card {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: 22px;
        box-shadow: var(--shadow-card);
    }

    .chart-heading {
        margin-bottom: 24px;
    }

    .chart-heading h2,
    .summary-card h2 {
        font-size: 16px;
        margin-bottom: 4px;
    }

    /* LISTAS DOS GRÁFICOS */

    .status-list,
    .orientador-list {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .status-info,
    .orientador-info {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 8px;
        font-size: 13px;
    }

    .status-info span,
    .orientador-info span {
        color: var(--color-text-secondary);
    }

    .status-info strong,
    .orientador-info strong {
        color: var(--color-text);
    }

    /* BARRAS DE PROGRESSO */

    .progress-track {
        height: 8px;
        background: var(--color-background);
        border-radius: 20px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: var(--color-primary);
        border-radius: 20px;
        transition: width .4s ease;
    }

    .orientador-fill {
        background: var(--color-secondary);
    }

    /* RESUMO */

    .summary-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }

    .summary-card h2 {
        margin-top: 5px;
    }

    .summary-card p {
        color: var(--color-text-secondary);
        font-size: 13px;
        margin-top: 8px;
    }

    .summary-card p strong {
        color: var(--color-primary);
    }

    .summary-icon {
        display: grid;
        place-items: center;
        width: 48px;
        height: 48px;
        flex-shrink: 0;
        background: var(--color-mint);
        color: var(--color-primary);
        border-radius: 14px;
        font-size: 22px;
    }

    /* ESTADO VAZIO */

    .empty-state {
        color: var(--color-text-secondary);
        font-size: 13px;
        padding: 20px 0;
    }

    /* CARREGAMENTO */

    .feedback {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 240px;
        gap: 12px;
        color: var(--color-text-secondary);
    }

    .loader {
        width: 28px;
        height: 28px;
        border: 3px solid var(--color-mint);
        border-top-color: var(--color-primary);
        border-radius: 50%;
        animation: spin .8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    /* ERRO */

    .error-message {
        padding: 22px;
        background: #fff4f2;
        border: 1px solid #f0d4ce;
        border-radius: var(--radius-md);
        color: #9e5148;
    }

    .error-message button {
        margin-top: 12px;
        border: none;
        border-radius: 8px;
        padding: 9px 13px;
        background: var(--color-primary);
        color: white;
        cursor: pointer;
    }

    /* RESPONSIVIDADE */

    @media (max-width: 1100px) {
        .stats-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 760px) {
        .charts-grid {
            grid-template-columns: 1fr;
        }

        .page-heading {
            align-items: flex-start;
            flex-direction: column;
        }
    }

    @media (max-width: 480px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }

    .extra-charts-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
    }

    /* GRÁFICO DE ROSCA */

    .donut-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 32px;
        min-height: 190px;
        flex-wrap: wrap;
    }

    .donut-chart {
        width: 164px;
        height: 164px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        flex-shrink: 0;
        position: relative;
    }

    .donut-center {
        width: 108px;
        height: 108px;
        background: white;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .donut-center strong {
        font-family: Manrope, sans-serif;
        font-size: 27px;
        color: var(--color-primary);
    }

    .donut-center span {
        font-size: 11px;
        color: var(--color-text-secondary);
    }

    .donut-legend {
        display: flex;
        flex-direction: column;
        gap: 13px;
        flex: 1;
        min-width: 130px;
    }

    .legend-item,
    .legend-name {
        display: flex;
        align-items: center;
        gap: 9px;
    }

    .legend-item {
        justify-content: space-between;
        font-size: 12px;
    }

    .legend-name {
        color: var(--color-text-secondary);
    }

    .legend-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    /* GRÁFICOS DE BARRAS */

    .bar-list {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .bar-info {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        font-size: 13px;
    }

    .bar-info span {
        color: var(--color-text-secondary);
    }

    .bar-info strong {
        color: var(--color-text);
    }

    .course-fill {
        background: var(--color-secondary);
    }

    .semester-fill {
        background: var(--color-primary-hover);
    }

    .semester-card {
        grid-column: 1 / -1;
    }

    .semester-list {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 22px 32px;
    }

    /* RESPONSIVIDADE */

    @media (max-width: 1100px) {
        .stats-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 760px) {
        .charts-grid,
        .extra-charts-grid {
            grid-template-columns: 1fr;
        }

        .page-heading {
            align-items: flex-start;
            flex-direction: column;
        }
    }

    @media (max-width: 480px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }

</style>
