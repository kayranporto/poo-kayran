  """Lojinha com cadastro, venda e reposição de produtos."""


class Produto:
    """Representa um produto cujo preço e estoque não podem ser negativos."""

    def __init__(self, nome, preco, estoque=0):
        self.nome = str(nome).strip()
        self.__preco = 0
        self.__estoque = 0
        # Atribuir pelas properties garante validação já na criação do objeto.
        self.preco = preco
        self.estoque = estoque

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError) as erro:
            raise ValueError("O preço deve ser um número.") from erro

        if valor < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco = valor

    @property
    def estoque(self):
        return self.__estoque

    @estoque.setter
    def estoque(self, valor):
        if isinstance(valor, bool):
            raise ValueError("O estoque deve ser um número inteiro.")
        try:
            valor = int(valor)
        except (TypeError, ValueError) as erro:
            raise ValueError("O estoque deve ser um número inteiro.") from erro

        if valor < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self.__estoque = valor

    def exibir(self):
        """Exibe os dados do produto formatados para o catálogo."""
        print(f"{self.nome} | R$ {self.preco:.2f} | estoque: {self.estoque}")

    def repor(self, qtd):
        """Acrescenta uma quantidade positiva ao estoque."""
        if not _quantidade_positiva(qtd):
            print("Reposição recusada: a quantidade deve ser um inteiro positivo.")
            return False

        self.estoque += qtd
        print(f"Reposição realizada: {qtd} unidade(s) adicionada(s).")
        return True

    def vender(self, qtd):
        """Vende uma quantidade positiva caso haja estoque suficiente."""
        if not _quantidade_positiva(qtd):
            print("Venda recusada: a quantidade deve ser um inteiro positivo.")
            return False
        if qtd > self.estoque:
            print("Venda recusada: estoque insuficiente.")
            return False

        self.estoque -= qtd
        print(f"Venda realizada: {qtd} unidade(s) vendida(s).")
        return True


def _quantidade_positiva(qtd):
    return isinstance(qtd, int) and not isinstance(qtd, bool) and qtd > 0


def listar(catalogo):
    if not catalogo:
        print("O catálogo está vazio. Cadastre um produto primeiro.")
        return False

    print("\n--- Catálogo ---")
    for numero, produto in enumerate(catalogo, start=1):
        print(f"{numero}. ", end="")
        produto.exibir()
    return True


def escolher_produto(catalogo):
    """Lista e devolve um produto escolhido, ou None quando não houver escolha válida."""
    if not listar(catalogo):
        return None

    try:
        numero = int(input("Número do produto: "))
        return catalogo[numero - 1] if 1 <= numero <= len(catalogo) else None
    except ValueError:
        return None


def ler_quantidade():
    try:
        return int(input("Quantidade: "))
    except ValueError:
        print("Quantidade inválida: digite um número inteiro.")
        return None


def cadastrar_produto(catalogo):
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Cadastro recusado: o nome não pode ficar vazio.")
        return

    try:
        preco = float(input("Preço (use ponto, por exemplo 4.50): "))
        estoque = int(input("Estoque inicial: "))
        catalogo.append(Produto(nome, preco, estoque))
        print("Produto cadastrado com sucesso.")
    except ValueError as erro:
        print(f"Cadastro recusado: {erro}")


def menu():
    catalogo = []
    while True:
        print("\n=== LOJINHA ===")
        print("1 - Cadastrar produto")
        print("2 - Listar catálogo")
        print("3 - Vender produto")
        print("4 - Repor estoque")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(catalogo)
        elif opcao == "2":
            listar(catalogo)
        elif opcao in {"3", "4"}:
            produto = escolher_produto(catalogo)
            if produto is None:
                if catalogo:
                    print("Número de produto inválido.")
                continue
            qtd = ler_quantidade()
            if qtd is not None:
                if opcao == "3":
                    produto.vender(qtd)
                else:
                    produto.repor(qtd)
        elif opcao == "5":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Escolha um número de 1 a 5.")


if __name__ == "__main__":
    menu()
