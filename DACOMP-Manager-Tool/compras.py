import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import conectar
from datetime import date

class TelaCompras(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        # Expansão total dentro do App
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Expansão das partes internas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário
        self.grid_columnconfigure(1, weight=0)  # Lista lateral (tamanho fixo)
        conectar()

        self.campos = self.criar_widgets()

        # Frame lateral com compras anteriores
        self.frame_compras = ctk.CTkScrollableFrame(self, width=300, label_text="Compras Anteriores")
        self.frame_compras.grid(row=0, column=1, padx=(10, 20), pady=10, sticky="ns")

        self.carregar_compras()
        self.atualizar_lista_compras()


    def criar_widgets(self):
        campos = {}

        def criar(frame, label_txt, placeholder, row, col):
            label = ctk.CTkLabel(frame, text=label_txt)
            label.grid(row=row*2, column=col, sticky="w", padx=5)
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entry.grid(row=row*2+1, column=col, padx=0, pady=(0, 10), sticky="we")
            return entry
        
        campos['formulario'] = ctk.CTkFrame(self)
        campos['formulario'].grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        campos['data_atual'] = ctk.CTkLabel(campos['formulario'], text=f'Hoje é dia: {date.today().strftime("%d/%m/%y")}')
        campos['data_atual'].grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")

        campos['nome_entry'] = criar(campos['formulario'], "Nome do Estabelecimento de Compra", "Digite o nome", 1, 0)
        campos['data_encomenda_entry'] = criar(campos['formulario'], "Data de Encomenda", "Ex: 2025-12-01", 2, 0)
        campos['data_recebimento_entry'] = criar(campos['formulario'], "Data de Recebimento", "Ex: 2025-12-31", 3, 0)
        campos['valor_nota_entry'] = criar(campos['formulario'], "Valor da nota fiscal", "Ex: 12.50", 4, 0)
        campos['chave_acesso_entry'] = criar(campos['formulario'], "Chave de Acesso da Nota Fiscal", "4325 0345 5439 ...", 5, 0)

        campos['submit'] = ctk.CTkButton(campos['formulario'], text="Criar Compra", command=self.abrir_nova_compra)
        campos['submit'].grid(row=12, column=0, padx=5, pady=(10, 0), sticky="we")

        campos['abrir_caixa'] = ctk.CTkButton(campos['formulario'], text="Abrir Caixa", command=self.abrir_novo_caixa)
        campos['abrir_caixa'].grid(row=14, column=0, padx=5, pady=(10, 0), sticky="we")
        
        campos['abrir_tipos'] = ctk.CTkButton(campos['formulario'], text="Abrir Tipos", command=self.abrir_tela_tipos)
        campos['abrir_tipos'].grid(row=16, column=0, padx=5, pady=(10, 0), sticky="we")

        return campos

    def carregar_compras(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT local, data_encomenda, chave_nota FROM compras ORDER BY id DESC")
        self.compras = cursor.fetchall()
        conn.close()
        self.atualizar_lista_compras()

        return self.compras
    
    def atualizar_lista_compras(self):
        # Limpa os botões antigos
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        for i, compra in enumerate(self.compras):
            nome, data, chave = compra
            texto = f"{nome} - {data} - {chave}"
            botao = ctk.CTkButton(
                self.frame_compras, 
                text=texto, 
                command=lambda i=(nome, data, chave): self.selecionar_compra(i),
                anchor="w",
                width=250
            )
            botao.pack(fill="x", padx=5, pady=5)

    def abrir_nova_compra(self):
        try:
            local = self.campos.get('nome_entry').get()
            encomenda_data = self.campos.get('data_encomenda_entry').get() or "2000-01-01"
            recebimento_data = self.campos.get('data_recebimento_entry').get() or "2000-01-01"
            valor = float(self.campos.get('valor_nota_entry').get() or "0.00")
            chave = self.campos.get('chave_acesso_entry').get()

            dados = (
                local,
                encomenda_data,
                recebimento_data,
                valor,
                chave
            )

            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO compras (local, data_encomenda, data_recebimento, valor_total, chave_nota)
                VALUES (?, ?, ?, ?, ?)
            """, dados)
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Compra criada com sucesso.")
            self.carregar_compras()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a compra: {e}")

    def selecionar_compra(self, id_compra):
        self.master.abrir_tela_produtos(id_compra)
        messagebox.showinfo("Selecionado", f"Você selecionou a compra {id_compra[0]} - {id_compra[1]} - {id_compra[2]}")

    def abrir_novo_caixa(self):
        self.master.abrir_tela_caixa()
        #messagebox.showinfo("Selecionado", f"Você selecionou a compra {id_compra[0]} - {id_compra[1]} - {id_compra[2]}")
        
    def abrir_tela_tipos(self):
        self.master.abrir_tela_tipos()
        #messagebox.showinfo("Selecionado", f"Você selecionou a compra {id_compra[0]} - {id_compra[1]} - {id_compra[2]}")