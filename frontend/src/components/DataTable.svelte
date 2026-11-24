
<script>
  /**
   * @typedef {{
   *   key: string,
   *   label: string,
   *   width?: string,
   *   align?: 'left' | 'center' | 'right'
   * }} Column
   */

  /** @typedef {Record<string, any>} TableItem */

  /** @type {Column[]} */
  export let columns = [];

  /** @type {TableItem[]} */
  export let items = [];

  export let loading = false;
  export let emptyMessage = 'Nenhum registro encontrado.';
  export let rowKey = 'id';
  export let showActions = false;

  /**
   * Recupera valores de propriedades simples ou aninhadas.
   * Exemplo: aluno.nome
   *
   * @param {TableItem} item
   * @param {string} key
   * @returns {any}
   */
  function getValue(item, key) {
    if (!item || !key) return null;

    return key.split('.').reduce((obj, part) => {
      return obj != null ? obj[part] : null;
    }, item);
  }

  $: columnCount = Math.max(
    columns.length + (showActions ? 1 : 0),
    1
  );
</script>

<div class="table-container">
  <table>
    <thead>
      <tr>
        {#each columns as column}
          <th
            style:width={column.width || 'auto'}
            class:align-center={column.align === 'center'}
            class:align-right={column.align === 'right'}
          >
            {column.label}
          </th>
        {/each}

        {#if showActions}
          <th class="actions-heading">
            Ações
          </th>
        {/if}
      </tr>
    </thead>

    <tbody>
      {#if loading}
        <tr>
          <td colspan={columnCount}>
            <div class="table-message">
              Carregando registros...
            </div>
          </td>
        </tr>

      {:else if !items || items.length === 0}
        <tr>
          <td colspan={columnCount}>
            <div class="table-message">
              {emptyMessage}
            </div>
          </td>
        </tr>

      {:else}
        {#each items as item, index (item?.[rowKey] ?? index)}
          <tr>
            {#each columns as column}
              <td
                class:align-center={column.align === 'center'}
                class:align-right={column.align === 'right'}
              >
                {#if column.key === 'status'}
                  <slot name="status" {item}>
                    {#if getValue(item, column.key) != null}
                      {getValue(item, column.key)}
                    {:else}
                      <span class="empty-value">Não informado</span>
                    {/if}
                  </slot>

                {:else if getValue(item, column.key) != null && getValue(item, column.key) !== ''}
                  {getValue(item, column.key)}

                {:else}
                  <span class="empty-value">
                    Não informado
                  </span>
                {/if}
              </td>
            {/each}

            {#if showActions}
              <td class="actions-cell">
                <slot name="actions" {item} />
              </td>
            {/if}
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
</div>

<style>
  .table-container {
    width: 100%;
    overflow-x: auto;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 13px;
  }

  thead {
    background: var(--color-background);
  }

  th {
    padding: 15px 18px;
    color: var(--color-text-secondary);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  td {
    padding: 16px 18px;
    color: var(--color-text);
    border-top: 1px solid var(--color-border);
    vertical-align: middle;
  }

  tbody tr {
    transition: background 0.15s ease;
  }

  tbody tr:hover {
    background: rgba(210, 232, 223, 0.18);
  }

  .align-center {
    text-align: center;
  }

  .align-right {
    text-align: right;
  }

  .actions-heading,
  .actions-cell {
    text-align: center;
    white-space: nowrap;
  }

  .table-message {
    padding: 36px 16px;
    text-align: center;
    color: var(--color-text-secondary);
  }

  .empty-value {
    color: var(--color-text-light);
  }
</style>
