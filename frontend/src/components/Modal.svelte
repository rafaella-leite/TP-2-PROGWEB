
<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let open = false;
  export let title = '';
  export let description = '';
  export let size = 'medium';
  export let closeOnBackdrop = true;

  function closeModal() {
    dispatch('close');
  }

  /**
   * @param {MouseEvent} event
   */
  function handleBackdropClick(event) {
    if (
      closeOnBackdrop &&
      event.target === event.currentTarget
    ) {
      closeModal();
    }
  }

  /**
   * @param {KeyboardEvent} event
   */
  function handleKeydown(event) {
    if (event.key === 'Escape' && open) {
      closeModal();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div
    class="modal-backdrop"
    on:click={handleBackdropClick}
    role="presentation"
  >
    <section
      class="modal"
      class:small={size === 'small'}
      class:large={size === 'large'}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      on:click|stopPropagation
    >
      <header class="modal-header">
        <div class="header-content">
          <h2 id="modal-title">{title}</h2>

          {#if description}
            <p>{description}</p>
          {/if}
        </div>

        <button
          type="button"
          class="close-button"
          on:click={closeModal}
          aria-label="Fechar janela"
        >
          ×
        </button>
      </header>

      <div class="modal-body">
        <slot />
      </div>

      <footer class="modal-footer">
        <slot name="footer" />
      </footer>
    </section>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background: rgba(20, 35, 30, 0.48);
    backdrop-filter: blur(3px);
    overflow-y: auto;
  }

  .modal {
    width: 100%;
    max-width: 560px;
    max-height: calc(100vh - 48px);
    display: flex;
    flex-direction: column;
    background: var(--color-surface);
    border-radius: var(--radius-lg);
    box-shadow: 0 12px 40px rgba(20, 35, 30, 0.16);
    animation: modal-enter 0.2s ease;
    overflow: hidden;
  }

  .modal.small {
    max-width: 400px;
  }

  .modal.large {
    max-width: 760px;
  }

  .modal-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    padding: 24px;
    border-bottom: 1px solid var(--color-border);
  }

  .header-content {
    min-width: 0;
  }

  h2 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 19px;
    font-weight: 700;
  }

  .header-content p {
    margin: 6px 0 0;
    color: var(--color-text-secondary);
    font-size: 13px;
    line-height: 1.5;
  }

  .close-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    border: none;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--color-text-secondary);
    font-size: 25px;
    cursor: pointer;
  }

  .close-button:hover {
    background: var(--color-background);
    color: var(--color-text);
  }

  .modal-body {
    padding: 24px;
    overflow-y: auto;
  }

  .modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    padding: 18px 24px;
    border-top: 1px solid var(--color-border);
    background: var(--color-background);
  }

  @keyframes modal-enter {
    from {
      opacity: 0;
      transform: translateY(8px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 600px) {
    .modal-backdrop {
      align-items: flex-end;
      padding: 12px;
    }

    .modal,
    .modal.small,
    .modal.large {
      max-width: 100%;
      max-height: 90vh;
    }

    .modal-header,
    .modal-body {
      padding: 20px;
    }
  }
</style>
