
<script>
  /** @type {number} */
  export let currentPage = 1;

  /** @type {number} */
  export let totalPages = 1;

  /** @type {(page: number) => void} */
  export let onPageChange = () => {};

  /** @type {number[]} */
  $: pages = Array.from(
    { length: Math.max(totalPages, 1) },
    (_, index) => index + 1
  );

  /** @type {number[]} */
  $: visiblePages = pages.filter((page) =>
    page === 1 ||
    page === totalPages ||
    Math.abs(page - currentPage) <= 1
  );

  /**
   * @param {number} page
   */
  function changePage(page) {
    if (
      page < 1 ||
      page > totalPages ||
      page === currentPage
    ) {
      return;
    }

    currentPage = page;
    onPageChange(page);
  }
</script>


{#if totalPages > 1}
  <nav class="pagination" aria-label="Navegação entre páginas">
    <button
      class="navigation-button"
      disabled={currentPage === 1}
      on:click={() => changePage(currentPage - 1)}
      aria-label="Página anterior"
    >
      ‹
    </button>

    {#each visiblePages as page, index}
      {#if index > 0 && page - visiblePages[index - 1] > 1}
        <span class="ellipsis">...</span>
      {/if}

      <button
        class:active={currentPage === page}
        class="page-button"
        aria-current={currentPage === page ? 'page' : undefined}
        on:click={() => changePage(page)}
      >
        {page}
      </button>
    {/each}

    <button
      class="navigation-button"
      disabled={currentPage === totalPages}
      on:click={() => changePage(currentPage + 1)}
      aria-label="Próxima página"
    >
      ›
    </button>
  </nav>
{/if}

<style>
  .pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 18px 0;
  }

  .page-button,
  .navigation-button {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 34px;
    height: 34px;
    padding: 0 9px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-surface);
    color: var(--color-text-secondary);
    font-family: inherit;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .page-button:hover:not(.active),
  .navigation-button:hover:not(:disabled) {
    background: var(--color-background);
    color: var(--color-primary);
    border-color: var(--color-secondary);
  }

  .page-button.active {
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
    font-weight: 600;
  }

  .navigation-button {
    font-size: 20px;
  }

  button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .ellipsis {
    padding: 0 4px;
    color: var(--color-text-light);
  }
</style>
