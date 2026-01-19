# Desafio MBA Engenharia de Software com IA - Full Cycle

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Sobre o Projeto

Sistema desenvolvido como parte do MBA em Engenharia de Software com IA da Full Cycle. Implementa um sistema de RAG (Retrieval-Augmented Generation) que permite realizar consultas inteligentes sobre documentos PDF através de busca semântica e geração de respostas contextualizadas.

O projeto utiliza embeddings vetoriais para indexar o conteúdo dos documentos e modelos de linguagem (LLM) para gerar respostas precisas baseadas no contexto recuperado.

## Tecnologias Utilizadas

- **LangChain**: Framework para desenvolvimento de aplicações com LLM
- **PostgreSQL + pgvector**: Banco de dados vetorial para armazenamento de embeddings
- **Google Gemini / OpenAI**: Modelos de linguagem e geração de embeddings
- **PyPDF**: Biblioteca para processamento e extração de texto de documentos PDF
- **Python 3.10+**: Linguagem de programação principal
- **Docker**: Containerização do banco de dados

## Estrutura do Projeto

```
.
├── src/
│   ├── ingest.py          # Script de ingestão de PDFs
│   ├── chat.py            # Interface de chat interativo
│   └── ...
├── docker-compose.yml     # Configuração do PostgreSQL
├── requirements.txt       # Dependências do projeto
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md             # Documentação do projeto
```

## Instalação

Siga os passos abaixo para configurar e executar o projeto.

### 1. Pré-requisitos

- Python 3.10 ou superior
- Docker e Docker Compose
- Conta no Google AI (para `GOOGLE_API_KEY`) ou OpenAI (para `OPENAI_API_KEY`)
- Git (para clonar o repositório)

### 2. Configuração do Ambiente Virtual

É recomendado utilizar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# No Linux/macOS:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate
```

### 3. Instalação das Dependências

Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configuração das Variáveis de Ambiente

Copie o arquivo de exemplo `.env.example` para `.env` e preencha com suas credenciais.

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as seguintes variáveis:

```bash
# API Keys (escolha um provedor)
GOOGLE_API_KEY=sua_chave_aqui
# OPENAI_API_KEY=sua_chave_aqui

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db

# Configurações opcionais
COLLECTION_NAME=document_vectors
BATCH_SIZE=100
BATCH_DELAY=1
```

**Variáveis importantes:**
- `GOOGLE_API_KEY` ou `OPENAI_API_KEY`: Chave de API do provedor de LLM escolhido
- `DATABASE_URL`: URL de conexão com o banco de dados (padrão já configurado para o Docker)
- `COLLECTION_NAME`: Nome da coleção de vetores (opcional)
- `BATCH_SIZE`: Tamanho do lote de documentos a serem inseridos por vez
- `BATCH_DELAY`: Tempo de espera em segundos entre a inserção de lotes

### 5. Inicialização do Banco de Dados

Suba o container do PostgreSQL com a extensão `pgvector` habilitada:

```bash
docker compose up -d
```

Verifique se o container está rodando:

```bash
docker compose ps
```

---

## Como Ingerir um Documento PDF

Para processar um arquivo PDF e armazenar seus vetores no banco de dados, utilize o script `ingest.py`.

Você pode passar o caminho do arquivo diretamente via linha de comando:

```bash
python src/ingest.py --pdf_path caminho/para/seu/documento.pdf
```

Alternativamente, se você definiu a variável `PDF_PATH` no arquivo `.env`, basta executar:

```bash
python src/ingest.py
```

### Parâmetros Opcionais

- `--collection_name`: Nome da coleção de vetores no banco de dados (padrão: `document_vectors` ou o definido no `.env`)
- `--batch_size`: Tamanho do lote de documentos a serem inseridos por vez (útil para evitar timeouts ou rate limits)
- `--batch_delay`: Tempo de espera em segundos entre a inserção de lotes

Exemplo com parâmetros personalizados:

```bash
python src/ingest.py --pdf_path documento.pdf --collection_name minha_colecao --batch_size 50 --batch_delay 2
```

### Processo de Ingestão

O script irá:
1. Carregar o arquivo PDF
2. Dividir o texto em partes menores (chunks)
3. Gerar embeddings vetoriais para cada chunk
4. Armazenar os vetores no banco de dados PostgreSQL com pgvector

---

## Como Fazer Perguntas (Chat)

Após a ingestão do documento, você pode interagir com o conteúdo através do chat. Execute o script `chat.py`:

```bash
python src/chat.py
```

### Parâmetros Opcionais

- `--collection_name`: Nome da coleção de vetores a ser consultada

**Importante:** Se você escolheu um nome diferente para a coleção durante a ingestão (usando `--collection_name`), este mesmo nome deve ser usado para fazer as perguntas, caso contrário o sistema não encontrará os documentos.

Exemplo:

```bash
python src/chat.py --collection_name minha_colecao
```

O sistema iniciará um chat interativo no terminal. Digite suas perguntas e o sistema buscará as informações relevantes no documento ingerido para gerar a resposta.

Para sair do chat, digite `sair`, `exit` ou `q`.

### Exemplo de Uso do Chat

```bash
python src/chat.py

