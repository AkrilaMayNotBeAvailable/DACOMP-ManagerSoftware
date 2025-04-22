import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import produtos as db
from customWidgets import widget_prototype_product

class TelaCaixa(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.top_commands = self.widgets_base_commands()
        self.available_products = self.widgets_available_products()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário

    # Criação da parte superior da tela de caixa:
    def widgets_base_commands(self):
        campos = {}

        campos['formulario'] = ctk.CTkFrame(self)
        campos['formulario'].grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Criação dos botões de comando base:
        campos["visualizar_dia"] = ctk.CTkButton(campos['formulario'], text="Visualizar Estatísticas do Dia")
        campos["atualizar_itens"] = ctk.CTkButton(campos['formulario'], text="Atualizar Itens")
        campos["fechar_dia"] = ctk.CTkButton(campos['formulario'], text="Fechar Caixa")
        campos["btn_voltar"] = ctk.CTkButton(campos['formulario'], text="Voltar para Interface Base", command=self.voltar)

        # Setando as posições dos botões na grid
        campos["visualizar_dia"].grid(row=0, column=0, padx=5, pady=(10, 0), sticky="we")
        campos["atualizar_itens"].grid(row=0, column=1, padx=5, pady=(10, 0), sticky="we")
        campos["fechar_dia"].grid(row=0, column=2, padx=5, pady=(10, 0), sticky="we")
        campos["btn_voltar"].grid(row=0, column=3, padx=5, pady=(10, 0), sticky="we")
        
        return campos
    
    def widgets_available_products(self):
        campos = {}

        campos['frame_scroller'] = ctk.CTkScrollableFrame(self, width=400, label_text="Produtos Disponíveis")
        campos['frame_scroller'].grid(row=1, column=0, padx=(10, 20), pady=10, sticky="nswe")

        # Cria produtos disponíveis:
        dados = self.load_database_tipos()
        for i, tipo in enumerate(dados):
            indice_coluna = i % 2
            indice_linha = i - indice_coluna
            campos[f'produto_{i}'] = widget_prototype_product(
                campos['frame_scroller'], tipo[1], tipo[2], indice_linha, indice_coluna
            )

        return campos

    def load_database_tipos(self):
        # Conecta ao banco de dados e busca os produtos disponíveis:
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos")
        produtos = cursor.fetchall()
        conn.close()

        return produtos

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()