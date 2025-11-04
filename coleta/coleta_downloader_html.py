import json
from datetime import datetime
from bs4 import BeautifulSoup 
import uuid
import requests

FILE_NAME = 'profissionais.json'
headers = {'Content-Type': 'application/json'}

class Profissional:
    def __init__(self, id, nome, data_de_nascimento, numero_CRM, nacionalidade, local_de_trabalho):
        self.id = id
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
        self.numero_CRM = numero_CRM
        self.nacionalidade = nacionalidade
        self.local_de_trabalho = local_de_trabalho
    
    def to_dict(self):
        return {
          'id': self.id,
          'nome': self.nome,
          'data_de_nascimento': self.data_de_nascimento.strftime('%Y-%m-%d'),
          'numero_CRM': self.numero_CRM,
          'nacionalidade': self.nacionalidade,
          'local_de_trabalho': self.local_de_trabalho
          }
    
    @staticmethod
    def from_dict(data):
        return Profissional(
            id=data['id'],
            nome=data['nome'],
            data_de_nascimento=data['data_de_nascimento'],
            numero_CRM=data['numero_CRM'],
            nacionalidade=data['nacionalidade'],
            local_de_trabalho=data['local_de_trabalho']
        )

class GerenciadorDeProfissionais:
    def __init__(self):
        self.profissionais = self.load_profissionais()
  
    def load_profissionais(self):
        with open(FILE_NAME, 'r') as file:
            profissionais = file.read()
            if profissionais:
                return [Profissional.from_dict(item) for item in json.loads(profissionais)]
            return []
  
    def save_profissionais(self):
        with open(FILE_NAME, 'w') as file:
            json.dump([p.to_dict() for p in self.profissionais], file, indent=4)
  
    def list_profissionais(self):
        if not self.profissionais:
            print("Nenhum profissional cadastrado.")
        else:
            print("\n-----Lista de profissionais da saúde:-----\n")
            for profissional in self.profissionais:
                print(f"\nID: {profissional.id}:\n")
                print(f"Nome: {profissional.nome}")
                print(f"Data de nascimento: {profissional.data_de_nascimento}")
                print(f"Número de CRM: {profissional.numero_CRM}")
                print(f"Nacionalidade: {profissional.nacionalidade}")
                print(f"Local de trabalho: {profissional.local_de_trabalho}")
        
  
    def get_profissional(self, profissional_id):
        for p in self.profissionais:
            if p.id == profissional_id:
                return p
        return None
        
    def add_profissional(self):
        profissional_id = input("Digite o ID: ")
        if self.get_profissional(profissional_id):
            print("Erro: ID já existe.")
            return
  
        nome = input("Digite o nome: ")
        data_de_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ")
        numero_CRM = input("Digite o número de CRM: ")
        nacionalidade = input("Digite a nacionalidade do profissional: ")
        local_de_trabalho = input("Digite o local de trabalho: ")
  
        try:
            datetime.strptime(data_de_nascimento, "%Y-%m-%d")
        except ValueError:
            print("Erro: Data inválida. Use o formato YYYY-MM-DD.")
            return
  
        try:
            numero_CRM = int(numero_CRM)
        except ValueError:
            print("Erro: Experiência deve ser um número.")
            return
    
        profissional = Profissional(
            id=profissional_id,
            nome=nome,
            data_de_nascimento=datetime.strptime(data_de_nascimento, "%Y-%m-%d"),
            numero_CRM=numero_CRM,
            nacionalidade=nacionalidade,
            local_de_trabalho=local_de_trabalho
        )
        self.profissionais.append(profissional)
        self.save_profissionais()
        print("Profissional adicionado com sucesso.")
  
    def update_profissional(self):
        profissional_id = input("Digite o ID do profissional a ser atualizado: ")
        profissional = self.get_profissional(profissional_id)
        if not profissional:
            print("Erro: ID inexistente.")
            return
    
        print("Deixe em branco para manter o valor atual.\n")
        nome = input(f"Nome ({profissional.nome}): ") or profissional.nome
        data_de_nascimento = input(
            f"Data de nascimento ({profissional.data_de_nascimento}): "
        ) or profissional.data_de_nascimento
        numero_CRM = input(
            f"Número de CRM ({profissional.numero_CRM}): ") or profissional.numero_CRM
        nacionalidade = input(
            f"Nacionalidade ({profissional.nacionalidade}): "
        ) or profissional.nacionalidade
        local_de_trabalho = input(
            f"Local de trabalho ({profissional.local_de_trabalho}): "
        ) or profissional.local_de_trabalho
  
        if data_de_nascimento:
            try:
                datetime.strptime(data_de_nascimento, "%Y-%m-%d")
            except ValueError:
                print("Erro: Data inválida. Use o formato YYYY-MM-DD.")
                return
  
        if numero_CRM:
            try:
                numero_CRM = int(numero_CRM)
            except ValueError:
                print("Erro: Número de CRM deve ser um número.")
                return
        
        profissional = Profissional(
            id=profissional_id,
            nome=nome,
            data_de_nascimento=datetime.strptime(data_de_nascimento, "%Y-%m-%d"),
            numero_CRM=numero_CRM,
            nacionalidade=nacionalidade,
            local_de_trabalho=local_de_trabalho
        )
        self.save_profissionais()
        print("Profissional atualizado com sucesso.")
    
    def delete_profissional(self):
        profissional_id = input("Digite o ID do profissional a ser deletado: ")
        profissional = self.get_profissional(profissional_id)
        if not profissional:
            print("Erro: ID inexistente.")
            return
  
        confirm = input(
            "Você tem certeza que deseja deletar o profissional"
            f"com ID {profissional_id}? (s/n): "
        )
        if confirm.lower() == 's':
            self.profissionais.remove(profissional)
            self.save_profissionais()
            print("Profissional deletado com sucesso.")
        else:
            print("Deleção cancelada.")

