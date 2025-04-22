import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import random

# Auxiliar para criar entradas de texto:
''' @Brief
    Cria entradas de texto com label e placeholder.
        @param frame: Frame onde a entrada será criada.
        @param label_txt: Texto do label.
        @param placeholder: Texto de placeholder da entrada.
        @param base_row: Linha base para a entrada.
        @param col: Coluna onde a entrada será criada.
        @param mode: Modo de criação da entrada (1 ou 0).

    @return: A entrada criada.
'''
def criar_entradas(frame, label_txt, placeholder, base_row, col, mode=1):
    label = ctk.CTkLabel(frame, text=label_txt)
    label.grid(row=base_row, column=col, sticky="w", padx=5)
    entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
    if mode == 1:
        entry.insert(0, placeholder)
        entry.grid(row=base_row + 1, column=col, padx=0, pady=(0, 0), columnspan=2, sticky="we")
    else:
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=0, column=col, padx=5, pady=5, sticky="we")
    return entry

class TelaProdutos(ctk.CTkFrame):
    def __init__(self, master, id_compra):
        super().__init__(master)
        self.id_compra = id_compra[2]
        self.grid(row=0, column=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Expansão das partes internas
        self.grid_columnconfigure(0, weight=1)  # Formulário
        self.grid_columnconfigure(1, weight=0)  # Lista lateral (tamanho fixo)
        self.incremental_widget()

        self.btn_voltar = ctk.CTkButton(self, text="Voltar para Compras", command=self.voltar)
        self.btn_voltar.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.botao_atualizar = ctk.CTkButton(self, text="Atualizar Produtos", command=self.atualizar_produtos)
        self.botao_atualizar.grid(row=2, column=0, padx=5, pady=5)

        self.frame_compras = ctk.CTkScrollableFrame(self, width=300, label_text="Itens da Compra")
        self.frame_compras.grid(row=1, column=0, columnspan=5, pady=10, sticky="nswe")
        self.atualizar_lista_compras()

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()

    def incremental_widget(self):
        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        self.nome_entry = criar_entradas(self.frame_formulario, "Nome do Produto", "Digite o nome", 1, 0, 0)
        self.cod_barras_entry = criar_entradas(self.frame_formulario, "Código de Barras", "Ex: 1234567890123", 1, 1, 0)
        self.validade_entry = criar_entradas(self.frame_formulario, "Validade (YYYY-MM-DD)", "Ex: 2025-12-31", 1, 2, 0)
        self.valor_unit_entry = criar_entradas(self.frame_formulario, "Valor Unitário", "Ex: 12.50", 1, 3, 0)
        self.quantidade_entry = criar_entradas(self.frame_formulario, "Quantidade", "Ex: 10", 1, 4, 0)
        
        # Combobox de Tipo de Produto
        self.label_tipo = ctk.CTkLabel(self.frame_formulario, text="Tipo")
        self.label_tipo.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        self.combobox_tipo = ctk.CTkComboBox(self.frame_formulario, values=[])
        self.combobox_tipo.grid(row=0, column=5, padx=5, pady=5)

        self.carregar_tipos()  # Chama o método abaixo para popular a comb

        self.botao_salvar = ctk.CTkButton(self.frame_formulario, text="Salvar Produto", command=self.salvar_produto)
        self.botao_salvar.grid(row=0, column=6)

        self.nome_entry.grid(row=0, column=0, padx=5, pady=5)
        self.cod_barras_entry.grid(row=0, column=1, padx=5, pady=5)
        self.validade_entry.grid(row=0, column=2, padx=5, pady=5)
        self.valor_unit_entry.grid(row=0, column=3, padx=5, pady=5)
        self.quantidade_entry.grid(row=0, column=4, padx=5, pady=5)
        
    def recuperar_dados(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id_compra = ?", (self.id_compra,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    def atualizar_lista_compras(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo FROM tipos")
        tipos_disponiveis = cursor.fetchall()  # Lista de tuplas (id, tipo)
        conn.close()


        self.entries_produtos = []  # ← Adicionado para armazenar os dados editáveis
        # Limpa os botões antigos
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        dados = self.recuperar_dados()
        for i, dado in enumerate(dados):
            row_base = i * 2  # Espaço para label e entry

            id_tipo = dado[2]  # ID do tipo do produto
            tipo_nome = next((t[1] for t in tipos_disponiveis if t[0] == id_tipo), "Desconhecido")

            label_tipo = ctk.CTkLabel(self.frame_compras, text="Tipo")
            label_tipo.grid(row=row_base, column=14)

            combobox_tipo = ctk.CTkComboBox(self.frame_compras, values=[t[1] for t in tipos_disponiveis])
            combobox_tipo.set(tipo_nome)
            combobox_tipo.grid(row=row_base + 1, column=14)

            id_produto = dado[0]

            entry_nome = criar_entradas(self.frame_compras, "Produto", dado[5], row_base, 0)
            entry_valor_unit = criar_entradas(self.frame_compras, "Valor Unitário", str(dado[6]), row_base, 2)
            entry_cod_barras = criar_entradas(self.frame_compras, "Código de Barras", dado[4], row_base, 6)
            entry_validade = criar_entradas(self.frame_compras, "Validade", dado[3], row_base, 8)
            entry_quantidade = criar_entradas(self.frame_compras, "Quantidade", str(dado[7]), row_base, 10)
            entry_estoque = criar_entradas(self.frame_compras, "Estoque", str(dado[8]), row_base, 12)

            # Botão para remover produto
            botao_remover = ctk.CTkButton(self.frame_compras, text="Remover", command=lambda id_produto=id_produto: self.remover_produto(id_produto))
            botao_remover.grid(row=row_base + 1, column=16, padx=10, pady=(0,0), sticky="we")

            # Guarda os dados para atualização
            self.entries_produtos.append({
                "id": id_produto,
                "tipo": combobox_tipo,
                "nome": entry_nome,
                "valor_unit": entry_valor_unit,
                "cod_barras": entry_cod_barras,
                "validade": entry_validade,
                "quantidade": entry_quantidade,
                "estoque": entry_estoque,
            })
    def gerar_codigo_barras_unico(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        while True:
            codigo = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            cursor.execute("SELECT 1 FROM produtos WHERE cod_barras = ?", (codigo,))
            if not cursor.fetchone():
                conn.close()
                return codigo

    def carregar_tipos(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tipo FROM tipos ORDER BY tipo")
        tipos = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.combobox_tipo.configure(values=tipos)
        if tipos:
            self.combobox_tipo.set(tipos[0])  # valor padrão

    def salvar_produto(self):
        # Coloca valores padrão para itens não preenchidos
        validade = self.validade_entry.get() or "2023-01-01"
        cod_barras = self.cod_barras_entry.get() or self.gerar_codigo_barras_unico()
        nome = self.nome_entry.get()
        valor_unit = float(self.valor_unit_entry.get() or "0.00")

        tipo_nome = self.combobox_tipo.get()

        # Buscar o id do tipo
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tipos WHERE tipo = ?", (tipo_nome,))
        tipo_result = cursor.fetchone()
        if not tipo_result:
            messagebox.showerror("Erro", "Tipo de produto inválido.")
            return
        id_tipo = tipo_result[0]


        dados = (
            self.id_compra,
            id_tipo,
            validade,
            cod_barras,
            nome,
            valor_unit,
            int(self.quantidade_entry.get() or "0"),
            int(self.quantidade_entry.get() or "0")
        )


        try:
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (id_compra, id_tipo, validade, cod_barras, nome, valor_unit, quantidade, estoque)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
            self.atualizar_lista_compras()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de barras duplicado.")

    def atualizar_produtos(self):
        try:
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()

            for item in self.entries_produtos:
                id_prod = item["id"]
                nome = item["nome"].get()
                valor_unit = float(item["valor_unit"].get())
                cod_barras = item["cod_barras"].get()
                validade = item["validade"].get()
                quantidade = int(item["quantidade"].get())
                estoque = int(item["estoque"].get())

                tipo_nome = item["tipo"].get()

                cursor.execute("SELECT id FROM tipos WHERE tipo = ?", (tipo_nome,))
                tipo_result = cursor.fetchone()
                if not tipo_result:
                    messagebox.showerror("Erro", f"Tipo '{tipo_nome}' não encontrado.")
                    conn.close()
                    return
                id_tipo = tipo_result[0]

                cursor.execute("""
                    UPDATE produtos
                    SET nome = ?, valor_unit = ?, quantidade = ?, estoque = ?, cod_barras = ?, validade = ?, id_tipo = ?
                    WHERE id = ?
                """, (nome, valor_unit, quantidade, estoque, cod_barras, validade, id_tipo, id_prod))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produtos atualizados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produtos: {e}")

        
    def remover_produto(self, id_produto):
        try:
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()

            # Remove o produto da tabela 'produtos' usando o id
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
            conn.commit()
            conn.close()

            # Atualiza a lista de produtos após a remoção
            self.atualizar_lista_compras()

            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover produto: {e}")
