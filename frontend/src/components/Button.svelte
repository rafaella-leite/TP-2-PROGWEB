
<script>
    export let variant = 'primary';
    export let size = 'medium';
    export let disabled = false;
    /** @type {'button' | 'submit' | 'reset'} */
    export let type = 'button';
    export let fullWidth = false;
</script>

<button
    class={`button ${variant} ${size}`}
    class:full-width={fullWidth}
    {disabled}
    {type}
    on:click
>
    <slot />
</button>

<style>
    .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        border: 1px solid transparent;
        border-radius: 9px;
        font-family: Inter, sans-serif;
        font-weight: 600;
        cursor: pointer;
        transition: background .2s ease, border-color .2s ease, transform .2s ease;
        white-space: nowrap;
    }

    .button:hover:not(:disabled) {
        transform: translateY(-1px);
    }

    .button:disabled {
        opacity: .55;
        cursor: not-allowed;
    }

    /* VARIAÇÕES */

    .primary {
        background: var(--color-primary);
        color: white;
    }

    .primary:hover:not(:disabled) {
        background: var(--color-primary-hover);
    }

    .secondary {
        background: white;
        color: var(--color-primary);
        border-color: var(--color-border);
    }

    .secondary:hover:not(:disabled) {
        background: var(--color-mint);
        border-color: var(--color-secondary);
    }

    .danger {
        background: #C96B6B;
        color: white;
    }

    .danger:hover:not(:disabled) {
        background: #B85C5C;
    }

    .ghost {
        background: transparent;
        color: var(--color-primary);
    }

    .ghost:hover:not(:disabled) {
        background: var(--color-mint);
    }

    /* TAMANHOS */

    .small {
        padding: 7px 11px;
        font-size: 12px;
    }

    .medium {
        padding: 10px 16px;
        font-size: 13px;
    }

    .large {
        padding: 13px 20px;
        font-size: 14px;
    }

    .full-width {
        width: 100%;
    }
</style>
