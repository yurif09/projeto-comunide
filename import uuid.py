import uuid

class Usuario:
    def __init__(self, id_usuario, nome, endereco, alimentos_contribuidos, alimentos_pendentes):
        self.id_usuario = id_usuario
        self.nome = nome
        self.endereco = endereco
        self.alimentos_contribuidos = alimentos_contribuidos  # Lista de objetos Alimento
        self.alimentos_pendentes = alimentos_pendentes  # Lista de strings com informações do alimento

    def __str__(self):
        contribuidos_kg = ', '.join(f"{alimento.nome} ({alimento.quantidade}kg)" for alimento in self.alimentos_contribuidos if alimento.quantidade_units == 'kg')
        contribuidos_l = ', '.join(f"{alimento.nome} ({alimento.quantidade}L)" for alimento in self.alimentos_contribuidos if alimento.quantidade_units == 'L')
        pendentes = ', '.join(pendente for pendente in self.alimentos_pendentes)
        return f"ID: {self.id_usuario}, Nome: {self.nome}, Endereço: {self.endereco}, Alimentos Contribuídos (Kg): {contribuidos_kg}, Alimentos Contribuídos (L): {contribuidos_l}, Alimentos Pendentes: {pendentes}"

class Alimento:
    def __init__(self, nome, quantidade, quantidade_units):
        self.nome = nome
        self.quantidade = quantidade
        self.quantidade_units = quantidade_units

    def __str__(self):
        return f"Nome: {self.nome}, Quantidade: {self.quantidade}{self.quantidade_units}"

usuarios = {}
alimentos = {}

def exibir_lista_contribuicoes():
    print("Lista de contribuidores:")
    for usuario in usuarios.values():
        print(usuario)

def deve_ser_litros(nome_alimento):
    """Verifica se o alimento deve ser tratado como litros com base no nome."""
    sucos_e_refrigerantes = [
        'suco', 'refrigerante', 'coca-cola', 'coca cola', 'fanta', 'bare', 'sprite',
        'pepsi', 'guaraná', 'schweppes', 'mountain dew', 'sukita', 'kuat', 'soda', 'guarana'
    ]
    nome_alimento_lower = nome_alimento.lower()
    return any(referencia in nome_alimento_lower for referencia in sucos_e_refrigerantes)

def converter_quantidade(nome_alimento):
    """Converte a quantidade para a unidade apropriada (kg ou L) com base no nome do alimento."""
    unidade = 'L' if deve_ser_litros(nome_alimento) else 'kg'
    return unidade

def adicionar_usuario():
    nome = input("Digite o nome do usuário: ")
    endereco = input("Digite o endereço do usuário: ")
    alimentos_contribuidos = []
    alimentos_pendentes = []
    id_usuario = str(uuid.uuid4())[:8]  # Gera um ID aleatório de 8 caracteres

    print("Você contribuiu com algum alimento?")
    print("1. SIM")
    print("2. NÃO")
    opcao = input("Digite a opção desejada: ")

    if opcao == '1':
        nome_alimento = input("Digite o nome do alimento: ")
        unidade = converter_quantidade(nome_alimento)
        while True:
            quantidade_alimento = input("Digite a quantidade do alimento: ")
            if quantidade_alimento.replace('.', '', 1).isdigit():  # Permite ponto decimal para valores flutuantes
                quantidade_alimento = float(quantidade_alimento)
                break
            else:
                print("Quantidade do alimento deve ser um número válido. Tente novamente.")

        alimento = Alimento(nome_alimento, quantidade_alimento, unidade)
        alimentos[nome_alimento] = alimento
        alimentos_contribuidos.append(alimento)
    else:
        print("Você não contribuiu com algum alimento. Você gostaria de doar algum alimento?")
        print("1. SIM")
        print("2. NÃO")
        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            nome_alimento = input("Digite o nome do alimento que você gostaria de doar: ")
            unidade = converter_quantidade(nome_alimento)
            while True:
                quantidade_alimento = input("Digite a quantidade do alimento que você gostaria de doar: ")
                if quantidade_alimento.replace('.', '', 1).isdigit():  # Permite ponto decimal para valores flutuantes
                    quantidade_alimento = float(quantidade_alimento)
                    break
                else:
                    print("Quantidade do alimento deve ser um número válido. Tente novamente.")

            alimentos_pendentes.append(f"{nome_alimento} - {quantidade_alimento}{unidade} (Pendente)")
            print(f"Alimento {nome_alimento} adicionado como pendente.")

    usuarios[id_usuario] = Usuario(id_usuario, nome, endereco, alimentos_contribuidos, alimentos_pendentes)
    print(f"Usuário {nome} adicionado com sucesso. Seu ID é {id_usuario}.")

    # Exibir lista de contribuições após o cadastro
    exibir_lista_ou_sair()

