import customtkinter as ctk
import sqlite3
from customWidgets import criar_entradas

class TelaTipos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configuração do layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        
        self.frame_title = ctk.CTkFrame(self)
        self.frame_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_columnconfigure(0, weight=1)
        self.titulo = criar_entradas(self.frame_title, "Tipos de Produtos", "Tipos de Produtos", 0, 0, widget='title')

        # Cria o scrollable frame uma vez
        self.frame_tipos = ctk.CTkScrollableFrame(self)
        self.frame_tipos.grid(row=3, column=0, columnspan=4, rowspan=3, sticky="nsew")
        self.frame_tipos.grid_rowconfigure(3, weight=1)
        self.frame_tipos.grid_columnconfigure(0, weight=1)

        # Criar entradas para adicionar tipos de produtos
        self.entry_tipo_produto = criar_entradas(
            frame=self,
            label_txt="Tipo de Produto:",
            placeholder="Digite o tipo de produto",
            base_row=1,
            col=0,
            widget='entry'
        )
        self.entry_tipo_valor = criar_entradas(
            frame=self,
            label_txt="Valor de Produto:",
            placeholder="Digite o valor de produto",
            base_row=1,
            col=1,
            widget='entry'
        )
        
        # Botão para salvar o tipo de produto
        btn_salvar = ctk.CTkButton(self, text="Salvar Tipo de Produto", command=self.salvar_tipo_produto)
        btn_salvar.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        btn_voltar = ctk.CTkButton(self, text="Voltar para Interface Base", command=self.voltar)
        btn_voltar.grid(row=2, column=3, padx=10, pady=10, sticky="e")
        
        # Lista para exibir os tipos de produtos cadastrados
        #self.lista_tipos = ctk.CTkTextbox(self, height=440)
        #self.lista_tipos.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.atualizar_tipos()
        
    def atualizar_tipos(self):
        try:
            # Conecta ao banco de dados
            with sqlite3.connect("sistema_compras.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, tipo, valor FROM tipos")
                tipos = cursor.fetchall()

            # Lista para guardar os widgets, se quiser usar depois (ex: para salvar alterações)
            self.entries_tipos = []

            #self.frame_tipos = ctk.CTkScrollableFrame(self)
            #self.frame_tipos.grid(row=3, column=0, padx=10, pady=10, sticky="nswe")
            #self.frame_tipos.grid_rowconfigure(3, weight=1)
            #self.frame_tipos.grid_columnconfigure(3, weight=1)

            # Limpa os widgets antigos da lista
            for widget in self.frame_tipos.winfo_children():
                widget.destroy()

            # Cria campos editáveis para cada tipo
            for i, (id_tipo, tipo_nome, valor) in enumerate(tipos):
                row_base = i * 2

                entrada_nome = criar_entradas(self.frame_tipos, "Tipo", tipo_nome, row_base, 0, widget='entry_autofill')
                entrada_valor = criar_entradas(self.frame_tipos, "Valor", str(valor), row_base, 2, widget='entry_autofill')

                # Guarda os widgets e o ID do tipo para futura atualização
                self.entries_tipos.append({
                    "id": id_tipo,
                    "nome": entrada_nome["entry"],
                    "valor": entrada_valor["entry"]
                })

        except sqlite3.Error as e:
            print(f"Erro ao carregar tipos de produtos: {e}")

    def salvar_tipo_produto(self):
        # Obtém o texto do campo de entrada
        tipo_produto = self.entry_tipo_produto['entry'].get()
        tipo_valor = self.entry_tipo_valor['entry'].get()
        
        if tipo_produto.strip():
            if not tipo_valor.strip():
                tipo_valor = 0.0
            try:
                with sqlite3.connect("sistema_compras.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO tipos (tipo, valor) VALUES (?, ?)", (tipo_produto, tipo_valor))
                    conn.commit()
                self.atualizar_tipos()
            except sqlite3.IntegrityError:
                print("O tipo de produto já existe no banco de dados.")
        else:
            print("O campo de tipo de produto está vazio.")

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()