
<script>
  /**
   * @typedef {'text' | 'email' | 'number' | 'date' | 'tel' | 'password' | 'select' | 'textarea'} FieldType
   */

  /**
   * @typedef {Object} FieldOption
   * @property {string | number} value
   * @property {string} label
   */

  /** @type {string} */
  export let label = '';

  /** @type {string} */
  export let name = '';

  /** @type {string | number} */
  export let value = '';

  /** @type {FieldType} */
  export let type = 'text';

  /** @type {string} */
  export let placeholder = '';

  /** @type {boolean} */
  export let required = false;

  /** @type {boolean} */
  export let disabled = false;

  /** @type {string} */
  export let error = '';

  /** @type {string} */
  export let hint = '';

  /** @type {FieldOption[]} */
  export let options = [];

  /** @type {number} */
  export let rows = 4;

  /** @type {string} */
  export let id = name || `field-${Math.random().toString(36).slice(2, 9)}`;

  $: hasError = Boolean(error);
</script>

<div class="form-field">
  {#if label}
    <label for={id}>
      {label}
      {#if required}
        <span class="required">*</span>
      {/if}
    </label>
  {/if}

  {#if type === 'select'}
    <select
      {id}
      {name}
      bind:value
      {required}
      {disabled}
      aria-invalid={hasError}
      aria-describedby={hasError ? `${id}-error` : hint ? `${id}-hint` : undefined}
    >
      <option value="" disabled>
        {placeholder || 'Selecione uma opção'}
      </option>

      {#each options as option}
        <option value={option.value}>
          {option.label}
        </option>
      {/each}
    </select>

  {:else if type === 'textarea'}
    <textarea
      {id}
      {name}
      bind:value
      {placeholder}
      {required}
      {disabled}
      {rows}
      aria-invalid={hasError}
      aria-describedby={hasError ? `${id}-error` : hint ? `${id}-hint` : undefined}
    ></textarea>

  {:else}
    <input
      {id}
      {name}
      type={type}
      bind:value
      {placeholder}
      {required}
      {disabled}
      aria-invalid={hasError}
      aria-describedby={hasError ? `${id}-error` : hint ? `${id}-hint` : undefined}
    />
  {/if}

  {#if hasError}
    <span class="field-error" id={`${id}-error`}>
      {error}
    </span>
  {:else if hint}
    <span class="field-hint" id={`${id}-hint`}>
      {hint}
    </span>
  {/if}
</div>

<style>
  .form-field {
    display: flex;
    flex-direction: column;
    gap: 7px;
    width: 100%;
  }

  label {
    color: var(--color-text);
    font-size: 13px;
    font-weight: 600;
  }

  .required {
    color: var(--color-danger);
    margin-left: 3px;
  }

  input,
  select,
  textarea {
    width: 100%;
    box-sizing: border-box;
    padding: 11px 13px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    outline: none;
    background: var(--color-surface);
    color: var(--color-text);
    font-family: inherit;
    font-size: 13px;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  input,
  select {
    min-height: 42px;
  }

  textarea {
    min-height: 100px;
    resize: vertical;
    line-height: 1.5;
  }

  input:focus,
  select:focus,
  textarea:focus {
    border-color: var(--color-secondary);
    box-shadow: 0 0 0 3px rgba(117, 169, 154, 0.12);
  }

  input::placeholder,
  textarea::placeholder {
    color: var(--color-text-light);
  }

  input:disabled,
  select:disabled,
  textarea:disabled {
    background: var(--color-background);
    cursor: not-allowed;
    opacity: 0.7;
  }

  [aria-invalid='true'] {
    border-color: var(--color-danger);
  }

  .field-error {
    color: var(--color-danger);
    font-size: 12px;
  }

  .field-hint {
    color: var(--color-text-secondary);
    font-size: 12px;
  }
</style>
