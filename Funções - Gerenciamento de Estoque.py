import sqlite3

class Produto:
    def __init__(self, id, nome, categoria, quantidade):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade

class Estoque:
    def __init__(self):
        self.produtos = []
        self.conectar_banco()

    def conectar_banco(self):
        self.conn = sqlite3.connect('estoque.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def cadastrar_produto(self, id, nome, categoria, quantidade):
        novo_produto = Produto(id, nome, categoria, quantidade)
        self.produtos.append(novo_produto)
        self.cursor.execute('''
            INSERT INTO produtos (id, nome, categoria, quantidade) VALUES (?, ?, ?, ?)
        ''', (id, nome, categoria, quantidade))
        self.conn.commit()
        print(f'Produto {nome} cadastrado com sucesso!')

    def consultar_produto(self, id):
        self.cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        produto = self.cursor.fetchone()
        if produto:
            return {'id': produto[0], 'nome': produto[1], 'categoria': produto[2], 'quantidade': produto[3]}
        return "Produto não encontrado."

    def registrar_movimentacao(self, id, quantidade):
        self.cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        produto = self.cursor.fetchone()
        if produto:
            nova_quantidade = produto[3] + quantidade
            self.cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, id))
            self.conn.commit()
            acao = "entrada" if quantidade > 0 else "saída"
            print(f'Registrada {acao} de {abs(quantidade)} unidades do produto {produto[1]}.')
            return
        print("Produto não encontrado.")

    def gerar_relatorio(self):
        self.cursor.execute('SELECT * FROM produtos')
        produtos = self.cursor.fetchall()
        print("Relatório de Produtos:")
        for produto in produtos:
            print(f'ID: {produto[0]}, Nome: {produto[1]}, Categoria: {produto[2]}, Quantidade: {produto[3]}')

    def fechar_banco(self):
        self.conn.close()

# Função principal para interação com o usuário
def main():
    estoque = Estoque()

    while True:
        print("\nMenu:")
        print("1. Cadastrar produto")
        print("2. Consultar produto")
        print("3. Registrar movimentação")
        print("4. Gerar relatório")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            id = int(input("ID do produto: "))
            nome = input("Nome do produto: ")
            categoria = input("Categoria do produto: ")
            quantidade = int(input("Quantidade inicial: "))
            estoque.cadastrar_produto(id, nome, categoria, quantidade)

        elif opcao == '2':
            id = int(input("ID do produto: "))
            print(estoque.consultar_produto(id))

        elif opcao == '3':
            id = int(input("ID do produto: "))
            quantidade = int(input("Quantidade a adicionar (positivo) ou retirar (negativo): "))
            estoque.registrar_movimentacao(id, quantidade)

        elif opcao == '4':
            estoque.gerar_relatorio()

        elif opcao == '5':
            estoque.fechar_banco()
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
