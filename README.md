# Projeto de Análise de Votação da Câmara dos Deputados

## Descrição

Este projeto tem como objetivo analisar os padrões de votação na Câmara dos Deputados. Utilizando dados da API da Câmara e/ou de um arquivo Excel, o projeto gera um grafo de relacionamentos entre deputados com base em suas votações. Cada nó representa um deputado e as arestas indicam votações similares.

## Funcionalidades

- Leitura de dados da API da Câmara dos Deputados
- Leitura de dados de um arquivo Excel
- Criação de um grafo de votação
- Diversas métricas e propriedades de grafo (conectividade, grau, etc.)

## Requisitos

- Python 3.x
- Pandas
- Requests

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu_usuario/seu_repositorio.git
```

Instale as dependências:

```bash
pip install pandas requests
```

## Uso

### Leitura da API

```python
graph, votes_count = read_from_api()
```

### Leitura do arquivo Excel

```python
graph, votes_count = read_votes_file('seuarquivo.xlsx')
```

## Estrutura do Código

- `Graph`: Classe responsável pela estrutura de dados do grafo e suas operações.
- `read_from_api`: Função para ler dados da API da Câmara dos Deputados.
- `read_votes_file`: Função para ler dados de um arquivo Excel.
- `write_graph_file`: Função para escrever o grafo em um arquivo de texto.
- `relacao_deputado_deputado`: Função para atualizar as arestas do grafo com base em votações similares.
