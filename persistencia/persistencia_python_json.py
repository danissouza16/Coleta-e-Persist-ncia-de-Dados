import requests as req
import json
from uuid import uuid4
from bs4 import BeautifulSoup

base_url = "https://crudcrud.com/api/5df55e2789b341f2a30c2fdccc3d556d/movies"
headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

api_url = "https://api.themoviedb.org/3/search/movie?query="

def get_all():
    response = req.get(base_url)
    if response.status_code == 200:
        print(response.json())

def get_filme(id):
    url = f"{base_url}/{id}"
    response = req.get(url)
    if response.status_code == 200:
        print(response.json())  

def create_filme(title, sinopse, elenco, direcao, nota, onde_assistir, critica, classificacao, nacionalidade):
    body = {
        "title": str(title), 
        "sinopse": str(sinopse), 
        "elenco": str(elenco), 
        "direcao": str(direcao),
        "nota": str(nota),
        "onde_assistir": str(onde_assistir),
        "critica": str(critica),
        "classificacao": str(classificacao),
        "nacionalidade": str(nacionalidade)
    }
    response = req.post(base_url, json=body)    
    if response.status_code == 201:
       print("Filme adicionado na base de dados!")
    else:
       print(response.status_code)
       print("Adição de filme deu errado.")

def update_filme(id):
    
  body = {
        "_id": id,
        "title": input("Título novo: "), 
        "sinopse": input("Sinopse nova: "), 
        "elenco": input("Elenco novo: "), 
        "direcao": input("Direção novo: "),
        "nota": input("Nota nova: "),
        "onde_assistir": input("Lugar para assistir novo: "),
        "critica": input("Crítica nova: "),
        "classificacao": input("Classifição nova: "),
        "nacionalidade": input("Nacionalidade nova: ")
    }
  url = f"{base_url}/{body['_id']}"
  response = req.put(url, json=body)
  if response.status_code == 200:
    print("Atualização bem-sucedida!")

def delete_filme(id):

  url = f"{base_url}/{id}"
  response = req.delete(url)
  if response.status_code == 200:
    print("Deletado com sucesso!")
  else:
    print("Erro ao deletar filme da base de dados.")

def acessa_api(titulo):
  api_url = "https://api.themoviedb.org/3/search/movie?query=" + titulo
  response = req.get(api_url, headers= {"Authorization" : "98c40c9b884cba77a096dbce916f86f2"})
  if response.status_code == req.codes.ok:
     print(response.json())

def salvar_json_local():
    response = req.get(base_url)
    if response.status_code == 200:
        dados = response.json()
        with open("CRUD.json", 'w') as arquivo_json:
            json.dump(dados, arquivo_json)
        print("Dados salvos em CRUD.json")
    else:
        print("Erro ao obter dados do CRUDCRUD:", response.status_code)


resposta = input("\nCole o link do filme que você deseja conhecer (site Adoro Cinema): ")
response = req.get(resposta, headers=headers)
if response.status_code == 200:
    html = BeautifulSoup(response.text, "html.parser")
else:
    print("Erro ao acessar o site.")
    exit()



#o programa acessa o site do filme a partir do link e pode adicioná-lo a api do crudcrud
#lista de filmes testados (pode-se pegar qualquer do site dos melhores filmes do adorofilmes)
  #https://www.adorocinema.com/filmes/filme-1628/
  #https://www.adorocinema.com/filmes/filme-11736/
  #https://www.adorocinema.com/filmes/filme-9393/
  #https://www.adorocinema.com/filmes/filme-10568/
while True:
  print("---------------------------------")
  print("Comandos disponíveis:\n")
  print("1. Mostrar filmes da base de dados.")
  print("2. Mostrar um filme da base de dados.")
  print("3. Adicionar filme na base de dados.")
  print("4. Atualizar filme na base de dados.")
  print("5. Deletar filme na base de dados.")
  print("6. Acessar API de filmes")
  print("7. Salvar em JSON local")
  print("8. Encerrar programa")
  print("---------------------------------\n")
  command = input("\nDigite o número do comando desejado: ")
  if command == "1":
    get_all()
  elif command == "2":
    id = input("Qual o id do filme? ")
    get_filme(id)
  elif command == "3":
    titulo = html.find("div", attrs={"class": "titlebar-title titlebar-title-xl"})
    titulo_text = titulo.text.strip() if titulo else "Título não encontrado"

    paragrafos = [p.text.strip() for p in html.find_all("p")]
    sinopse = paragrafos[0] if paragrafos else "Sinopse não encontrada"

    elenco = html.find("div", attrs={"class": "meta-body-item meta-body-actor"})
    elenco_text = elenco.text.strip() if elenco else "Elenco não encontrado"

    direcao = html.find("div", attrs={"class": "meta-body-item meta-body-direction meta-body-oneline"})
    direcao_text = direcao.text.strip() if direcao else "Direção não encontrada"

    avaliacao = html.find("span", attrs={"class": "stareval-note"})
    avaliacao_text = avaliacao.text.strip() if avaliacao else "Avaliação não encontrada"

    onde_assistir = html.find("div", attrs={"class": "provider-tile-text"})
    onde_assistir_text = onde_assistir.text.strip() if onde_assistir else "Local de exibição não encontrado"

    critica = html.find("div", attrs={"class": "editorial-content cf"})
    critica_text = critica.text.strip() if critica else "Crítica não encontrada"

    classificacao = html.find("div", attrs={"class": "certificate"})
    classificacao_text = classificacao.text.strip() if classificacao else "Classificação indicativa não encontrada"

    nacionalidade = html.find("div", attrs={"class": "item"})
    nacionalidade_text = nacionalidade.text.strip() if nacionalidade else "Nacionalidade não encontrada"
    create_filme(titulo_text, sinopse, elenco_text, direcao_text, avaliacao_text, onde_assistir_text, critica_text, classificacao_text, nacionalidade_text)
  elif command == "4":
    id = input("Qual o id do filme? (Digite 0 para voltar)")
    if id == 0:
      exit()
    else:  
      update_filme(id)
  elif command == "5":
    id = int(input("Qual o id do filme? "))
    delete_filme(id)
  elif command == "6":
    titulo = input("Qual o titulo do filme que quer procurar? ")
    acessa_api(titulo)
  elif command == "7":
    salvar_json_local()
  elif command == "8":
    print("\nPrograma Encerrado")
    break
  else:
    print("\nComando Inválido")