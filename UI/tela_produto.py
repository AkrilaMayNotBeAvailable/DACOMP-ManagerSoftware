# ui/tela_produtos.py
import customtkinter as ctk
from tkinter import messagebox, IntVar
from utils.customWidgets import criar_entradas
from database import produtos_db as db
from database.tipos_db import recuperar_tipos

# TODO: Acessar os dados da COMPRA e poder alterar os dados nesta tela!
class TelaProdutos(ctk.CTkFrame):
    def __init__(self, master, id_compra):
        super().__init__(master)
        self.radio = IntVar(value=0)
        self.tipos = recuperar_tipos()
        self.id_compra = id_compra # Chave de acesso para a compra
        self.grid(row=0, column=0, sticky="nswe")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        titulo_tela = f'Editando produtos da compra no: {id_compra[0]}, feito na data: {id_compra[1]}'
        self.frame_title = ctk.CTkFrame(self)
        self.frame_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_columnconfigure(0, weight=1)
        self.titulo = criar_entradas(self.frame_title, titulo_tela, titulo_tela, 0, 0, widget='title')

        self.base_widgets_product()
        self.ordenador()
        self.frame_compras = ctk.CTkScrollableFrame(self, label_text="Itens da Compra", label_font=("Arial", 14, "bold"))
        self.frame_compras.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")
        self.atualizar_lista_compras()
        

    def base_widgets_product(self):
        tipos = [tipos[1] for tipos in self.tipos]
        
        self.frame_formulario = ctk.CTkFrame(self.frame_title)
        self.frame_formulario.grid(row=2, column=0, padx=10, pady=5, sticky="nswe")

        self.frame_form_compras = ctk.CTkFrame(self.frame_title)
        self.frame_form_compras.grid(row=1, column=0, padx=10, pady=5, sticky="nswe")

        #Dados da Compra:
        #------------------------------------------------
        self.nome_compra_entry = criar_entradas(self.frame_form_compras, "Nome do Estabelecimento", self.id_compra[0], 0, 0, widget='entry_autofill')
        self.data_encomenda_entry = criar_entradas(self.frame_form_compras, "Data de Entrega", self.id_compra[1], 0, 1, widget='entry_autofill')
        self.valor_total_entry = criar_entradas(self.frame_form_compras, "Valor Total", self.id_compra[2], 0, 3, widget='entry_autofill')
        
        # Interface de entrada de dados:
        #------------------------------------------------
        self.nome_entry = criar_entradas(self.frame_formulario, "Nome do Produto", "Digite o nome", 1, 0, widget='entry')
        self.cod_barras_entry = criar_entradas(self.frame_formulario, "Código de Barras", "Ex: 1234567890", 1, 1, widget='entry')
        self.validade_entry = criar_entradas(self.frame_formulario, "Validade", "2025-12-31", 1, 2, widget='entry')
        self.valor_unit_entry = criar_entradas(self.frame_formulario, "Valor Unitário", "0.00", 1, 3, widget='entry')
        self.quantidade_entry = criar_entradas(self.frame_formulario, "Quantidade", "0", 1, 4, widget='entry')
        self.combobox_tipo = criar_entradas(self.frame_formulario, "Tipo de Produto", tipos, 1, 5, widget='combobox')

        self.botao_salvar = ctk.CTkButton(self.frame_formulario, text="Salvar Produto", command=self.salvar_produto)
        self.btn_voltar = ctk.CTkButton(self.frame_formulario, text="Voltar para Compras", command=self.voltar)
        self.botao_atualizar = ctk.CTkButton(self.frame_formulario, text="Atualizar Produtos", command=self.atualizar_produtos)
        
        self.botao_salvar.grid(row=2, column=6, pady=5, padx=5)
        self.botao_atualizar.grid(row=3, column=1, pady=5, padx=5)
        self.btn_voltar.grid(row=3, column=0, pady=5, padx=5)
        
    def ordenador(self):
        self.ordenador_nome = ctk.CTkRadioButton(self.frame_formulario, text="Nome", variable=self.radio, value=1, command=self.atualizar_lista_compras)
        self.ordenador_preco = ctk.CTkRadioButton(self.frame_formulario, text="Valor", variable=self.radio, value=2, command=self.atualizar_lista_compras)
        self.ordenador_quantidade = ctk.CTkRadioButton(self.frame_formulario, text="Quantidade", variable=self.radio, value=3, command=self.atualizar_lista_compras)
        self.ordenador_tipo = ctk.CTkRadioButton(self.frame_formulario, text="Tipo", variable=self.radio, value=4, command=self.atualizar_lista_compras)

        self.ordenador_nome.grid(row=3, column=2, pady=5, padx=5)
        self.ordenador_preco.grid(row=3, column=3, pady=5, padx=5)
        self.ordenador_quantidade.grid(row=3, column=4, pady=5, padx=5)
        self.ordenador_tipo.grid(row=3, column=5, pady=5, padx=5)

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()

    def atualizar_lista_compras(self):
        self.entries_produtos = []
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        dados = db.recuperar_produtos_por_compra(self.id_compra[3], self.radio.get())
        tipos = self.tipos

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
        dados = (self.id_compra[3], id_tipo, validade, cod_barras, nome, valor_unit, quantidade, quantidade)

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
