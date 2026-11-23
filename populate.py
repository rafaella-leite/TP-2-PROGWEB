
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcc_project.settings')
django.setup()

from django.db import transaction
from core.models import (
    UnidadeAcademica,
    Departamento,
    Curso,
    Aluno,
    Professor,
    TCC
)


@transaction.atomic
def popular_banco():

    print('\nIniciando carga de dados...\n')

    # -------------------------------------------------
    # 1. UNIDADES ACADÊMICAS
    # -------------------------------------------------

    unidades_dados = [
        ('Faculdade de Ciências Exatas', 'FCEX'),
        ('Faculdade de Ciências Humanas', 'FCH'),
        ('Faculdade de Engenharia', 'FENG'),
    ]

    unidades = {}

    for nome, sigla in unidades_dados:
        unidade, _ = UnidadeAcademica.objects.get_or_create(
            sigla=sigla,
            defaults={'nome': nome}
        )
        unidades[sigla] = unidade

    print('Unidades acadêmicas cadastradas.')

    # -------------------------------------------------
    # 2. DEPARTAMENTOS
    # -------------------------------------------------

    departamentos_dados = [
        ('Departamento de Computação', 'DCC', 'FCEX'),
        ('Departamento de Matemática', 'DMT', 'FCEX'),
        ('Departamento de Administração', 'DAD', 'FCH'),
        ('Departamento de Educação', 'DED', 'FCH'),
        ('Departamento de Engenharia', 'DEN', 'FENG'),
    ]

    departamentos = {}

    for nome, sigla, unidade_sigla in departamentos_dados:
        departamento, _ = Departamento.objects.get_or_create(
            sigla=sigla,
            defaults={
                'nome': nome,
                'unidade_academica': unidades[unidade_sigla]
            }
        )
        departamentos[sigla] = departamento

    print('Departamentos cadastrados.')

    # -------------------------------------------------
    # 3. CURSOS
    # -------------------------------------------------

    cursos_dados = [
        ('Sistemas de Informação', 'SI', 'CUR001'),
        ('Ciência da Computação', 'CC', 'CUR002'),
        ('Administração', 'ADM', 'CUR003'),
        ('Engenharia de Software', 'ES', 'CUR004'),
        ('Pedagogia', 'PED', 'CUR005'),
        ('Engenharia de Produção', 'EP', 'CUR006'),
    ]

    cursos = []

    for nome, sigla, codigo in cursos_dados:
        curso, _ = Curso.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nome': nome,
                'sigla': sigla
            }
        )
        cursos.append(curso)

    print('Cursos cadastrados.')

    # -------------------------------------------------
    # 4. ALUNOS
    # -------------------------------------------------

    alunos_dados = [
        'Ana Clara Martins',
        'Bruno Henrique Souza',
        'Camila Oliveira Costa',
        'Daniel Ferreira Lima',
        'Eduarda Santos Alves',
        'Felipe Rodrigues Silva',
        'Gabriela Mendes Rocha',
        'Henrique Carvalho Dias',
        'Isabela Ribeiro Castro',
        'João Pedro Almeida',
        'Larissa Fernandes Melo',
        'Lucas Barbosa Moreira',
    ]

    alunos = []

    for i, nome in enumerate(alunos_dados):
        aluno, _ = Aluno.objects.get_or_create(
            matricula=f'2026{i + 1:04d}',
            defaults={
                'nome': nome,
                'curso': cursos[i % len(cursos)]
            }
        )
        alunos.append(aluno)

    print('Alunos cadastrados.')

    # -------------------------------------------------
    # 5. PROFESSORES
    # -------------------------------------------------

    professores_dados = [
        ('Mariana Costa', 'DCC'),
        ('Roberto Almeida', 'DCC'),
        ('Fernanda Martins', 'DMT'),
        ('Carlos Eduardo Lima', 'DAD'),
        ('Patrícia Oliveira', 'DEN'),
    ]

    professores = []

    for nome, departamento_sigla in professores_dados:
        professor, _ = Professor.objects.get_or_create(
            nome=nome,
            departamento=departamentos[departamento_sigla]
        )
        professores.append(professor)

    print('Professores cadastrados.')

    # -------------------------------------------------
    # 6. TCCs
    # -------------------------------------------------

    
    tccs_dados = [
        # EM ELABORAÇÃO: 5
        ('Desenvolvimento de uma plataforma de acessibilidade web', '0', 'MONOGRAFIA', 'PT'),
        ('Inteligência artificial aplicada à educação', '0', 'ARTIGO', 'PT'),
        ('Análise de experiência do usuário em sistemas acadêmicos', '0', 'MONOGRAFIA', 'PT'),
        ('Segurança da informação em aplicações web', '0', 'ARTIGO', 'EN'),
        ('Aplicações de aprendizado de máquina na saúde', '0', 'MONOGRAFIA', 'PT'),

        # ENVIADOS: 5
        ('Desenvolvimento de um sistema de gestão acadêmica', '1', 'RELATORIO_TECNICO', 'PT'),
        ('Análise de usabilidade em aplicativos móveis', '1', 'MONOGRAFIA', 'PT'),
        ('Automação de processos organizacionais', '1', 'RELATORIO_ESTAGIO', 'PT'),
        ('Impactos da transformação digital nas empresas', '1', 'ARTIGO', 'PT'),
        ('Arquitetura de software para sistemas distribuídos', '1', 'MONOGRAFIA', 'EN'),

        # APROVADOS: 5
        ('Tecnologias assistivas no ambiente educacional', '2', 'ARTIGO', 'PT'),
        ('Gestão de projetos utilizando metodologias ágeis', '2', 'MONOGRAFIA', 'PT'),
        ('Análise de dados aplicada à tomada de decisão', '2', 'ARTIGO', 'EN'),
        ('Sistema inteligente de recomendação acadêmica', '2', 'MONOGRAFIA', 'PT'),
        ('O uso de tecnologias digitais na educação superior', '2', 'RELATORIO_ESTAGIO', 'PT'),

        # REPROVADOS: 5
        ('Desenvolvimento de API para gestão de documentos', '3', 'RELATORIO_TECNICO', 'PT'),
        ('Análise de desempenho em redes de computadores', '3', 'MONOGRAFIA', 'PT'),
        ('Aplicação de técnicas de mineração de dados', '3', 'ARTIGO', 'EN'),
        ('Estudo de segurança em aplicações distribuídas', '3', 'ARTIGO', 'PT'),
        ('Sistema de monitoramento de infraestrutura', '3', 'RELATORIO_TECNICO', 'PT'),
    ]


    tipos = [
        'MONOGRAFIA',
        'RELATORIO_ESTAGIO',
        'RELATORIO_TECNICO',
        'ARTIGO'
    ]

    idiomas = ['PT', 'EN']

    semestres = [
        '2024/1',
        '2024/2',
        '2025/1',
        '2025/2',
        '2026/1'
    ]

    criados = 0

    for i, (titulo, status, tipo, idioma) in enumerate(tccs_dados):

        orientador = professores[i % 5]

        presidente = professores[(i + 1) % 5]
        primeiro_membro = professores[(i + 2) % 5]
        segundo_membro = professores[(i + 3) % 5]

        # Alguns trabalhos terão coorientador.
        coorientador = (
            professores[(i + 4) % 5]
            if i % 2 == 0
            else None
        )

        tcc, criado = TCC.objects.update_or_create(
            titulo=titulo,
            defaults={
                'resumo': (
                    f'Este trabalho apresenta um estudo sobre {titulo.lower()}. '
                    'O objetivo é investigar soluções, analisar resultados '
                    'e apresentar contribuições para a área de conhecimento.'
                ),
                'palavras_chave': 'Tecnologia, Pesquisa, Inovação',
                'tipo': tipo,
                'idioma': idioma,
                'aluno': alunos[i % len(alunos)],
                'orientador': orientador,
                'coorientador': coorientador,
                'presidente': presidente,
                'primeiro_membro': primeiro_membro,
                'segundo_membro': segundo_membro,
                'semestre_letivo_defesa': semestres[i % len(semestres)],
                'status': status,
            }
        )

        if criado:
            criados += 1

    print(f'{criados} novos TCCs cadastrados.')

    print('\nCarga de dados finalizada!')
    print('--------------------------------')
    print(f'Unidades: {UnidadeAcademica.objects.count()}')
    print(f'Departamentos: {Departamento.objects.count()}')
    print(f'Cursos: {Curso.objects.count()}')
    print(f'Alunos: {Aluno.objects.count()}')
    print(f'Professores: {Professor.objects.count()}')
    print(f'TCCs: {TCC.objects.count()}')
    print('--------------------------------\n')


if __name__ == '__main__':
    popular_banco()
