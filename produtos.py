import flet as ft


# 1. Tabela Hash
class TabelaHashProdutos:
    def __init__(self, tamanho=5):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(self.tamanho)]

    def _funcao_hash(self, chave):
        return sum(ord(letra) for letra in chave) % self.tamanho

    def inserir(self, nome_produto, preco):
        indice = self._funcao_hash(nome_produto)
        gaveta = self.tabela[indice]

        for i, (chave, valor) in enumerate(gaveta):
            if chave == nome_produto:
                gaveta[i] = (nome_produto, preco)
                return "atualizado"

        gaveta.append((nome_produto, preco))
        return "inserido"

    def buscar(self, nome_produto):
        indice = self._funcao_hash(nome_produto)
        gaveta = self.tabela[indice]
        for chave, valor in gaveta:
            if chave == nome_produto:
                return valor
        return None

    def listar(self):
        """Retorna uma lista com todos os produtos cadastrados."""
        todos_produtos = []
        for gaveta in self.tabela:
            for chave, valor in gaveta:
                todos_produtos.append((chave, valor))
        return todos_produtos


# 2. INTERFACE GRÁFICA
def main(page: ft.Page):
    page.title = "Gerenciador de Estoque - ProdDesk"
    page.window_width = 480
    page.window_height = 700  # Mantido para caber a lista e o status confortavelmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    inventario = TabelaHashProdutos(tamanho=5)

    # Inputs
    txt_nome = ft.TextField(label="Nome do Produto", expand=True)
    txt_preco = ft.TextField(label="Preço (R$)", expand=True)
    txt_busca = ft.TextField(label="Digite o produto para buscar", expand=True)

    # Janela de Status Dinâmica (Container que suporta textos e blocos extras)
    lbl_status = ft.Container(
        content=ft.Column(spacing=10, tight=True),
        padding=12,
        border_radius=10,
        visible=False,  # Começa invisível até que ocorra uma ação
    )

    # Elemento visual para exibir a lista de estoque
    lista_produtos_view = ft.ListView(expand=True, spacing=5, height=130)

    # Função unificada para mostrar mensagens estilizadas
    def mostrar_mensagem(texto, cor_fundo, cor_texto, icone, bloco_extra=None):
        lbl_status.bgcolor = cor_fundo

        # Linha básica de status com ícone e texto descritivo
        elementos = [
            ft.Row(
                [
                    ft.Icon(icone, color=cor_texto),
                    ft.Text(texto, color=cor_texto, weight="medium", expand=True),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        ]

        # Se houver um bloco de produto (como no caso da busca), adicionamos ele aqui
        if bloco_extra:
            elementos.append(bloco_extra)

        lbl_status.content.controls = elementos
        lbl_status.visible = True
        page.update()

    # Função para atualizar a lista de produtos no estoque
    def atualizar_lista():
        lista_produtos_view.controls.clear()
        produtos = inventario.listar()

        if not produtos:
            lista_produtos_view.controls.append(
                ft.Text(
                    "Nenhum produto cadastrado.", italic=True, color=ft.Colors.GREY_500
                )
            )
        else:
            for nome, preco in produtos:
                lista_produtos_view.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.SHOPPING_BAG, color=ft.Colors.GREEN_400
                            ),
                            title=ft.Text(nome, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"R$ {preco:.2f}"),
                        ),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        border_radius=5,
                    )
                )
        page.update()

    def salvar_clicado(e):
        nome = txt_nome.value.strip()
        preco_str = txt_preco.value.strip()

        if not nome or not preco_str:
            mostrar_mensagem(
                texto="Erro: Preencha todos os campos para salvar!",
                cor_fundo=ft.Colors.RED_100,
                cor_texto=ft.Colors.RED_900,
                icone=ft.Icons.ERROR_OUTLINE,
            )
            return

        try:
            preco = float(preco_str)
            resultado = inventario.inserir(nome, preco)
            indice = inventario._funcao_hash(nome)

            txt_nome.value = ""
            txt_preco.value = ""

            msg_sucesso = f"Sucesso! '{nome}' foi {resultado}.\nAlocado na gaveta (Índice): {indice}"
            mostrar_mensagem(
                texto=msg_sucesso,
                cor_fundo=ft.Colors.GREEN_100,
                cor_texto=ft.Colors.GREEN_900,
                icone=ft.Icons.CHECK_CIRCLE_OUTLINE,
            )

            # Atualiza a lista visual após salvar com sucesso
            atualizar_lista()

        except ValueError:
            mostrar_mensagem(
                texto="Erro: O preço deve ser um número válido!",
                cor_fundo=ft.Colors.RED_100,
                cor_texto=ft.Colors.RED_900,
                icone=ft.Icons.ERROR_OUTLINE,
            )

    def buscar_clicado(e):
        nome = txt_busca.value.strip()

        if not nome:
            mostrar_mensagem(
                texto="Erro: Digite o nome de um produto para buscar!",
                cor_fundo=ft.Colors.RED_100,
                cor_texto=ft.Colors.RED_900,
                icone=ft.Icons.ERROR_OUTLINE,
            )
            return

        preco = inventario.buscar(nome)
        indice = inventario._funcao_hash(nome)

        if preco is not None:
            # Criamos o bloco visual do produto encontrado, idêntico ao do estoque
            bloco_busca = ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.FIND_IN_PAGE_ROUNDED, color=ft.Colors.BLUE_700
                    ),
                    title=ft.Text(
                        nome, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900
                    ),
                    subtitle=ft.Text(
                        f"R$ {preco:.2f} • Buscado no índice: {indice}",
                        color=ft.Colors.BLUE_800,
                    ),
                ),
                bgcolor=ft.Colors.SURFACE,
                border_radius=5,
            )

            mostrar_mensagem(
                texto="Produto Encontrado no Estoque!",
                cor_fundo=ft.Colors.BLUE_100,
                cor_texto=ft.Colors.BLUE_900,
                icone=ft.Icons.SEARCH,
                bloco_extra=bloco_busca,
            )
        else:
            mostrar_mensagem(
                texto=f"Produto '{nome}' não encontrado (Índice verificado: {indice}).",
                cor_fundo=ft.Colors.ORANGE_100,
                cor_texto=ft.Colors.ORANGE_900,
                icone=ft.Icons.WARNING_AMBER_ROUNDED,
            )

    # Adiciona o layout inicial na página
    page.add(
        ft.Text("Sistema de Estoque - ProdDesk", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        # Seção de Cadastro (Botão atualizado para ft.Button)
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Adicionar / Atualizar Produto", weight=ft.FontWeight.BOLD),
                    ft.Row([txt_nome, txt_preco]),
                    ft.Button(
                        "Salvar na Tabela",
                        on_click=salvar_clicado,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        width=400,
                    ),
                ]
            ),
            padding=15,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        # Seção de Busca (Botão atualizado para ft.Button)
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Preço", weight=ft.FontWeight.BOLD),
                    ft.Row([txt_busca]),
                    ft.Button(
                        "Buscar com Hash",
                        on_click=buscar_clicado,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        width=400,
                    ),
                ]
            ),
            padding=15,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
        ),
        # Seção: Lista de Itens Cadastrados
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Produtos no Estoque", weight=ft.FontWeight.BOLD),
                    lista_produtos_view,
                ]
            ),
            padding=15,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
        ),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        # Local dinâmico da janelinha de feedback/status (Sucesso, Alertas, Buscas)
        lbl_status,
    )

    # Inicializa a lista de produtos (mostrará "Nenhum produto cadastrado" no início)
    atualizar_lista()


if __name__ == "__main__":
    ft.run(main)
