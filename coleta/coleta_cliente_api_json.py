import requests as req
from bs4 import BeautifulSoup
headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

#img 1
response1 = req.get("https://www.adorocinema.com/filmes/filme-1628/", headers=headers)
if response1.status_code == 200:
    parsed_html = BeautifulSoup(response1.text, "html.parser")
    img_chefao = parsed_html.find("img", attrs={
        "alt": " O Poderoso Chefão"
    })
    if img_chefao:
        response = req.get(img_chefao["src"])
        img_content = response.content
        with open("o_poderoso_chefao.jpeg", "wb") as arq:
            arq.write(img_content)
#img 2
response2 = req.get("https://www.adorocinema.com/filmes/filme-11736/", headers=headers)
if response2.status_code == 200:
    parsed_html2 = BeautifulSoup(response2.text, "html.parser")
    img_sonho = parsed_html2.find("img", attrs={
        "alt": " Um Sonho de Liberdade"
    })
    if img_sonho:
        response = req.get(img_sonho["src"])
        img_content = response.content
        with open("um_sonho_de_liberdade.jpeg", "wb") as arq:
            arq.write(img_content)

print("Filmes disponíveis:\n")
print("1 - O Poderoso Chefão")
print("2 - Um Sonho de Liberdade")
resposta = input("\nDigite o número do filme que deseja conhecer: ")
if resposta == "1":
  html = BeautifulSoup(response1.text, "html.parser")
if resposta == "2":
  html = BeautifulSoup(response2.text, "html.parser")
while True:
  print("---------------------------------")
  print("Comandos disponíveis:\n")
  print("1. Título do filme")
  print("2. Sinopse")
  print("3. Elenco")
  print("4. Direção")
  print("5. Nota")
  print("6. Onde assistir")
  print("7. Crítica")
  print("8. Classificação Indicativa")
  print("9. Nacionalidade")
  print("10. Encerrar programa")
  print("---------------------------------\n")
  command = input("\nDigite o número do comando desejado: ")
  titulo = html.find("div", attrs={"class": "titlebar-title titlebar-title-xl"})
  paragrafos = html.find_all("p")
  elenco = html.find("div", attrs={"class": "meta-body-item meta-body-actor" })
  direcao = html.find("div", attrs={"class": "meta-body-item meta-body-direction meta-body-oneline"})
  avaliacao = html.find("span", attrs={"class": "stareval-note"})
  onde_assistir = html.find("div", attrs={"class": "provider-tile-text"})
  critica = html.find("div", attrs={"class": "editorial-content cf"})
  classificacao = html.find("div", attrs={"class": "certificate"})
  nacionalidade = html.find("div", attrs={"class": "item"})
  curiosidade = html.find("div", attrs={"class": "trivia-news"})
  if command == "1":
    print(titulo.text)
  elif command == "2":
    print(paragrafos[1].text)
  elif command == "3":
    print(elenco.text)
  elif command == "4":
    print(direcao.text)
  elif command == "5":
    print("Nota: "+avaliacao.text)
  elif command == "6":
    print(onde_assistir.text)
  elif command == "7":
    print(critica.text)
  elif command == "8":
    print(classificacao.text)
  elif command == "9":
    print(nacionalidade.text)
  elif command == "10":
    print("\nPrograma Encerrado")
    break
  else:
    print("\nComando Inválido")

