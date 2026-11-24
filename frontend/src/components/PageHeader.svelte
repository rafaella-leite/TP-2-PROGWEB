
<script>
  import Button from './Button.svelte';

  export let title = '';
  export let description = '';
  export let actionLabel = '';
  export let actionIcon = '';
  export let onAction = () => {};
  export let showAction = true;
</script>

<header class="page-header">
  <div class="header-content">
    <h1>{title}</h1>

    {#if description}
      <p>{description}</p>
    {/if}
  </div>

  <div class="header-actions">
    <slot name="actions" />

    {#if actionLabel && showAction}
      <Button variant="primary" on:click={onAction}>
        {#if actionIcon}
          <span>{actionIcon}</span>
        {/if}
        {actionLabel}
      </Button>
    {/if}
  </div>
</header>

<style>
  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 28px;
  }

  .header-content {
    min-width: 0;
  }

  h1 {
    margin: 0;
    color: var(--color-text);
    font-family: 'Manrope', sans-serif;
    font-size: 24px;
    font-weight: 700;
  }

  p {
    margin: 6px 0 0;
    color: var(--color-text-secondary);
    font-size: 13px;
    line-height: 1.5;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }

  @media (max-width: 640px) {
    .page-header {
      align-items: flex-start;
      flex-direction: column;
      gap: 16px;
    }

    .header-actions {
      width: 100%;
      flex-wrap: wrap;
    }
  }
</style>
