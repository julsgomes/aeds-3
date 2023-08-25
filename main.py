import pandas as pd
import requests



def relacao_deputado_deputado(graph_voto, graph):
  flag = {}
  flag1 = 0
  for id1 in graph_voto:
    for dep in graph_voto[id1]:
      for dep2 in graph_voto[id1]:
        if dep2 not in flag:
          if dep != dep2:
            if dep in graph:
              for vizinhos in graph[dep]:
                if vizinhos == dep2:
                  flag1 = 1
              if flag1 == 1:
                graph[dep][dep2] += 1
              if flag1 == 0:
                graph[dep][dep2] = 1
            else:
              graph[dep][dep2] = 1
        flag1 = 0

      flag[dep] = {}  #flag para que nao aja ambiguidade na soma
    flag.clear()

#Função da API
def read_from_api():
  graph = {}
  graph_voto_nao = {}
  graph_voto_sim = {}
  votes_count = {}
  verifica = True
  i = 0
  while verifica == True:
    i += 1
    url = "https://dadosabertos.camara.leg.br/api/v2/votacoes"
    parameters = {
      "dataInicio": "2022-01-01",
      "dataFim": "2022-03-01",
      "ordem": "DESC",
      "ordenarPor": "dataHoraRegistro",
      "pagina": i
    }
    headers = {"accept": "application/json"}
    response = requests.get(url=url, params=parameters, headers=headers)

    if response.status_code == 200:
      data = response.json()
      tam = (len(data["dados"]))
      if tam < 200:
        verifica = False

      for votacao in data["dados"]:
        id_votacao = votacao["id"]
        url = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id_votacao}/votos"
        headers = {"accept": "application/json"}
        response2 = requests.get(url=url, headers=headers)

        if response2.status_code == 200:
          graph_voto_nao[id_votacao] = []
          graph_voto_sim[id_votacao] = []
          data2 = response2.json()
          for projeto in data2["dados"]:
            voto = projeto["tipoVoto"]
            deputado = projeto["deputado_"]["nome"]
            if deputado not in graph:
              graph[deputado] = {}
              votes_count[deputado] = 1
            else:
              votes_count[deputado] += 1
            if voto == "Sim":
              graph_voto_sim[id_votacao].append(deputado)
            if voto == "Não":
              graph_voto_nao[id_votacao].append(deputado)

        else:
          print("Falha ao fazer a solicitação à API da Câmara dos Deputados.")
          break

    else:
      print("Falha ao fazer a solicitação à API da Câmara dos Deputados.")
      break

  #Criar grafo direcional de votos iguais entre deputados no msm projeto
  relacao_deputado_deputado(graph_voto_sim, graph)
  relacao_deputado_deputado(graph_voto_nao, graph)

  return graph, votes_count


# Função para ler o arquivo de votações e criar o grafo
def read_votes_file(file_name):
  df = pd.read_excel(file_name)
  graph = {}
  votes_count = {}

  for _, row in df.iterrows():
    deputado = row["deputado_nome"]
    if deputado not in graph:
      graph[deputado] = {}
      votes_count[deputado] = 0

  for _, row in df.iterrows():
    deputado1 = row["deputado_nome"]
    numero_proj1 = row["idVotacao"]
    voto1 = row["voto"]
    votes_count[deputado1] += 1

    for _, row2 in df.iterrows():
      deputado2 = row2["deputado_nome"]
      numero_proj2 = row2["idVotacao"]
      voto2 = row2["voto"]
      if deputado1 != deputado2 and voto1 == voto2 and numero_proj1 == numero_proj2:
        if deputado2 in graph[deputado1]:
          graph[deputado1][deputado2] += 1
        else:
          graph[deputado1][deputado2] = 1

  return graph, votes_count


# Função para escrever o grafo em um arquivo de texto
def write_graph_file(graph, file_name):
  with open(file_name, "w") as file:
    file.write(f"{len(graph)} {sum(len(edges) for edges in graph.values())}\n")
    for node, edges in graph.items():
      for neighbor, weight in edges.items():
        file.write(
          f"{node.replace(' ', '_')} {neighbor.replace(' ', '_')} {weight}\n")


# Função para escrever o número de votações de cada deputado em um arquivo de texto
def write_votes_count_file(votes_count, file_name):
  with open(file_name, "w") as file:
    for deputado, count in votes_count.items():
      file.write(f"{deputado.replace(' ', '_')} {count}\n")


# Função principal
def main():
  file_name = input("Informe o arquivo de votações: ")
  print("Processando...")

  graph, votes_count = read_votes_file(file_name)

  graph_file_name = file_name.replace(".xlsx", "-graph.txt")
  write_graph_file(graph, graph_file_name)

  votes_count_file_name = file_name.replace(".xlsx", "-votes-count.txt")
  write_votes_count_file(votes_count, votes_count_file_name)

  print("O grafo foi escrito no arquivo:")
  print(f"- {graph_file_name}")
  print("A contagem de votações foi escrita no arquivo:")
  print(f"- {votes_count_file_name}")


if __name__ == "__main__":
  v = int(input("Insira o método de pesquisa: \n 1 - Dados de um arquivo excel\n 2 - Dados diretamente da API\n"))

  if v == 2:
    print("Processando...")
    graph, vote_count = read_from_api()

    write_graph_file(graph, "z-graph.txt")
    write_votes_count_file(vote_count, "z-votes-count.txt")

    print("O grafo foi escrito no arquivo:")
    print("z-graph.txt")
    print("A contagem de votações foi escrita no arquivo:")
    print("z-votes-count.txt")
  if v == 1:
    main()
  if v <= 0 or v > 2:
    print("Escolha entre 1 e 2 apenas!")
