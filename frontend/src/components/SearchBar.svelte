
<script>
  export let value = '';
  export let placeholder = 'Buscar...';
  export let disabled = false;
  export let width = '100%';

  function limparBusca() {
    value = '';
  }
</script>

<div class="search-container" style="width: {width}">
  <span class="search-icon">⌕</span>

  <input
    type="text"
    bind:value
    {placeholder}
    {disabled}
    aria-label={placeholder}
  />

  {#if value}
    <button
      type="button"
      class="clear-button"
      on:click={limparBusca}
      aria-label="Limpar pesquisa"
    >
      ×
    </button>
  {/if}
</div>

<style>
  .search-container {
    display: flex;
    align-items: center;
    gap: 10px;
    height: 42px;
    padding: 0 13px;
    background: var(--color-surface, #fff);
    border: 1px solid var(--color-border, #e8eeea);
    border-radius: var(--radius-md, 12px);
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .search-container:focus-within {
    border-color: var(--color-secondary, #75a99a);
    box-shadow: 0 0 0 3px rgba(117, 169, 154, 0.12);
  }

  .search-icon {
    color: var(--color-text-secondary, #77857f);
    font-size: 24px;
    line-height: 1;
    transform: rotate(-20deg);
  }

  input {
    flex: 1;
    min-width: 0;
    height: 100%;
    border: none;
    outline: none;
    background: transparent;
    color: var(--color-text, #253a34);
    font-family: inherit;
    font-size: 13px;
  }

  input::placeholder {
    color: var(--color-text-light, #a0aaa5);
  }

  .clear-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    padding: 0;
    border: none;
    border-radius: 50%;
    background: transparent;
    color: var(--color-text-secondary, #77857f);
    font-size: 20px;
    cursor: pointer;
  }

  .clear-button:hover {
    background: var(--color-background, #f5f8f5);
  }

  input:disabled {
    cursor: not-allowed;
  }
</style>