def main():
    crud = GerenciadorDeProfissionais()
    while True:
        print("---------------------------------")
        print("Comandos disponíveis:\n")
        print("1. Listar todos os profissionais da saúdes")
        print("2. Acessar os dados de um profissional da saúde específico")
        print("3. Registrar um novo profissional da saúde")
        print("4. Atualizar um profissional da saúde")
        print("5. Deletar um profissional da saúde")
        print("6. Pesquisar um profissional da saúde na Wiki")
        print("8. Sair do programa")
        print("---------------------------------\n")

        command = input("\nDigite o número do comando desejado: ")

        if command == '1':
            crud.list_profissionais()
        elif command == '2':
            profissional_id = input("Digite o ID do profissional da saúde: ")
            profissional = crud.get_profissional(profissional_id)
            if profissional:
                print(f"\nID do profissional: {profissional.id}:\n")
                print(f"Nome: {profissional.nome}")
                print(f"Data de nascimento: {profissional.data_de_nascimento}")
                print(f"Número de CRM: {profissional.numero_CRM}")
                print(f"Nascionalidade: {profissional.nacionalidade}")
                print(f"Local de trabalho: {profissional.local_de_trabalho}")
            else:
                print("\n-----Profissional da saúde não encontrado.\n-----")
        elif command == '3':
            crud.add_profissional()
        elif command == '4':
            crud.update_profissional()
        elif command == '5':
            crud.delete_profissional()

        elif command == '6':
            pesq = input("\nDigite o nome de um profissional da saúde: ")
            url = f"https://pt.wikipedia.org/wiki/{'_'.join(pesq.split(' '))}"
            response = requests.get(url, headers=headers)
            parsed_html = BeautifulSoup(response.text, 'html.parser')
            parag = parsed_html.find_all('p')[0].get_text()
            print("\n")
            print(parag)

        elif command == '8':
            print("\n-----Programa Encerrado-----\n")
            break
        else:
            print("\nComando inválido.\n")

if __name__ == "__main__":
  main()
