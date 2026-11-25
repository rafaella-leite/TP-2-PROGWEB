<script>
  import Dashboard from './pages/Dashboard.svelte';
  import TCCs from './pages/TCCs.svelte';
  import Alunos from './pages/Alunos.svelte';


  let paginaAtual = 'Dashboard';

  const menu = [
    {
      grupo: 'GERENCIAMENTO',
      itens: [
        { nome: 'Dashboard', icone: '▦' },
        { nome: 'TCCs', icone: '▤' },
        { nome: 'Alunos', icone: '♙' },
        { nome: 'Professores', icone: '♧' }
      ]
    },
    {
      grupo: 'INSTITUCIONAL',
      itens: [
        { nome: 'Cursos', icone: '▣' },
        { nome: 'Departamentos', icone: '▥' },
        { nome: 'Unidades acadêmicas', icone: '⌂' }
      ]
    }
  ];
</script>

<svelte:head>
  <title>Gestão de TCCs</title>

  <meta
    name="description"
    content="Sistema de gerenciamento de Trabalhos de Conclusão de Curso"
  />

  <meta
    name="viewport"
    content="width=device-width, initial-scale=1"
  />
</svelte:head>

<div class="app-layout">
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="sidebar-heading">GESTÃO ACADÊMICA</div>

      <nav>
        {#each menu as grupo}
          <div class="menu-group">
            <span class="group-title">{grupo.grupo}</span>

            {#each grupo.itens as item}
              <button
                class:active={paginaAtual === item.nome}
                class="menu-item"
                onclick={() => paginaAtual = item.nome}
              >
                <span class="menu-icon">{item.icone}</span>
                <span>{item.nome}</span>
              </button>
            {/each}
          </div>
        {/each}
      </nav>
    </div>

    <div class="sidebar-bottom">
      <div class="sidebar-footer">
        <span class="footer-dot"></span>
        Sistema acadêmico
      </div>
    </div>
  </aside>

  <main class="main-area">
    <header class="header">
      <div class="breadcrumb">
        <span>Início</span>
        <span class="breadcrumb-separator">/</span>
        <strong>{paginaAtual}</strong>
      </div>

      <div class="header-actions">
        <span class="header-date">
          Painel de gerenciamento
        </span>

        <div class="profile">
          <div class="profile-avatar">A</div>
          <div class="profile-info">
            <strong>Administrador</strong>
            <span>Gestão acadêmica</span>
          </div>
        </div>
      </div>
    </header>

    
    <section class="page-content">
      {#if paginaAtual === 'Dashboard'}
        <Dashboard />

      {:else if paginaAtual === 'TCCs'}
        <TCCs />

      {:else}
        <div class="page-heading">
          <div>
            <span class="eyebrow">GERENCIAMENTO</span>
            <h1>{paginaAtual}</h1>
            <p>Área reservada para o módulo {paginaAtual}.</p>
          </div>
        </div>
      {/if}
    </section>

    <section class="page-content">
      {#if paginaAtual === 'Dashboard'}
        <Dashboard />

      {:else if paginaAtual === 'TCCs'}
        <TCCs />

      {:else if paginaAtual === 'Alunos'}
        <Alunos />

      {:else}
        <div class="page-heading">
          <div>
            <span class="eyebrow">GERENCIAMENTO</span>
            <h1>{paginaAtual}</h1>
            <p>Área reservada para o módulo {paginaAtual}.</p>
          </div>
        </div>
      {/if}
    </section>

  </main>
</div>

<style>
  .app-layout {
    display: flex;
    min-height: 100vh;
  }

  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;

    width: 250px;
    min-width: 250px;
    height: 100vh;

    background: var(--color-primary);
    color: white;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    padding: 30px 18px 20px;
    box-sizing: border-box;

    overflow-y: auto;
    z-index: 100;
  }

  .sidebar-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.2px;
    padding: 0 12px;
    margin-bottom: 42px;
    color: #D2E8DF;
  }

  .menu-group {
    margin-bottom: 30px;
  }

  .group-title {
    display: block;
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 600;
    color: #A9C5BA;
    padding: 0 12px;
    margin-bottom: 12px;
  }

  .menu-item {
    display: flex;
    align-items: center;
    gap: 13px;
    width: 100%;
    padding: 12px;
    border: 0;
    border-radius: 9px;
    color: #D5E4DD;
    background: transparent;
    text-align: left;
    font-size: 13px;
    margin-bottom: 5px;
    transition: background 0.2s;
  }

  .menu-item:hover,
  .menu-item.active {
    background: #397568;
    color: white;
  }

  .menu-icon {
    width: 20px;
    font-size: 18px;
    text-align: center;
  }

  .sidebar-footer {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 12px;
    color: #D2E8DF;
    font-size: 11px;
    border-top: 1px solid #397568;
  }

  .footer-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #75A99A;
  }

  .main-area {
      flex: 1;
      min-width: 0;
      width: calc(100% - 250px);
      margin-left: 250px;
      box-sizing: border-box;
  }

  .header {
    height: 76px;
    background: white;
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 38px;
  }

  .breadcrumb {
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 12px;
    color: var(--color-text-secondary);
  }

  .breadcrumb strong {
    color: var(--color-text);
  }

  .breadcrumb-separator {
    color: #C4CEC8;
  }

  .header-actions,
  .profile {
    display: flex;
    align-items: center;
  }

  .header-actions {
    gap: 25px;
  }

  .header-date {
    font-size: 12px;
    color: var(--color-text-secondary);
  }

  .profile {
    gap: 10px;
  }

  .profile-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--color-mint);
    color: var(--color-primary);
    display: grid;
    place-items: center;
    font-weight: 700;
  }

  .profile-info {
    display: flex;
    flex-direction: column;
    font-size: 11px;
    gap: 2px;
  }

  .profile-info span {
    color: var(--color-text-secondary);
  }

  .page-content {
    width: 100%;
    min-width: 0;
    padding: 38px;
    box-sizing: border-box;
  }

  .page-heading {
    margin-bottom: 30px;
  }

  .eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: var(--color-secondary);
  }

  .page-heading h1 {
    font-size: 28px;
    margin: 7px 0;
  }

  .page-heading p {
    color: var(--color-text-secondary);
    font-size: 13px;
  }

  @media (max-width: 760px) {
    .main-area {
        width: calc(100% - 65px);
        margin-left: 65px;
    }

    .sidebar-heading,
    .group-title,
    .menu-item span:not(.menu-icon),
    .sidebar-footer {
      display: none;
    }

    .menu-item {
      justify-content: center;
      padding: 12px 5px;
    }

    .header {
      padding: 0 16px;
    }

    .header-date,
    .profile-info {
      display: none;
    }

    .page-content {
        width: 100%;
        padding: 20px 12px;
    }
  }

  @media (max-width: 760px) {
    .app-layout .sidebar {
      width: 65px !important;
      min-width: 65px !important;
      max-width: 65px !important;
      flex: 0 0 65px;
      box-sizing: border-box;
      padding: 20px 7px;
    }

    .app-layout .main-area {
      margin-left: 65px;
      width: calc(100% - 65px);
    }

    .app-layout .sidebar-heading,
    .app-layout .group-title,
    .app-layout .menu-item span:not(.menu-icon),
    .app-layout .sidebar-footer {
      display: none;
    }

    .app-layout .menu-item {
      justify-content: center;
      padding: 12px 5px;
    }
  }
</style>