Bem-vindo ao RAG Chat!
Usando coleção: DOC1_COLLECTION
Este programa responde perguntas sobre o documento PDF ingerido.
Nota: Este chat não possui memória. Cada pergunta é tratada independentemente.
Digite sua pergunta abaixo. Para sair, digite 'sair', 'exit' ou 'q'.
--------------------------------------------------

Você: qual o faturamento da empresa Alfa Logística Holding?
Processando...

Resposta: O faturamento da empresa Alfa Logística Holding é R$ 62.934.469,48.
--------------------------------------------------

Você: Quais empresas foram fundadas até 1950?
Processando...

Resposta: As empresas fundadas até 1950 são:

*   Alfa Agronegócio Indústria (1931)
*   Alfa Logística Holding (1948)
*   Alfa Tecnologia Holding (1950)
*   Alfa Turismo S.A. (1940)
*   Aliança Consultoria LTDA (1940)
*   Aliança Esportes Comércio (1945)
*   Alta Alimentos Comércio (1943)
*   Alta Construtora Participações (1931)
*   Alta Construtora Serviços (1937)
*   Alta Serviços Holding (1948)
*   Atlas Construtora S.A. (1939)
*   Atlas Higiene Indústria (1939)
*   Atlas Petróleo Serviços (1934)
*   Aurora Construtora Holding (1942)
*   Aurora Educação Indústria (1932)
*   Beta Logística Participações (1950)
*   Beta Serviços Comércio (1932)
*   Beta Telecom Participações (1933)
*   Beta Transporte ME (1942)
*   Brava Consultoria Comércio (1942)
*   Bronze Logística Serviços (1935)
*   Bronze Publicidade S.A. (1942)
*   Clara Bebidas Holding (1938)
*   Delta Software ME (1936)
*   Delta Telecom LTDA (1943)
*   Delta Turismo Holding (1944)
*   Dourado Cosméticos EPP (1944)
*   Dourado Entretenimento Comércio (1932)
*   Dourado Hardware Comércio (1941)
*   Rápida Hardware LTDA (1933)
*   Rápida Mídia Participações (1944)
*   Rápida Saúde Holding (1937)
*   Rápida Software Serviços (1941)
*   Zenith Papel e Celulose EPP (1931)
*   Zenith Seguros Holding (1942)
*   Ágil Hotelaria ME (1940)
*   Âmbar Automotiva Serviços (1944)
*   Âmbar E-commerce LTDA (1930)
*   Âmbar Games Participações (1933)
--------------------------------------------------

Você: sair
Encerrando o chat. Até logo!

Process finished with exit code 0
```

---

## Solução de Problemas Comuns

### Erro de conexão com banco de dados

**Problema:** `connection refused` ou erro ao conectar no PostgreSQL

**Solução:**
```bash
# Verifique se o container está rodando
docker compose ps

# Se não estiver, inicie novamente
docker compose up -d

# Verifique os logs do container
docker compose logs db
```

### Erro de API Key inválida

**Problema:** `Invalid API key` ou `Authentication failed`

**Solução:**
- Confirme que a variável está corretamente definida no `.env` sem espaços ou aspas extras
- Verifique se a chave é válida no console do provedor (Google AI Studio ou OpenAI)
- Certifique-se de que escolheu apenas UM provedor (Google OU OpenAI)

### Timeout durante ingestão de documentos grandes

**Problema:** Erro de timeout ao processar PDFs muito grandes

**Solução:**
```bash
# Aumente o batch_delay ou diminua o batch_size
python src/ingest.py --pdf_path documento.pdf --batch_size 20 --batch_delay 3
```

### Coleção não encontrada ao fazer perguntas

**Problema:** `Collection not found` ou respostas vazias

**Solução:**
- Certifique-se de usar o mesmo `collection_name` tanto na ingestão quanto no chat
- Verifique se a ingestão foi concluída com sucesso
- Confirme que o banco de dados contém os dados usando um cliente PostgreSQL

### Módulo não encontrado

**Problema:** `ModuleNotFoundError: No module named 'X'`

**Solução:**
```bash
# Certifique-se de que o ambiente virtual está ativado
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## Autor

**Jeandeson de Oliveira Merelis**

Projeto desenvolvido como parte do MBA em Engenharia de Software com IA - Full Cycle

---

## Agradecimentos

- Full Cycle pela excelente formação em Engenharia de Software com IA
- Comunidade LangChain pelos recursos e documentação
- Contribuidores do projeto pgvector

---
