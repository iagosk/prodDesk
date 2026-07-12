import flet as ft


# === 1. NOSSA CLASSE TABELA HASH (A LÓGICA) ===
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


# === 2. A INTERFACE GRÁFICA ATUALIZADA (FLET v0.85+) ===
def main(page: ft.Page):
    page.title = "Gerenciador de Inventário (Hash Table)"
    page.window_width = 480
    page.window_height = 550
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    inventario = TabelaHashProdutos(tamanho=5)

    # Inputs
    txt_nome = ft.TextField(label="Nome do Produto", expand=True)
    txt_preco = ft.TextField(label="Preço (R$)", expand=True)
    txt_busca = ft.TextField(label="Digite o produto para buscar", expand=True)

    # Texto de Status corrigido para ft.Colors.GREY_500
    lbl_status = ft.Text(
        value="Aguardando ações...",
        size=14,
        italic=True,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER,
    )

    def salvar_clicado(e):
        nome = txt_nome.value.strip()
        preco_str = txt_preco.value.strip()

        if not nome or not preco_str:
            lbl_status.value = "Erro: Preencha todos os campos para salvar!"
            lbl_status.color = ft.Colors.RED_500
            page.update()
            return

        try:
            preco = float(preco_str)
            resultado = inventario.inserir(nome, preco)
            indice = inventario._funcao_hash(nome)

            txt_nome.value = ""
            txt_preco.value = ""

            lbl_status.value = f"Sucesso! '{nome}' foi {resultado}.\nAlocado na gaveta (Índice): {indice}"
            lbl_status.color = ft.Colors.GREEN_500
        except ValueError:
            lbl_status.value = "Erro: O preço deve ser um número válido!"
            lbl_status.color = ft.Colors.RED_500

        page.update()

    def buscar_clicado(e):
        nome = txt_busca.value.strip()

        if not nome:
            lbl_status.value = "Erro: Digite o nome de um produto para buscar!"
            lbl_status.color = ft.Colors.RED_500
            page.update()
            return

        preco = inventario.buscar(nome)
        indice = inventario._funcao_hash(nome)

        if preco is not None:
            lbl_status.value = f"Encontrado!\nPreço de '{nome}': R${preco:.2f}\nBuscado direto no índice: {indice}"
            lbl_status.color = ft.Colors.BLUE_500
        else:
            lbl_status.value = (
                f"Produto '{nome}' não encontrado (Índice verificado: {indice})."
            )
            lbl_status.color = ft.Colors.ORANGE_500

        page.update()

    page.add(
        ft.Text("Sistema de Inventário Hash", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Adicionar / Atualizar Produto", weight=ft.FontWeight.BOLD),
                    ft.Row([txt_nome, txt_preco]),
                    ft.ElevatedButton(
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
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Buscar Preço", weight=ft.FontWeight.BOLD),
                    ft.Row([txt_busca]),
                    ft.ElevatedButton(
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
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        lbl_status,
    )


if __name__ == "__main__":
    # Atualizado para o método correto da nova versão do Flet
    ft.run(main)
