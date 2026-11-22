
<script>
  export let title = '';
  export let value = '--';
  export let description = '';
  export let icon = '▦';
  export let color = 'green';
</script>

<div class="stat-card">
  <div class="card-top">
    <span class="card-title">{title}</span>

    <div class="card-icon" class:blue={color === 'blue'}
      class:gold={color === 'gold'}
      class:red={color === 'red'}>
      {icon}
    </div>
  </div>

  <div class="card-value">{value}</div>

  <p class="card-description">{description}</p>
</div>

<style>
  .stat-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 22px;
    box-shadow: var(--shadow-card);
    min-width: 0;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(32, 76, 67, 0.08);
  }

  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }

  .card-title {
    font-size: 12px;
    color: var(--color-text-secondary);
    font-weight: 500;
  }

  .card-icon {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: var(--color-mint);
    color: var(--color-primary);
    font-size: 19px;
  }

  .card-icon.blue {
    background: #E4EEF2;
    color: #527F91;
  }

  .card-icon.gold {
    background: #F7F0E3;
    color: #B58A43;
  }

  .card-icon.red {
    background: #F6E9E7;
    color: #B76A61;
  }

  .card-value {
    font-family: 'Manrope', sans-serif;
    font-size: 29px;
    font-weight: 800;
    color: var(--color-text);
    margin-top: 17px;
  }

  .card-description {
    font-size: 11px;
    color: var(--color-text-light);
    margin-top: 3px;
  }
</style>
