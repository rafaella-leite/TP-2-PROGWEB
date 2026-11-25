
<script>
  import { onMount } from 'svelte';

  const API = 'http://127.0.0.1:8000/api';

  /**
   * @typedef {{id: number, nome: string, sigla: string, codigo: string}} Curso
   */

  /**
   * @typedef {{
   *   id: number,
   *   nome: string,
   *   matricula: string,
   *   curso: number | Curso | null
   * }} Aluno
   */

  /** @type {Aluno[]} */
  let alunos = [];

  /** @type {Curso[]} */
  let cursos = [];

  let loading = true;
  let errorMessage = '';

  let search = '';
  let filtroCurso = '';

  let currentPage = 1;
  const pageSize = 10;
    
  /** @param {string} endpoint */
  async function getData(endpoint) {
    const response = await fetch(`${API}/${endpoint}/`);

    if (!response.ok) {
      throw new Error(`Erro ao carregar ${endpoint}.`);
    }

    const data = await response.json();

    return Array.isArray(data) ? data : data.results || [];
  }

  async function loadData() {
    loading = true;
    errorMessage = '';

    try {
      const [alunosData, cursosData] = await Promise.all([
        getData('alunos'),
        getData('cursos')
      ]);

      alunos = alunosData;
      cursos = cursosData;
    } catch (error) {
      errorMessage = error instanceof Error
        ? error.message
        : 'Não foi possível carregar os alunos.';
    } finally {
      loading = false;
    }
  }

  /** @param {Aluno} aluno
    * @returns {Curso | null}
    */
  function getCurso(aluno) {
    if (!aluno.curso) return null;

    if (typeof aluno.curso === 'object') {
      return aluno.curso;
    }

    return cursos.find(
      curso => String(curso.id) === String(aluno.curso)
    ) || null;
  }

  /** @param {Aluno} aluno */
  function getCursoNome(aluno) {
    return getCurso(aluno)?.nome || 'Curso não informado';
  }

  $: filteredAlunos = alunos.filter(aluno => {
    const term = search.trim().toLowerCase();

    const curso = getCursoNome(aluno).toLowerCase();

    const matchesSearch =
      !term ||
      String(aluno.nome || '').toLowerCase().includes(term) ||
      String(aluno.matricula || '').toLowerCase().includes(term) ||
      curso.includes(term);

    const matchesCurso =
      !filtroCurso ||
      String(
        typeof aluno.curso === 'object'
          ? aluno.curso?.id
          : aluno.curso
      ) === filtroCurso;

    return matchesSearch && matchesCurso;
  });

  $: totalPages = Math.max(
    1,
    Math.ceil(filteredAlunos.length / pageSize)
  );

  $: paginatedAlunos = filteredAlunos.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  $: totalAlunos = alunos.length;

  $: totalCursos = new Set(
    alunos
      .map(aluno => getCurso(aluno)?.id)
      .filter(id => id !== undefined && id !== null)
  ).size;

  $: if (currentPage > totalPages) {
    currentPage = totalPages;
  }

  function resetPage() {
    currentPage = 1;
  }

  function clearFilters() {
    search = '';
    filtroCurso = '';
    currentPage = 1;
  }

  function previousPage() {
    if (currentPage > 1) currentPage--;
  }

  function nextPage() {
    if (currentPage < totalPages) currentPage++;
  }

  onMount(loadData);
</script>

<svelte:head>
  <title>Alunos | Gestão de TCCs</title>
</svelte:head>

