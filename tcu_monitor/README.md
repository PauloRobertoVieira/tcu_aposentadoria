```markdown
# Monitor de Status de Aposentadoria do TCU

Este é um aplicativo Flask que permite monitorar o status de aposentadoria de pessoas consultando dados do Tribunal de Contas da União (TCU). Ele oferece funcionalidades para cadastrar, listar, editar e excluir pessoas, além de exibir o histórico de consultas e um relatório geral.

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado em seu sistema:

* **Python 3.7+**: A linguagem de programação utilizada no desenvolvimento.
* **pip**: O gerenciador de pacotes do Python, geralmente instalado com o Python.

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências do aplicativo:

### 1. Clonar o Repositório (Opcional)

Se você recebeu o código de um repositório (como GitHub), clone-o para sua máquina local:

```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_REPOSITÓRIO]
```

### 2. Criar um Ambiente Virtual

É altamente recomendado criar um ambiente virtual isolado para este projeto. Isso evita conflitos com outras dependências do seu sistema.

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Após ativar o ambiente virtual, você verá o nome do ambiente (`(venv)`) no início da linha de comando.

### 3. Instalar as Dependências

Com o ambiente virtual ativado, navegue até o diretório raiz do projeto (onde o arquivo `app.py` está localizado) e instale as dependências listadas no arquivo `requirements.txt` (se houver). Como não há um arquivo `requirements.txt` no código fornecido, vamos criar um e instalar as bibliotecas necessárias:

Crie um arquivo chamado `requirements.txt` na raiz do seu projeto com o seguinte conteúdo:

```
Flask
Flask-SQLAlchemy
requests
APScheduler
```

Agora, instale as dependências usando o pip:

```bash
pip install -r requirements.txt
```

## Configurações Necessárias

As configurações do aplicativo são gerenciadas pelo arquivo `config.py`. Por padrão, o aplicativo utiliza um banco de dados SQLite chamado `tcu_monitor.db` que será criado na mesma pasta do projeto.

### Configurar o Banco de Dados (SQLite por padrão)

Para inicializar o banco de dados, execute os seguintes comandos no shell do Flask:

```bash
flask shell
```

Dentro do shell do Flask, execute os comandos Python para criar as tabelas no banco de dados:

```python
>>> from app import db
>>> with app.app_context():
...     db.create_all()
...
>>> exit()
```

**Observação:** Certifique-se de que a variável `app` esteja definida e importada corretamente no seu ambiente Flask. O arquivo `app.py` já instancia o `db` e o inicializa com o aplicativo.

### Configurações Adicionais (Opcional)

Você pode personalizar as configurações através de variáveis de ambiente. Se a variável de ambiente `DATABASE_URL` estiver definida, o SQLAlchemy utilizará essa URL para conectar ao banco de dados. Da mesma forma, a variável `SECRET_KEY` pode ser definida para uma chave secreta personalizada (importante para segurança em ambientes de produção).

Para definir variáveis de ambiente no Linux/macOS:

```bash
export SECRET_KEY='sua_chave_secreta'
export DATABASE_URL='postgresql://usuario:senha@host:porta/banco_de_dados'
```

No Windows:

```bash
set SECRET_KEY='sua_chave_secreta'
set DATABASE_URL='postgresql://usuario:senha@host:porta/banco_de_dados'
```

**Observação:** Para manter essas variáveis de ambiente persistentes, você pode adicioná-las ao seu arquivo de configuração do shell (por exemplo, `.bashrc`, `.zshrc` no Linux/macOS ou através das configurações do sistema no Windows).

## Como Executar

Siga os passos abaixo para executar a aplicação:

1.  Certifique-se de estar no diretório raiz do projeto e com o ambiente virtual ativado (`(venv)` no prompt).
2.  Execute o seguinte comando para iniciar o servidor de desenvolvimento do Flask:

```bash
python app.py
```

Você deverá ver uma mensagem indicando que o servidor de desenvolvimento do Flask está rodando (geralmente em `http://127.0.0.1:5000/`).

## Acessar no Navegador

Abra seu navegador web e acesse o seguinte endereço:

```
http://localhost:5000
```

Você deverá ver a página inicial do aplicativo com informações sobre o número total de pessoas cadastradas e seus respectivos status.

## Funcionalidades Principais

O aplicativo oferece as seguintes funcionalidades através da interface web:

* **Página Inicial (`/`)**: Exibe um resumo com o número total de pessoas e a contagem por status (Aguardando autuação, Concedida, Apreciado ilegal).
* **Listar Pessoas (`/pessoas`)**: Mostra uma lista de todas as pessoas cadastradas, ordenadas por nome.
* **Detalhes da Pessoa (`/pessoa/<id>`)**: Exibe os detalhes de uma pessoa específica, incluindo seu histórico de consultas ao TCU.
* **Cadastrar Pessoa (`/pessoa/cadastrar`)**: Um formulário para adicionar novas pessoas ao sistema, solicitando matrícula, nome e CPF. Ao cadastrar uma nova pessoa, uma consulta ao TCU é iniciada para obter o status da aposentadoria.
* **Editar Pessoa (`/pessoa/editar/<id>`)**: Um formulário para editar os dados de uma pessoa existente (matrícula, nome, CPF e status de ativo).
* **Excluir Pessoa (`/pessoa/excluir/<id>`)**: Permite remover uma pessoa do sistema.
* **API de Pessoas (`/api/pessoas`)**: Retorna um JSON com os dados de todas as pessoas cadastradas.
* **API de Histórico por CPF (`/api/pessoas/<cpf>/historico`)**: Retorna um JSON com o histórico de consultas de uma pessoa específica, identificada pelo CPF.
* **Relatório (`/relatorio`)**: Exibe um relatório com a lista de todas as pessoas cadastradas e a data e hora da geração do relatório.

## Agendamento de Tarefas

O aplicativo utiliza o `APScheduler` para agendar uma tarefa que consulta o status de aposentadoria de todas as pessoas ativas no sistema uma vez por mês (no dia 1º às 4 da manhã). Essa tarefa é definida na função `agendar_tarefas` no arquivo `scheduler.py`.

## Modelos de Dados

O aplicativo utiliza o SQLAlchemy para definir e interagir com o banco de dados:

* **Pessoa (`models/pessoa.py`)**: Representa uma pessoa monitorada, com atributos como `id`, `matricula`, `nome`, `cpf`, `status`, `url_consulta`, `ativo`, `data_cadastro` e `data_atualizacao`.
* **HistoricoConsulta (`models/historico.py`)**: Registra o histórico de consultas ao TCU para cada pessoa, incluindo `data_consulta`, `status`, `detalhes` e `url_consulta`.

## Serviços

* **`tcu_service.py`**: Contém as funções para interagir com a API do TCU (`consultar_status_aposentadoria`) e para consultar o status de todas as pessoas ativas (`consultar_todos`). A função `consultar_status_aposentadoria` faz uma requisição para a API do TCU com o CPF da pessoa para obter informações sobre seu status de aposentadoria e salva essa informação no banco de dados, juntamente com um registro no histórico de consultas.
* **`scheduler.py`**: Configura e inicia o agendador de tarefas (`APScheduler`) para executar a consulta periódica de status.
