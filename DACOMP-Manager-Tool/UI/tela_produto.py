# ui/tela_produtos.py
import customtkinter as ctk
from tkinter import messagebox
from customWidgets import criar_entradas
from database import produtos as db

class TelaProdutos(ctk.CTkFrame):
    def __init__(self, master, id_compra):
        super().__init__(master)
        self.id_compra = id_compra[2]
        self.grid(row=0, column=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.base_widgets_product()

        self.btn_voltar = ctk.CTkButton(self, text="Voltar para Compras", command=self.voltar)
        self.btn_voltar.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.botao_atualizar = ctk.CTkButton(self, text="Atualizar Produtos", command=self.atualizar_produtos)
        self.botao_atualizar.grid(row=2, column=0, padx=5, pady=5)

        self.frame_compras = ctk.CTkScrollableFrame(self, width=300, label_text="Itens da Compra", label_font=("Arial", 14, "bold"))
        self.frame_compras.grid(row=1, column=0, columnspan=5, pady=10, sticky="nswe")
        self.atualizar_lista_compras()

    def base_widgets_product(self):
        tipos = [t[1] for t in db.recuperar_tipos()]
        
        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        # Interface de entrada de dados:
        #------------------------------------------------
        self.nome_entry = criar_entradas(self.frame_formulario, "Nome do Produto", "Digite o nome", 0, 0, widget='entry')
        self.cod_barras_entry = criar_entradas(self.frame_formulario, "Código de Barras", "Ex: 1234567890123", 0, 1, widget='entry')
        self.validade_entry = criar_entradas(self.frame_formulario, "Validade", "2025-12-31", 0, 2, widget='entry')
        self.valor_unit_entry = criar_entradas(self.frame_formulario, "Valor Unitário", "0.00", 0, 3, widget='entry')
        self.quantidade_entry = criar_entradas(self.frame_formulario, "Quantidade", "0", 0, 4, widget='entry')
        self.combobox_tipo = criar_entradas(self.frame_formulario, "Tipo de Produto", tipos, 0, 5, widget='combobox')
        self.botao_salvar = ctk.CTkButton(self.frame_formulario, text="Salvar Produto", command=self.salvar_produto)
        self.botao_salvar.grid(row=1, column=7)

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()

    def atualizar_lista_compras(self):
        self.entries_produtos = []
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        dados = db.recuperar_produtos_por_compra(self.id_compra)
        tipos = db.recuperar_tipos()

        for i, dado in enumerate(dados):
            row = i * 2
            id_tipo = dado[2]
            id_produto = dado[0]
            tipo_nome = next((t[1] for t in tipos if t[0] == id_tipo), "Desconhecido")

            entry_nome = criar_entradas(self.frame_compras, "Produto", dado[5], row, 0, widget='entry_autofill')
            entry_valor_unit = criar_entradas(self.frame_compras, "Valor Unitário", str(dado[6]), row, 2, widget='entry_autofill')
            entry_cod_barras = criar_entradas(self.frame_compras, "Código de Barras", dado[4], row, 6, widget='entry_autofill')
            entry_validade = criar_entradas(self.frame_compras, "Validade", dado[3], row, 8, widget='entry_autofill')
            entry_quantidade = criar_entradas(self.frame_compras, "Quantidade", str(dado[7]), row, 10, widget='entry_autofill')
            entry_estoque = criar_entradas(self.frame_compras, "Estoque", str(dado[8]), row, 12, widget='entry_autofill')
            combobox_tipo = criar_entradas(self.frame_compras, "Tipo", [t[1] for t in tipos], row, 14, widget='combobox')
            combobox_tipo['combobox'].set(tipo_nome)

            botao_remover = ctk.CTkButton(self.frame_compras, text="Remover", command=lambda id_produto=id_produto: self.remover_produto(id_produto))
            botao_remover.grid(row=row + 1, column=16, padx=10, sticky="we")

            self.entries_produtos.append({
                "id": id_produto,
                "tipo": combobox_tipo['combobox'],
                "nome": entry_nome['entry'],
                "valor_unit": entry_valor_unit['entry'],
                "cod_barras": entry_cod_barras['entry'],
                "validade": entry_validade['entry'],
                "quantidade": entry_quantidade['entry'],
                "estoque": entry_estoque['entry'],
            })

    def salvar_produto(self):
        validade = self.validade_entry['entry'].get() or "2023-01-01"
        cod_barras = self.cod_barras_entry['entry'].get() or db.gerar_codigo_barras_unico()
        nome = self.nome_entry['entry'].get()
        valor_unit = float(self.valor_unit_entry['entry'].get() or "0.00")
        quantidade = int(self.quantidade_entry['entry'].get() or "0")
        tipo_nome = self.combobox_tipo['combobox'].get()

        tipo_result = db.buscar_id_tipo_por_nome(tipo_nome)
        if not tipo_result:
            messagebox.showerror("Erro", "Tipo de produto inválido.")
            return

        id_tipo = tipo_result[0]
        dados = (self.id_compra, id_tipo, validade, cod_barras, nome, valor_unit, quantidade, quantidade)

        try:
            db.inserir_produto(dados)
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
            self.atualizar_lista_compras()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_produtos(self):
        try:
            for item in self.entries_produtos:
                id_prod = item["id"]
                nome = item["nome"].get()
                valor_unit = float(item["valor_unit"].get())
                cod_barras = item["cod_barras"].get()
                validade = item["validade"].get()
                quantidade = int(item["quantidade"].get())
                estoque = int(item["estoque"].get())
                tipo_nome = item["tipo"].get()

                tipo_result = db.buscar_id_tipo_por_nome(tipo_nome)
                if not tipo_result:
                    messagebox.showerror("Erro", f"Tipo '{tipo_nome}' não encontrado.")
                    return
                id_tipo = tipo_result[0]
                dados = (nome, valor_unit, quantidade, estoque, cod_barras, validade, id_tipo)
                db.atualizar_produto(id_prod, dados)

            messagebox.showinfo("Sucesso", "Produtos atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_produto(self, id_produto):
        try:
            db.remover_produto(id_produto)
            self.atualizar_lista_compras()
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