def exibir_lista_ou_sair():
    """Pergunta ao usuário se ele deseja ver a lista de contribuidores ou sair."""
    print("\nVocê gostaria de ver a lista de quem contribuiu?")
    print("1. SIM")
    print("2. NÃO")
    opcao = input("Digite a opção desejada: ")

    if opcao == '1':
        exibir_lista_contribuicoes()
    elif opcao == '2':
        print("Obrigado pela contribuição!")
    else:
        print("Opção inválida. Tente novamente.")

def login_usuario():
    id_usuario = input("Digite o ID do usuário: ")
    nome = input("Digite o nome do usuário: ")

    if id_usuario in usuarios and usuarios[id_usuario].nome == nome:
        print(f"Bem-vindo, {nome}! Seu ID é {id_usuario}.")
        while True:
            print("\nOpções:")
            print("1. Adicionar alimento")
            print("2. Sair")

            opcao = input("Digite a opção desejada: ")

            if opcao == '1':
                nome_alimento = input("Digite o nome do alimento: ")
                unidade = converter_quantidade(nome_alimento)
                while True:
                    quantidade_alimento = input("Digite a quantidade do alimento: ")
                    if quantidade_alimento.replace('.', '', 1).isdigit():  # Permite ponto decimal para valores flutuantes
                        quantidade_alimento = float(quantidade_alimento)
                        break
                    else:
                        print("Quantidade do alimento deve ser um número válido. Tente novamente.")

                alimento = Alimento(nome_alimento, quantidade_alimento, unidade)
                alimentos[nome_alimento] = alimento
                usuarios[id_usuario].alimentos_contribuidos.append(alimento)
                print(f"Alimento {nome_alimento} adicionado com sucesso.")

                # Pergunta se deseja ver a lista de contribuições após adicionar alimento
                exibir_lista_ou_sair()
            elif opcao == '2':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("Usuário não encontrado. Você será redirecionado para o cadastro.")
        adicionar_usuario()

def main():
    # Adicionando usuários e suas contribuições iniciais
    rebeca = Usuario(
        id_usuario=str(uuid.uuid4())[:8],
        nome="Rebeca Alencar",
        endereco="Rua A, 123, Bairro B, Cidade C",
        alimentos_contribuidos=[Alimento("Arroz", 5, 'kg')],
        alimentos_pendentes=[]
    )
    alexandre = Usuario(
        id_usuario=str(uuid.uuid4())[:8],
        nome="Alexandre Moraes",
        endereco="Avenida X, 456, Bairro Y, Cidade Z",
        alimentos_contribuidos=[Alimento("Óleo", 10, 'kg')],
        alimentos_pendentes=[]
    )
    fernanda = Usuario(
        id_usuario=str(uuid.uuid4())[:8],
        nome="Fernanda",
        endereco="Praça P, 789, Bairro Q, Cidade R",
        alimentos_contribuidos=[Alimento("Macarrão", 7, 'kg'), Alimento("Batata Inglesa", 4, 'kg')],
        alimentos_pendentes=[]
    )

    usuarios[rebeca.id_usuario] = rebeca
    usuarios[alexandre.id_usuario] = alexandre
    usuarios[fernanda.id_usuario] = fernanda

    while True:
        print("1. Cadastrar-se")
        print("2. Login")
        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            adicionar_usuario()
        elif opcao == '2':
            login_usuario()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()