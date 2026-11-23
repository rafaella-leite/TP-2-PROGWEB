
<script>
    /**
     * @typedef {'0' | '1' | '2' | '3' | 'Em Elaboração' | 'Enviado' | 'Aprovado' | 'Reprovado'} Status
     */

    /** @type {Status} */
    export let status = '0';

    const statusConfig = {
        '0': {
            label: 'Em elaboração',
            className: 'elaboracao'
        },
        '1': {
            label: 'Enviado',
            className: 'enviado'
        },
        '2': {
            label: 'Aprovado',
            className: 'aprovado'
        },
        '3': {
            label: 'Reprovado',
            className: 'reprovado'
        },
        'Em Elaboração': {
            label: 'Em elaboração',
            className: 'elaboracao'
        },
        'Enviado': {
            label: 'Enviado',
            className: 'enviado'
        },
        'Aprovado': {
            label: 'Aprovado',
            className: 'aprovado'
        },
        'Reprovado': {
            label: 'Reprovado',
            className: 'reprovado'
        }
    };

    $: configuracao = statusConfig[status] ?? {
        label: 'Não informado',
        className: 'indefinido'
    };
</script>

<span class={`status-badge ${configuracao.className}`}>
    <span class="status-dot"></span>
    {configuracao.label}
</span>

<style>
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 11px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
    }

    .elaboracao {
        background: #FBF2DF;
        color: #A87927;
    }

    .enviado {
        background: #E7F0F5;
        color: #547E96;
    }

    .aprovado {
        background: #E3F1EA;
        color: #397568;
    }

    .reprovado {
        background: #FBE9E9;
        color: #C96B6B;
    }

    .indefinido {
        background: #EEF0EF;
        color: #77857F;
    }
</style>
