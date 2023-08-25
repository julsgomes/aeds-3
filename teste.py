import pandas as pd


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
  main()