<div class="alunos-page">

  <!-- CABEÇALHO -->
  <header class="page-header">
    <div>
      <span class="eyebrow">GERENCIAMENTO</span>
      <h1>Alunos</h1>
      <p>Consulte os alunos cadastrados e seus respectivos cursos.</p>
    </div>

    <button
      class="refresh-button"
      onclick={loadData}
      disabled={loading}
    >
      ↻ Atualizar dados
    </button>
  </header>

  <!-- MENSAGEM DE ERRO -->
  {#if errorMessage}
    <div class="feedback error">
      <span>{errorMessage}</span>
      <button onclick={loadData}>Tentar novamente</button>
    </div>
  {/if}

  <!-- INDICADORES -->
  <section class="summary-grid">
    <article class="summary-card">
      <div>
        <span>Total de alunos</span>
        <strong>{totalAlunos}</strong>
        <small>Alunos cadastrados no sistema</small>
      </div>
      <div class="summary-icon">♙</div>
    </article>

    <article class="summary-card">
      <div>
        <span>Cursos com alunos</span>
        <strong>{totalCursos}</strong>
        <small>Cursos representados na listagem</small>
      </div>
      <div class="summary-icon">▣</div>
    </article>
  </section>

  <!-- LISTAGEM -->
  <section class="list-section">

    <div class="section-heading">
      <div>
        <h2>Alunos cadastrados</h2>
        <p>{filteredAlunos.length} registro(s) encontrado(s)</p>
      </div>
    </div>

    <!-- FILTROS -->
    <div class="filters">
      <input
        type="search"
        class="search-input"
        placeholder="Buscar por nome ou matrícula..."
        bind:value={search}
        oninput={resetPage}
      />

      <select bind:value={filtroCurso} onchange={resetPage}>
        <option value="">Todos os cursos</option>

        {#each cursos as curso (curso.id)}
          <option value={String(curso.id)}>
            {curso.nome}
          </option>
        {/each}
      </select>

      <button class="clear-button" onclick={clearFilters}>
        Limpar filtros
      </button>
    </div>

    <!-- TABELA -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Aluno</th>
            <th>Matrícula</th>
            <th>Curso</th>
            <th>Código do curso</th>
          </tr>
        </thead>

        <tbody>
          {#if loading}
            <tr>
              <td colspan="4" class="table-message">
                Carregando alunos...
              </td>
            </tr>

          {:else if paginatedAlunos.length === 0}
            <tr>
              <td colspan="4" class="table-message">
                Nenhum aluno encontrado.
              </td>
            </tr>

          {:else}
            {#each paginatedAlunos as aluno (aluno.id)}
              <tr>
                <td class="student-name">
                  <div class="student-avatar">
                    {aluno.nome?.charAt(0)?.toUpperCase() || '?'}
                  </div>
                  <strong>{aluno.nome}</strong>
                </td>

                <td>
                  <span class="registration">
                    {aluno.matricula}
                  </span>
                </td>

                <td>{getCursoNome(aluno)}</td>

                <td>
                  {getCurso(aluno)?.codigo || 'Não informado'}
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>

    <!-- PAGINAÇÃO -->
    <footer class="table-footer">
      <span>
        Página {currentPage} de {totalPages}
      </span>

      <div class="pagination">
        <button
          onclick={previousPage}
          disabled={currentPage <= 1}
        >
          Anterior
        </button>

        <button
          onclick={nextPage}
          disabled={currentPage >= totalPages}
        >
          Próxima
        </button>
      </div>
    </footer>

  </section>
</div>

<style>
  .alunos-page {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 100%;
    min-width: 0;
  }

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 16px;
  }

  .eyebrow {
    color: var(--color-secondary);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
  }

  .page-header h1 {
    margin: 5px 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
  }

  .page-header p {
    margin: 0;
    color: var(--color-text-secondary);
    font-size: 13px;
  }

  .refresh-button {
    min-height: 40px;
    padding: 0 15px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: white;
    color: var(--color-primary);
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
  }

  .refresh-button:hover {
    background: var(--color-mint);
  }

  .refresh-button:disabled {
    opacity: .5;
    cursor: wait;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .summary-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    padding: 22px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    min-width: 0;
  }

  .summary-card span {
    display: block;
    color: var(--color-text-secondary);
    font-size: 12px;
    font-weight: 600;
  }

  .summary-card strong {
    display: block;
    margin: 9px 0 5px;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 28px;
  }

  .summary-card small {
    color: var(--color-text-light);
    font-size: 11px;
  }

  .summary-icon {
    display: grid;
    place-items: center;
    flex-shrink: 0;
    width: 46px;
    height: 46px;
    border-radius: 13px;
    background: var(--color-mint);
    color: var(--color-primary);
    font-size: 22px;
  }

  .list-section {
    min-width: 0;
    padding: 22px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
  }

  .section-heading {
    margin-bottom: 20px;
  }

  .section-heading h2 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
  }

  .section-heading p {
    margin: 5px 0 0;
    color: var(--color-text-secondary);
    font-size: 12px;
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 22px;
  }

  .filters input,
  .filters select {
    height: 42px;
    min-width: 150px;
    padding: 0 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: white;
    color: var(--color-text);
    font-family: inherit;
    font-size: 12px;
    box-sizing: border-box;
  }

  .filters input:focus,
  .filters select:focus {
    outline: none;
    border-color: var(--color-secondary);
  }

  .search-input {
    flex: 1 1 240px;
  }

  .clear-button {
    height: 42px;
    padding: 0 12px;
    border: none;
    background: transparent;
    color: var(--color-text-secondary);
    font-family: inherit;
    font-size: 12px;
    cursor: pointer;
  }

  .table-container {
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }

  table {
    width: 100%;
    min-width: 600px;
    border-collapse: collapse;
    text-align: left;
    font-size: 12px;
  }

  thead {
    background: var(--color-background);
  }

  th {
    padding: 14px;
    color: var(--color-text-secondary);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    white-space: nowrap;
  }

  td {
    padding: 14px;
    color: var(--color-text);
    border-top: 1px solid var(--color-border);
    vertical-align: middle;
  }

  tbody tr:hover {
    background: rgba(210, 232, 223, .18);
  }

  .student-name {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 200px;
  }

  .student-name strong {
    font-weight: 600;
  }

  .student-avatar {
    display: grid;
    place-items: center;
    flex-shrink: 0;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: var(--color-mint);
    color: var(--color-primary);
    font-weight: 700;
  }

  .registration {
    color: var(--color-text-secondary);
    font-variant-numeric: tabular-nums;
  }

  .table-message {
    padding: 35px;
    text-align: center;
    color: var(--color-text-secondary);
  }

  .table-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 18px;
    color: var(--color-text-secondary);
    font-size: 12px;
  }

  .pagination {
    display: flex;
    gap: 8px;
  }

  .pagination button {
    padding: 8px 12px;
    border: 1px solid var(--color-border);
    border-radius: 7px;
    background: white;
    color: var(--color-text);
    cursor: pointer;
  }

  .pagination button:disabled {
    opacity: .45;
    cursor: not-allowed;
  }

  .feedback {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    padding: 13px 16px;
    border-radius: var(--radius-md);
    font-size: 13px;
  }

  .feedback.error {
    background: rgba(201, 107, 107, .1);
    color: var(--color-danger);
  }

  .feedback button {
    border: none;
    background: transparent;
    color: inherit;
    font-weight: 600;
    cursor: pointer;
  }

  @media (max-width: 760px) {
    .alunos-page {
      gap: 18px;
    }

    .page-header {
      align-items: stretch;
      flex-direction: column;
    }

    .refresh-button {
      width: 100%;
    }

    .summary-grid {
      grid-template-columns: 1fr;
    }

    .list-section {
      padding: 15px;
    }

    .filters {
      align-items: stretch;
    }

    .filters input,
    .filters select {
      width: 100%;
      flex: 1 1 100%;
    }

    .clear-button {
      align-self: flex-start;
    }

    .table-footer {
      align-items: flex-start;
      flex-direction: column;
    }
  }
</style>
