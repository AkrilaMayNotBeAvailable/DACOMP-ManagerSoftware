import customtkinter as ctk
from tkinter import messagebox
from database import compras_db as db
from utils.customWidgets import criar_entradas
from utils.sqliteAux import formatar_data_para_sqlite, formatar_valor_para_sqlite
from datetime import date

class TelaCompras(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário
        self.grid_columnconfigure(1, weight=0)  # Lista lateral (tamanho fixo)

        purchases = ctk.CTkFrame(self)
        purchases.grid(row=0, column=0, padx=10, pady=10, sticky="ne")
        purchases.grid_rowconfigure(0, weight=1)
        purchases.grid_columnconfigure(0, weight=1)  # Formulário

        self.campos = self.inicializar_tela_de_compras(purchases)

        # Frame lateral com compras anteriores
        self.frame_compras = ctk.CTkScrollableFrame(self.campos['compras'], width=300, label_text="Compras Anteriores")
        self.frame_compras.grid(row=0, column=1, padx=(10, 20), pady=10, rowspan=20, sticky="ns")
        self.atualizar_lista_compras()

    def inicializar_tela_de_compras(self, frame):
        campos = {}

        # Cria o frame de compras
        campos['compras'] = ctk.CTkFrame(frame)
        campos['compras'].grid(row=0, column=0, padx=10, pady=5, sticky="nswe")

        campos['titulo'] = criar_entradas(
            frame=campos['compras'], label_txt="Informar uma nova compra", 
            base_row=0, col=0, 
            widget='title'
        )

        # Entrada para nome do local de compra
        campos['nome_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Nome do Estabelecimento",
            base_row=1, col=0,
            widget='entry',
            placeholder="Digite o nome"
        )
        # Entrada para data de encomenda
        campos['data_encomenda_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Data de Encomenda",
            base_row=3, col=0,
            widget='entry_autofill',
            placeholder=date.today().strftime("%d/%m/%y")
        )
        # Entrada para data de recebimento
        campos['data_recebimento_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Data de Recebimento",
            base_row=5, col=0,
            widget='entry_autofill', placeholder=date.today().strftime("%d/%m/%y")
        )
        # Entrada para valor da nota fiscal
        campos['valor_nota_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Valor da Nota Fiscal",
            base_row=7, col=0,
            widget='entry', placeholder="Ex: 12.50 ou ignore"
        )
        # Entrada para chave de acesso da nota fiscal - CAMPO OBRIGATÓRIO E ÚNICO
        campos['chave_acesso_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Chave de Acesso da Nota Fiscal",
            base_row=9, col=0,
            widget='entry', placeholder="4325 0345 5439 ..."
        )

        campos['submit'] = ctk.CTkButton(
            campos['compras'], text="Criar Compra", command=self.abrir_nova_compra
        )
        campos['abrir_caixa'] = ctk.CTkButton(
            campos['compras'], text="Abrir Caixa", command=self.abrir_novo_caixa
        )
        campos['abrir_tipos'] = ctk.CTkButton(
            campos['compras'], text="Abrir Tipos", command=self.abrir_tela_tipos
        )

        # Botões de ação:
        campos['submit'].grid(row=11, column=0, padx=5, pady=(15, 5), sticky="we")
        campos['abrir_caixa'].grid(row=13, column=0, padx=5, pady=5, sticky="we")
        campos['abrir_tipos'].grid(row=15, column=0, padx=5, pady=5, sticky="we")

        return campos

    def atualizar_lista_compras(self):
        compras = db.carregar_compras() # Lista
        # Limpa os botões antigos
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        for i, compra in enumerate(compras):
            nome, data, chave, valor = compra
            texto = f"{nome} - {data} - {chave}"
            botao = ctk.CTkButton(
                self.frame_compras, 
                text=texto, 
                command=lambda i=(nome, data, valor, chave): self.selecionar_compra(i),
                anchor="w",
                width=300
            )
            botao.pack(fill="x", padx=5, pady=5)

    def abrir_nova_compra(self):
        try:
            local = self.campos['nome_entry']['entry'].get() # Nome do local de compra
            if not local: # O maluco não preencheu o campo
                messagebox.showerror("Erro", "Nome do local de compra não pode ser vazio.")
                return

            encomenda_data = formatar_data_para_sqlite(self.campos['data_encomenda_entry']['entry'].get())
            if encomenda_data is None: # Não colocou a data ou não está no formato correto
                return
            
            recebimento_data = formatar_data_para_sqlite(self.campos['data_recebimento_entry']['entry'].get())
            if recebimento_data is None: # Não colocou a data ou não está no formato correto
                return

            valor = formatar_valor_para_sqlite(self.campos['valor_nota_entry']['entry'].get())
            if valor is None: # Não colocou o valor ou não está no formato correto
                messagebox.showerror("Erro", "Valor da nota fiscal inválido.")
                return

            chave = self.campos['chave_acesso_entry']['entry'].get() # Precisa ser informada e necessita ser única!
            if not chave: # Não colocou a chave no troço
                messagebox.showerror("Erro", "Chave de acesso da nota fiscal não pode ser vazia.")
                return
            #-------------------------------------------------------------------
            dados = ( local, encomenda_data, recebimento_data, valor, chave ) # Armazena os dados

            db.criar_compra(dados)
            self.atualizar_lista_compras()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a compra: {e}")
        except ValueError as ve:
            messagebox.showerror("Erro", f"Erro ao criar a compra: {ve}")

    def selecionar_compra(self, id_compra):
        self.master.abrir_tela_produtos(id_compra)

    def abrir_novo_caixa(self):
        self.master.abrir_tela_caixa()
        
    def abrir_tela_tipos(self):
        self.master.abrir_tela_tipos()
