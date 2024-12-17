# Gerenciamento de Alunos e Cursos

Este é um sistema de gerenciamento de alunos e cursos desenvolvido com **FastAPI** e **SQLAlchemy**, que implementa operações CRUD completas.  

## Tecnologias Utilizadas

- **Python** (3.10+)
- **FastAPI**: Framework para criação de APIs rápidas e modernas.
- **SQLAlchemy**: ORM para manipulação do banco de dados.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **Pydantic**: Validação de dados.

## Funcionalidades

- **Cursos**:
  - Criar um curso.
  - Listar todos os cursos.
  - Visualizar detalhes de um curso.
  - Excluir um curso.

- **Alunos**:
  - Criar um aluno.
  - Listar todos os alunos.
  - Visualizar detalhes de um aluno.
  - Atualizar informações de um aluno.
  - Excluir um aluno.

### Estrutura do Banco de Dados

#### Tabelas:
1. **Cursos**:
   - `id`: ID único do curso.
   - `nome`: Nome do curso.
   - `descricao`: Descrição do curso.

2. **Alunos**:
   - `id`: ID único do aluno.
   - `nome`: Nome do aluno.
   - `idade`: Idade do aluno.
   - `curso_id`: Referência ao curso ao qual o aluno está matriculado.

---

## Instalação e Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
2. **Crie um ambiente virtual**
  ```
  python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
  ```
3. **Instale as dependências**
   ```
   pip install -r requirements.txt
   ```
