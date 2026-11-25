
<script>
  import { onMount } from 'svelte';

  /** @typedef {{ id: number; nome: string }} Registro */
  /** @typedef {{
   * id: number;
   * titulo: string;
   * resumo: string;
   * palavras_chave: string;
   * tipo: string;
   * idioma: string;
   * aluno: number | string;
   * orientador: number | string;
   * coorientador: number | string | null;
   * presidente: number | string;
   * primeiro_membro: number | string;
   * segundo_membro: number | string;
   * semestre_letivo_defesa: string | null;
   * status: string;
   * status_display?: string;
   * tipo_display?: string;
   * idioma_display?: string;
   * arquivo?: string | null;
   * }} TCC */
  /** @typedef {{
   * titulo: string; resumo: string; palavras_chave: string; tipo: string;
   * idioma: string; aluno: string | number; orientador: string | number;
   * coorientador: string | number; presidente: string | number;
   * primeiro_membro: string | number; segundo_membro: string | number;
   * semestre_letivo_defesa: string; status: string;
   * }} FormularioTCC */
  /** @typedef {{ nome?: string }} RegistroRelacionado */

  const API = 'http://127.0.0.1:8000/api';
  const MEDIA = 'http://127.0.0.1:8000';

  const STATUS_OPTIONS = [
    { value: '0', label: 'Em Elaboração' },
    { value: '1', label: 'Enviado' },
    { value: '2', label: 'Aprovado' },
    { value: '3', label: 'Reprovado' }
  ];

  const TIPO_OPTIONS = [
    { value: 'MONOGRAFIA', label: 'Monografia' },
    { value: 'RELATORIO_ESTAGIO', label: 'Relatório de Estágio' },
    { value: 'RELATORIO_TECNICO', label: 'Relatório Técnico' },
    { value: 'ARTIGO', label: 'Artigo' }
  ];

  const IDIOMA_OPTIONS = [
    { value: 'PT', label: 'Português' },
    { value: 'EN', label: 'Inglês' }
  ];

  const SEMESTRES = [
    '2020/1', '2020/2', '2021/1', '2021/2', '2022/1', '2022/2',
    '2023/1', '2023/2', '2024/1', '2024/2', '2025/1', '2025/2', '2026/1'
  ];

  /** @type {TCC[]} */
  let tccs = [];
  /** @type {Registro[]} */
  let alunos = [];
  /** @type {Registro[]} */
  let professores = [];

  let loading = true;
  let saving = false;
  let errorMessage = '';
  let successMessage = '';
  let search = '';
  let filtroStatus = '';
  let filtroTipo = '';
  let filtroIdioma = '';
  let currentPage = 1;
  const pageSize = 10;
  let modalOpen = false;
  let detailsOpen = false;
  /** @type {number | null} */
  let editingId = null;
  /** @type {TCC | null} */
  let selectedTcc = null;
  /** @type {File | null} */
  let arquivo = null;

  /** @returns {FormularioTCC} */
  function createEmptyForm() {
    return {
      titulo: '', resumo: '', palavras_chave: '', tipo: 'MONOGRAFIA', idioma: 'PT',
      aluno: '', orientador: '', coorientador: '', presidente: '',
      primeiro_membro: '', segundo_membro: '', semestre_letivo_defesa: '', status: '0'
    };
  }

  /** @type {FormularioTCC} */
  let form = createEmptyForm();

  /** @param {string} endpoint @returns {Promise<any[]>} */
  async function getData(endpoint) {
    const response = await fetch(`${API}/${endpoint}/`);
    if (!response.ok) throw new Error(`Erro ao carregar ${endpoint}.`);
    const data = await response.json();
    return Array.isArray(data) ? data : (data.results || []);
  }

  async function loadData() {
    loading = true;
    errorMessage = '';
    try {
      const [tccData, alunoData, professorData] = await Promise.all([
        getData('tccs'), getData('alunos'), getData('professores')
      ]);
      tccs = /** @type {TCC[]} */ (tccData);
      alunos = /** @type {Registro[]} */ (alunoData);
      professores = /** @type {Registro[]} */ (professorData);
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Não foi possível carregar os dados.';
    } finally {
      loading = false;
    }
  }

  /** @param {Registro[]} collection @param {number | string | RegistroRelacionado | null | undefined} id */
  function getName(collection, id) {
    if (id === null || id === undefined || id === '') return 'Não informado';
    if (typeof id === 'object') return id.nome || 'Não informado';
    const item = collection.find((registro) => String(registro.id) === String(id));
    return item?.nome || 'Não informado';
  }

  /** @param {string | number} status */
  function getStatusClass(status) {
    /** @type {Record<string, string>} */
    const classes = {
      '0': 'status-draft', '1': 'status-sent',
      '2': 'status-approved', '3': 'status-rejected'
    };
    return classes[String(status)] || 'status-draft';
  }

  /** @param {TCC} tcc */
  function getStatusLabel(tcc) {
    return tcc.status_display ||
      STATUS_OPTIONS.find((option) => option.value === String(tcc.status))?.label ||
      'Não informado';
  }

  /** @param {TCC} tcc */
  function getTipoLabel(tcc) {
    return tcc.tipo_display || TIPO_OPTIONS.find((option) => option.value === tcc.tipo)?.label || tcc.tipo || 'Não informado';
  }

  /** @param {TCC} tcc */
  function getIdiomaLabel(tcc) {
    return tcc.idioma_display || IDIOMA_OPTIONS.find((option) => option.value === tcc.idioma)?.label || tcc.idioma || 'Não informado';
  }

  $: filteredTccs = tccs.filter((tcc) => {
    const term = search.trim().toLowerCase();
    const alunoNome = getName(alunos, tcc.aluno).toLowerCase();
    const orientadorNome = getName(professores, tcc.orientador).toLowerCase();
    const matchesSearch = !term || String(tcc.titulo || '').toLowerCase().includes(term) ||
      String(tcc.resumo || '').toLowerCase().includes(term) || alunoNome.includes(term) || orientadorNome.includes(term);
    const matchesStatus = !filtroStatus || String(tcc.status) === filtroStatus;
    const matchesTipo = !filtroTipo || tcc.tipo === filtroTipo;
    const matchesIdioma = !filtroIdioma || tcc.idioma === filtroIdioma;
    return matchesSearch && matchesStatus && matchesTipo && matchesIdioma;
  });

  $: totalPages = Math.max(1, Math.ceil(filteredTccs.length / pageSize));
  $: paginatedTccs = filteredTccs.slice((currentPage - 1) * pageSize, currentPage * pageSize);
  $: totalTccs = tccs.length;
  $: totalEmElaboracao = tccs.filter((tcc) => String(tcc.status) === '0').length;
  $: totalEnviados = tccs.filter((tcc) => String(tcc.status) === '1').length;
  $: totalAprovados = tccs.filter((tcc) => String(tcc.status) === '2').length;
  $: totalReprovados = tccs.filter((tcc) => String(tcc.status) === '3').length;
  $: if (currentPage > totalPages) currentPage = totalPages;

  function resetPage() { currentPage = 1; }
  function clearFilters() {
    search = ''; filtroStatus = ''; filtroTipo = ''; filtroIdioma = ''; currentPage = 1;
  }
  function openCreateModal() {
    editingId = null; selectedTcc = null; form = createEmptyForm(); arquivo = null;
    errorMessage = ''; detailsOpen = false; modalOpen = true;
  }

  /** @param {TCC} tcc */
  function openEditModal(tcc) {
    editingId = tcc.id;
    selectedTcc = null;
    form = {
      titulo: tcc.titulo || '', resumo: tcc.resumo || '', palavras_chave: tcc.palavras_chave || '',
      tipo: tcc.tipo || 'MONOGRAFIA', idioma: tcc.idioma || 'PT',
      aluno: tcc.aluno ?? '', orientador: tcc.orientador ?? '', coorientador: tcc.coorientador ?? '',
      presidente: tcc.presidente ?? '', primeiro_membro: tcc.primeiro_membro ?? '',
      segundo_membro: tcc.segundo_membro ?? '', semestre_letivo_defesa: tcc.semestre_letivo_defesa || '',
      status: String(tcc.status ?? '0')
    };
    arquivo = null; errorMessage = ''; detailsOpen = false; modalOpen = true;
  }

  /** @param {TCC} tcc */
  function openDetails(tcc) { selectedTcc = tcc; detailsOpen = true; modalOpen = true; }

  function closeModal() {
    modalOpen = false; detailsOpen = false; selectedTcc = null; editingId = null;
    arquivo = null; errorMessage = '';
  }

  /** @param {Event} event */
  function handleFileChange(event) {
    const input = /** @type {HTMLInputElement} */ (event.currentTarget);
    arquivo = input.files?.[0] || null;
  }

  function buildPayload() {
    const payload = new FormData();
    /** @type {[string, string | number][]} */
    const entries = Object.entries(form);
    entries.forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) payload.append(key, String(value));
      else if (key === 'coorientador') payload.append(key, '');
    });
    if (arquivo) payload.append('arquivo', arquivo);
    return payload;
  }

  function validateForm() {
    /** @type {[keyof FormularioTCC, string][]} */
    const requiredFields = [
      ['titulo', 'Título'], ['resumo', 'Resumo'], ['palavras_chave', 'Palavras-chave'],
      ['aluno', 'Aluno'], ['orientador', 'Orientador'], ['presidente', 'Presidente da banca'],
      ['primeiro_membro', 'Primeiro membro'], ['segundo_membro', 'Segundo membro']
    ];
    for (const [field, label] of requiredFields) {
      if (!String(form[field] ?? '').trim()) {
        errorMessage = `Preencha o campo obrigatório: ${label}.`;
        return false;
      }
    }
    return true;
  }

  async function saveTcc() {
    errorMessage = '';
    if (!validateForm()) return;
    saving = true;
    try {
      const endpoint = editingId ? `${API}/tccs/${editingId}/` : `${API}/tccs/`;
      const response = await fetch(endpoint, { method: editingId ? 'PATCH' : 'POST', body: buildPayload() });
      if (!response.ok) {
        const data = await response.json().catch(() => null);
        const details = data ? Object.entries(data)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`)
          .join(' | ') : 'Não foi possível salvar o TCC.';
        throw new Error(details);
      }
      successMessage = editingId ? 'TCC atualizado com sucesso!' : 'TCC cadastrado com sucesso!';
      closeModal();
      await loadData();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Erro ao salvar o TCC.';
    } finally {
      saving = false;
    }
  }

  /** @param {TCC} tcc */
  async function deleteTcc(tcc) {
    const confirmed = confirm(`Deseja realmente excluir o TCC "${tcc.titulo}"?`);
    if (!confirmed) return;
    errorMessage = ''; successMessage = '';
    try {
      const response = await fetch(`${API}/tccs/${tcc.id}/`, { method: 'DELETE' });
      if (!response.ok) throw new Error('Não foi possível excluir o TCC.');
      successMessage = 'TCC excluído com sucesso!';
      await loadData();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Erro ao excluir o TCC.';
    }
  }

  function previousPage() { if (currentPage > 1) currentPage--; }
  function nextPage() { if (currentPage < totalPages) currentPage++; }

  /** @param {string | null | undefined} path */
  function getFileUrl(path) {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return `${MEDIA}${path.startsWith('/') ? '' : '/'}${path}`;
  }

  onMount(() => { void loadData(); });
</script>

<svelte:head>
  <title>Gestão de TCCs</title>
</svelte:head>

<div class="tcc-page">
  <header class="page-header">
    <div>
      <h1>Gestão de TCCs</h1>
      <p>Gerencie os trabalhos de conclusão de curso cadastrados.</p>
    </div>

    <button class="primary-button" on:click={openCreateModal}>
      + Novo TCC
    </button>
  </header>

  {#if errorMessage && !modalOpen}
    <div class="feedback error">
      {errorMessage}
      <button on:click={() => errorMessage = ''}>×</button>
    </div>
  {/if}

  {#if successMessage}
    <div class="feedback success">
      {successMessage}
      <button on:click={() => successMessage = ''}>×</button>
    </div>
  {/if}

  <section class="summary-grid">
    <article class="summary-card">
      <span>Total de TCCs</span>
      <strong>{totalTccs}</strong>
      <small>Trabalhos cadastrados</small>
    </article>

    <article class="summary-card">
      <span>Em elaboração</span>
      <strong>{totalEmElaboracao}</strong>
      <small>Em desenvolvimento</small>
    </article>

    <article class="summary-card">
      <span>Enviados</span>
      <strong>{totalEnviados}</strong>
      <small>Aguardando avaliação</small>
    </article>

    <article class="summary-card">
      <span>Aprovados</span>
      <strong>{totalAprovados}</strong>
      <small>Trabalhos aprovados</small>
    </article>

    <article class="summary-card">
      <span>Reprovados</span>
      <strong>{totalReprovados}</strong>
      <small>Trabalhos reprovados</small>
    </article>
  </section>

  <section class="list-section">
    <div class="filters">
      <input
        class="search-input"
        type="search"
        bind:value={search}
        on:input={resetPage}
        placeholder="Buscar por título, aluno ou orientador..."
      />

      <select bind:value={filtroStatus} on:change={resetPage}>
        <option value="">Todos os status</option>
        {#each STATUS_OPTIONS as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>

      <select bind:value={filtroTipo} on:change={resetPage}>
        <option value="">Todos os tipos</option>
        {#each TIPO_OPTIONS as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>

      <select bind:value={filtroIdioma} on:change={resetPage}>
        <option value="">Todos os idiomas</option>
        {#each IDIOMA_OPTIONS as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>

      <button class="clear-button" on:click={clearFilters}>
        Limpar filtros
      </button>
    </div>

    <div class="table-heading">
      <div>
        <h2>Trabalhos cadastrados</h2>
        <p>{filteredTccs.length} registro(s) encontrado(s)</p>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Aluno</th>
            <th>Orientador</th>
            <th>Tipo</th>
            <th>Idioma</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>

        <tbody>
          {#if loading}
            <tr>
              <td colspan="7" class="table-message">
                Carregando registros...
              </td>
            </tr>
          {:else if paginatedTccs.length === 0}
            <tr>
              <td colspan="7" class="table-message">
                Nenhum TCC encontrado.
              </td>
            </tr>
          {:else}
            {#each paginatedTccs as tcc (tcc.id)}
              <tr>
                <td class="title-cell">{tcc.titulo}</td>
                <td>{getName(alunos, tcc.aluno)}</td>
                <td>{getName(professores, tcc.orientador)}</td>
                <td>{getTipoLabel(tcc)}</td>
                <td>{getIdiomaLabel(tcc)}</td>
                <td>
                  <span class="status-badge {getStatusClass(tcc.status)}">
                    {getStatusLabel(tcc)}
                  </span>
                </td>
                <td>
                  <div class="row-actions">
                    <button class="action-button" on:click={() => openDetails(tcc)}>
                      Ver
                    </button>
                    <button class="action-button" on:click={() => openEditModal(tcc)}>
                      Editar
                    </button>
                    <button class="action-button delete-action" on:click={() => deleteTcc(tcc)}>
                      Excluir
                    </button>
                  </div>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>

    <footer class="table-footer">
      <span>Página {currentPage} de {totalPages}</span>

      <div class="pagination">
        <button on:click={previousPage} disabled={currentPage <= 1}>
          Anterior
        </button>
        <button on:click={nextPage} disabled={currentPage >= totalPages}>
          Próxima
        </button>
      </div>
    </footer>
  </section>
</div>

{#if modalOpen}
  <div class="modal-overlay" role="presentation">
    <div
      class="modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <header class="modal-header">
        <div>
          <h2 id="modal-title">
            {#if detailsOpen}
              Detalhes do TCC
            {:else if editingId}
              Editar TCC
            {:else}
              Novo TCC
            {/if}
          </h2>
          <p>
            {detailsOpen
              ? 'Informações do trabalho cadastrado.'
              : 'Preencha os dados do trabalho.'}
          </p>
        </div>

        <button class="close-button" on:click={closeModal}>×</button>
      </header>

      {#if detailsOpen && selectedTcc}
        <div class="details-grid">
          <div class="detail-item full">
            <span>Título</span>
            <strong>{selectedTcc.titulo}</strong>
          </div>

          <div class="detail-item full">
            <span>Resumo</span>
            <p>{selectedTcc.resumo || 'Não informado'}</p>
          </div>

          <div class="detail-item full">
            <span>Palavras-chave</span>
            <strong>{selectedTcc.palavras_chave || 'Não informado'}</strong>
          </div>

          <div class="detail-item">
            <span>Aluno</span>
            <strong>{getName(alunos, selectedTcc.aluno)}</strong>
          </div>

          <div class="detail-item">
            <span>Orientador</span>
            <strong>{getName(professores, selectedTcc.orientador)}</strong>
          </div>

          <div class="detail-item">
            <span>Coorientador</span>
            <strong>{getName(professores, selectedTcc.coorientador)}</strong>
          </div>

          <div class="detail-item">
            <span>Tipo</span>
            <strong>{getTipoLabel(selectedTcc)}</strong>
          </div>

          <div class="detail-item">
            <span>Idioma</span>
            <strong>{getIdiomaLabel(selectedTcc)}</strong>
          </div>

          <div class="detail-item">
            <span>Presidente da banca</span>
            <strong>{getName(professores, selectedTcc.presidente)}</strong>
          </div>

          <div class="detail-item">
            <span>Primeiro membro</span>
            <strong>{getName(professores, selectedTcc.primeiro_membro)}</strong>
          </div>

          <div class="detail-item">
            <span>Segundo membro</span>
            <strong>{getName(professores, selectedTcc.segundo_membro)}</strong>
          </div>

          <div class="detail-item">
            <span>Semestre de defesa</span>
            <strong>{selectedTcc.semestre_letivo_defesa || 'Não informado'}</strong>
          </div>

          <div class="detail-item">
            <span>Status</span>
            <span class="status-badge {getStatusClass(selectedTcc.status)}">
              {getStatusLabel(selectedTcc)}
            </span>
          </div>

          {#if selectedTcc.arquivo}
            <div class="detail-item full">
              <span>Arquivo</span>
              <a href={getFileUrl(selectedTcc.arquivo)} target="_blank" rel="noreferrer">
                Abrir arquivo do TCC
              </a>
            </div>
          {/if}
        </div>

        <footer class="modal-footer">
          <button class="secondary-button" on:click={closeModal}>Fechar</button>
          <button class="primary-button" on:click={() => { if (selectedTcc) openEditModal(selectedTcc); }}>
            Editar TCC
          </button>
        </footer>

      {:else}
        <form class="tcc-form" on:submit|preventDefault={saveTcc}>
          <div class="form-group full">
            <label for="titulo">Título do TCC *</label>
            <input id="titulo" bind:value={form.titulo} required maxlength="255" />
          </div>

          <div class="form-group full">
            <label for="resumo">Resumo *</label>
            <textarea id="resumo" bind:value={form.resumo} required rows="4"></textarea>
          </div>

          <div class="form-group full">
            <label for="palavras_chave">Palavras-chave *</label>
            <input id="palavras_chave" bind:value={form.palavras_chave} required maxlength="255" />
          </div>

          <div class="form-group">
            <label for="aluno">Aluno *</label>
            <select id="aluno" bind:value={form.aluno} required>
              <option value="">Selecione o aluno</option>
              {#each alunos as aluno}
                <option value={aluno.id}>{aluno.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="orientador">Orientador *</label>
            <select id="orientador" bind:value={form.orientador} required>
              <option value="">Selecione o orientador</option>
              {#each professores as professor}
                <option value={professor.id}>{professor.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="coorientador">Coorientador</label>
            <select id="coorientador" bind:value={form.coorientador}>
              <option value="">Nenhum</option>
              {#each professores as professor}
                <option value={professor.id}>{professor.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="tipo">Tipo de trabalho *</label>
            <select id="tipo" bind:value={form.tipo} required>
              {#each TIPO_OPTIONS as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="idioma">Idioma *</label>
            <select id="idioma" bind:value={form.idioma} required>
              {#each IDIOMA_OPTIONS as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="semestre">Semestre de defesa</label>
            <select id="semestre" bind:value={form.semestre_letivo_defesa}>
              <option value="">Selecione</option>
              {#each SEMESTRES as semestre}
                <option value={semestre}>{semestre}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="status">Status</label>
            <select id="status" bind:value={form.status}>
              {#each STATUS_OPTIONS as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="presidente">Presidente da banca *</label>
            <select id="presidente" bind:value={form.presidente} required>
              <option value="">Selecione</option>
              {#each professores as professor}
                <option value={professor.id}>{professor.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="primeiro_membro">Primeiro membro *</label>
            <select id="primeiro_membro" bind:value={form.primeiro_membro} required>
              <option value="">Selecione</option>
              {#each professores as professor}
                <option value={professor.id}>{professor.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group">
            <label for="segundo_membro">Segundo membro *</label>
            <select id="segundo_membro" bind:value={form.segundo_membro} required>
              <option value="">Selecione</option>
              {#each professores as professor}
                <option value={professor.id}>{professor.nome}</option>
              {/each}
            </select>
          </div>

          <div class="form-group full">
            <label for="arquivo">Arquivo do TCC</label>
            <input
              id="arquivo"
              type="file"
              accept=".pdf,.doc,.docx"
              on:change={handleFileChange}
            />
            <small>
              {arquivo ? arquivo.name : 'Envio opcional. PDF, DOC ou DOCX.'}
            </small>
          </div>

          {#if errorMessage}
            <div class="form-error full">{errorMessage}</div>
          {/if}

          <footer class="modal-footer full">
            <button type="button" class="secondary-button" on:click={closeModal}>
              Cancelar
            </button>

            <button type="submit" class="primary-button" disabled={saving}>
              {saving
                ? 'Salvando...'
                : editingId
                  ? 'Salvar alterações'
                  : 'Cadastrar TCC'}
            </button>
          </footer>
        </form>
      {/if}
    </div>
  </div>
{/if}

<style>
  .tcc-page {
    width: 100%;
  }

  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 26px;
  }

  .page-header h1 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 25px;
  }

  .page-header p {
    margin: 7px 0 0;
    color: var(--color-text-secondary);
    font-size: 13px;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 24px;
  }

  .summary-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 20px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
  }

  .summary-card span {
    color: var(--color-text-secondary);
    font-size: 12px;
    font-weight: 600;
  }

  .summary-card strong {
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
  }

  .summary-card small {
    color: var(--color-text-light);
    font-size: 11px;
  }

  .list-section {
    padding: 22px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 26px;
  }

  .search-input {
    flex: 1 1 250px;
  }

  .filters input,
  .filters select {
    min-width: 140px;
    height: 42px;
    padding: 0 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-surface);
    color: var(--color-text);
    font-family: inherit;
    font-size: 12px;
  }

  .filters input:focus,
  .filters select:focus {
    outline: none;
    border-color: var(--color-secondary);
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

  .table-heading {
    margin-bottom: 16px;
  }

  .table-heading h2 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
  }

  .table-heading p {
    margin: 5px 0 0;
    color: var(--color-text-secondary);
    font-size: 12px;
  }

  .table-container {
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }

  table {
    width: 100%;
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
    background: rgba(210, 232, 223, 0.18);
  }

  .title-cell {
    min-width: 180px;
    font-weight: 600;
  }

  .table-message {
    padding: 35px;
    text-align: center;
    color: var(--color-text-secondary);
  }

  .status-badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    white-space: nowrap;
  }

  .status-draft {
    background: #f0f1f0;
    color: #65716b;
  }

  .status-sent {
    background: #e5eff6;
    color: #47738e;
  }

  .status-approved {
    background: #e2f1e9;
    color: #397568;
  }

  .status-rejected {
    background: #f8e8e8;
    color: #b85f5f;
  }

  .row-actions {
    display: flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
  }

  .action-button {
    padding: 6px;
    border: none;
    border-radius: 5px;
    background: transparent;
    color: var(--color-primary);
    font-family: inherit;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
  }

  .action-button:hover {
    background: var(--color-background);
  }

  .delete-action {
    color: var(--color-danger);
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
    background: var(--color-surface);
    color: var(--color-text);
    cursor: pointer;
  }

  .pagination button:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  .primary-button,
  .secondary-button {
    min-height: 40px;
    padding: 0 17px;
    border-radius: var(--radius-md);
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
  }

  .primary-button {
    border: 1px solid var(--color-primary);
    background: var(--color-primary);
    color: white;
  }

  .primary-button:hover:not(:disabled) {
    background: var(--color-primary-hover);
  }

  .primary-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .secondary-button {
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    color: var(--color-text-secondary);
  }

  .feedback {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 16px;
    border-radius: var(--radius-md);
    font-size: 13px;
  }

  .feedback button {
    border: none;
    background: transparent;
    font-size: 18px;
    cursor: pointer;
  }

  .feedback.error,
  .form-error {
    background: rgba(201, 107, 107, 0.1);
    color: var(--color-danger);
  }

  .feedback.success {
    background: rgba(57, 117, 104, 0.1);
    color: var(--color-success);
  }

  .modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(20, 35, 30, 0.48);
    overflow-y: auto;
  }

  .modal {
    width: 100%;
    max-width: 760px;
    max-height: 90vh;
    padding: 24px;
    overflow-y: auto;
    background: var(--color-surface);
    border-radius: var(--radius-lg);
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.18);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 24px;
  }

  .modal-header h2 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 19px;
  }

  .modal-header p {
    margin: 6px 0 0;
    color: var(--color-text-secondary);
    font-size: 12px;
  }

  .close-button {
    border: none;
    background: transparent;
    color: var(--color-text-secondary);
    font-size: 25px;
    cursor: pointer;
  }

  .tcc-form,
  .details-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 17px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 7px;
    min-width: 0;
  }

  .form-group.full,
  .detail-item.full,
  .modal-footer.full {
    grid-column: 1 / -1;
  }

  .form-group label {
    color: var(--color-text);
    font-size: 12px;
    font-weight: 600;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    width: 100%;
    box-sizing: border-box;
    min-height: 42px;
    padding: 10px 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    outline: none;
    background: var(--color-surface);
    color: var(--color-text);
    font-family: inherit;
    font-size: 13px;
  }

  .form-group textarea {
    min-height: 100px;
    resize: vertical;
  }

  .form-group input:focus,
  .form-group select:focus,
  .form-group textarea:focus {
    border-color: var(--color-secondary);
  }

  .form-group small {
    color: var(--color-text-secondary);
    font-size: 11px;
  }

  .form-error {
    padding: 11px;
    border-radius: var(--radius-sm);
    font-size: 12px;
  }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 12px;
    margin-top: 8px;
  }

  .detail-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 0;
  }

  .detail-item > span:first-child {
    color: var(--color-text-secondary);
    font-size: 11px;
  }

  .detail-item strong,
  .detail-item p {
    margin: 0;
    color: var(--color-text);
    font-size: 13px;
    line-height: 1.6;
    overflow-wrap: anywhere;
  }

  .detail-item a {
    color: var(--color-primary);
    font-size: 13px;
  }

  @media (max-width: 1100px) {
    .summary-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
  }

  @media (max-width: 700px) {
    .page-header {
      align-items: flex-start;
      flex-direction: column;
    }

    .summary-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .filters {
      align-items: stretch;
    }

    .filters input,
    .filters select {
      flex: 1 1 100%;
    }

    .tcc-form,
    .details-grid {
      grid-template-columns: 1fr;
    }

    .form-group.full,
    .detail-item.full,
    .modal-footer.full {
      grid-column: auto;
    }

    .table-footer {
      align-items: flex-start;
      flex-direction: column;
    }

    .modal {
      padding: 18px;
    }
  }
</style>
