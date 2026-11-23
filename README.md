🎓 Projeto de Gestão de TCCs

Sistema web para gerenciamento de Trabalhos de Conclusão de Curso (TCC), desenvolvido como trabalho prático da disciplina GAC116 - Programação Web.

O projeto consiste no desenvolvimento de uma aplicação Front-end utilizando Svelte, integrada a uma API REST desenvolvida em Django REST Framework (DRF).

A aplicação permite consultar e gerenciar informações acadêmicas, cadastrar trabalhos, acompanhar seus status, realizar upload de documentos PDF e visualizar estatísticas por meio de um dashboard.

👥 Equipe

Projeto desenvolvido por:

Rafaella Maciel Pereira Leite
Juan
Vitor

Disciplina: GAC116 - Programação Web
Instituição: Universidade Federal de Lavras (UFLA)

🛠️ Tecnologias utilizadas

Backend:
Python
Django
Django REST Framework (DRF)
SQLite

Frontend:
Svelte
JavaScript
Vite
HTML5
CSS3

## ⚙️ Instalação e configuração

Siga as instruções abaixo para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.10 ou superior](https://www.python.org/downloads/)
- [Node.js (versão LTS)](https://nodejs.org/)

### 2. Clonar o repositório

Abra o terminal e execute:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd projeto-gestao-tccs
```

Para trabalhar na branch de desenvolvimento:

```bash
git checkout develop
```

### 3. Configurar o backend (Django)

Na raiz do projeto, crie um ambiente virtual:

```powershell
py -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Execute as migrações do banco de dados:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

### 4. Popular o banco de dados (opcional)

Para inserir dados fictícios e testar o funcionamento do sistema, execute:

```powershell
.\.venv\Scripts\python.exe populate.py
```

O script cadastra unidades acadêmicas, departamentos, cursos, alunos, professores e TCCs para demonstração.

**Observação:** os dados gerados são destinados ao ambiente de desenvolvimento.

### 5. Iniciar o backend

Na raiz do projeto, execute:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

O backend estará disponível em:

`http://127.0.0.1:8000/`

A API poderá ser acessada em:

`http://127.0.0.1:8000/api/`

Endpoint de estatísticas:

`http://127.0.0.1:8000/api/tccs/estatisticas/`

### 6. Configurar o frontend (Svelte)

Abra um segundo terminal no VS Code.

Entre na pasta do frontend:

```powershell
cd frontend
```

Instale as dependências:

```powershell
npm install
```

Inicie o servidor de desenvolvimento:

```powershell
npm run dev
```

O frontend estará disponível em:

`http://localhost:5173/`

### 7. Executar o projeto

Para utilizar o sistema, mantenha os dois servidores em execução simultaneamente:

| Serviço | Endereço |
|---|---|
| Backend Django | http://127.0.0.1:8000/ |
| Frontend Svelte | http://localhost:5173/ |
| API de estatísticas | http://127.0.0.1:8000/api/tccs/estatisticas/ |

