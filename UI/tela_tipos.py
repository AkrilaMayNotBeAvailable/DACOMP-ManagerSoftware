import customtkinter as ctk
import sqlite3
from database import tipos_db as db
from utils.customWidgets import criar_entradas, sorting_widget
from utils import sqliteAux
from tkinter import messagebox

class TelaTipos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.radio_controller = ctk.IntVar(value=0)
        
        # Configuração do layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Top Container permanece na linha 0
        self.top_container = ctk.CTkFrame(self)
        self.top_container.grid(row=0, column=0, columnspan=6, sticky="ew")
        self.top_container.grid_rowconfigure(0, weight=1)
        self.top_container.grid_columnconfigure(0, weight=1)


        self.frame_title = ctk.CTkFrame(self.top_container)
        self.frame_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_columnconfigure(0, weight=1)
        self.titulo = criar_entradas(self.frame_title, "Tipos de Produtos", "Tipos de Produtos", 0, 0, widget='title')

        # Layout da tela principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Scrollable frame agora vai para a linha 1
        self.frame_tipos = ctk.CTkScrollableFrame(self)
        self.frame_tipos.grid(row=1, column=0, rowspan=3, columnspan=6, sticky="nsew")
        self.frame_tipos.grid_rowconfigure(0, weight=1)
        self.frame_tipos.grid_columnconfigure(0, weight=1)


        # Criar entradas para adicionar tipos de produtos
        self.entry_tipo_produto = criar_entradas(
            frame=self.top_container,
            label_txt="Tipo de Produto:",
            placeholder="Digite o tipo de produto",
            base_row=1,
            col=0,
            widget='entry'
        )
        self.entry_tipo_categoria = criar_entradas(
            frame=self.top_container,
            label_txt="Categoria:",
            placeholder="Digite a categoria do produto",
            base_row=1,
            col=1,
            widget='entry'
        )
        self.entry_tipo_valor = criar_entradas(
            frame=self.top_container,
            label_txt="Valor de Produto:",
            placeholder="Digite o valor de produto",
            base_row=1,
            col=2,
            widget='entry'
        )
        
        # Botão para salvar o tipo de produto
        btn_salvar = ctk.CTkButton(self.top_container, text="Salvar Tipo de Produto", command=self.salvar_tipo_produto)
        btn_salvar.grid(row=2, column=3, padx=10, pady=10, sticky="e")

        btn_att = ctk.CTkButton(self.top_container, text="Atualizar Todos os Tipos", command=self.atualizar_todos_tipos)
        btn_att.grid(row=2, column=4, padx=10, pady=10, sticky="e")

        btn_voltar = ctk.CTkButton(self.top_container, text="Voltar para Interface Base", command=self.voltar)
        btn_voltar.grid(row=2, column=5, padx=10, pady=10, sticky="e")

        sorter = sorting_widget(
            row=3, 
            column=0, 
            frame=self.top_container, 
            controller = self.radio_controller, 
            on_change= lambda x = self.radio_controller : self.atualizar_tipos(x.get()),
            sort_screen="tipos"
        )

        i = 0
        for key, value in sorter.items():
            if key != "title":
                sorter[key].grid(row=3, column=i, sticky="ew")
            
            i += 1

        self.atualizar_tipos()

    def voltar(self):
        #self.destroy()
        self.master.trocar_tela("compras")


    ''' Database Related Functions:
        - Salvar tipo de produto()
        - Remover tipo de produto()
        - Atualizar tipo de produto()
    '''
    def salvar_tipo_produto(self):
        tipo_produto = self.entry_tipo_produto['entry'].get()
        tipo_categoria = self.entry_tipo_categoria['entry'].get()

        tipo_valor = sqliteAux.formatar_valor_para_sqlite(self.entry_tipo_valor['entry'].get())
        if tipo_valor is None:
            messagebox.showerror("Erro", "Valor de tipo inválido, por favor, modifique o campo valor.")
            return

        
        if tipo_produto.strip():
            try:
                print(f"Salvando tipo: {tipo_produto}, Categoria: {tipo_categoria}, Valor: {tipo_valor}")
                db.inserir_tipo_produto(tipo_produto, tipo_categoria, tipo_valor)
                self.atualizar_tipos()
            except sqlite3.IntegrityError:
                print("O tipo de produto já existe no banco de dados.")
        else:
            print("O campo de tipo de produto está vazio.")

    def remover_tipo(self, id_tipo):
        try:
            db.remover_tipo_produto(id_tipo)
            self.atualizar_tipos(self.radio_controller.get())
        except Exception as e:
            print(f"Erro ao remover tipo: {e}")

    def atualizar_tipo(self, id_tipo, tipo_nome, categoria, tipo_valor):
        try:
            db.atualizar_tipo_produto(id_tipo, tipo_nome, categoria, tipo_valor)
            self.atualizar_tipos(self.radio_controller.get())
        except sqlite3.Error as e:
            print(f"Erro ao atualizar tipo: {e}")
    
    def atualizar_todos_tipos(self):
        try:
            for entry in self.entries_tipos:
                id_tipo = entry["id"]
                nome = entry["nome"].get()
                categoria = entry["categoria"].get()
                valor = entry["valor"].get()

                dados = (nome, categoria, valor)
                db.atualizar_todos_tipos(id_tipo, dados)

            self.atualizar_tipos(self.radio_controller.get())
        except sqlite3.Error as e:
            print(f"Erro ao atualizar todos os tipos: {e}")

    def atualizar_tipos(self, x=None):
        try:
            self.entries_tipos = []
            # Limpa os widgets antigos da lista
            for widget in self.frame_tipos.winfo_children(): 
                widget.destroy()

            tipos = db.recover_types_by_ordering(self.radio_controller.get())
            print("Access")
            
            # Cria campos editáveis para cada tipo
            for i, (id_tipo, tipo_nome, valor, categoria) in enumerate(tipos):
                row_base = i * 2

                entrada_nome = criar_entradas(self.frame_tipos, "Tipo", tipo_nome, row_base, 0, widget='entry_autofill')
                entrada_categoria = criar_entradas(self.frame_tipos, "Categoria", categoria, row_base, 1, widget='entry_autofill')
                entrada_valor = criar_entradas(self.frame_tipos, "Valor", str(valor), row_base, 2, widget='entry_autofill')
                
                botao_atualizar = ctk.CTkButton(self.frame_tipos, text="Atualizar", command=lambda id_tipo=id_tipo, nome=entrada_nome["entry"], categoria=entrada_categoria["entry"], valor=entrada_valor["entry"]: self.atualizar_tipo(id_tipo, nome.get(), categoria.get(), valor.get()))
                botao_atualizar.grid(row=row_base+1, column=3)

                botao_remover = ctk.CTkButton(self.frame_tipos, text="Remover", command=lambda id_tipo=id_tipo: self.remover_tipo(id_tipo), fg_color="#960513", hover_color="#5e030c")
                botao_remover.grid(row=row_base+1, column=4, padx=20)

                # Guarda os widgets e o ID do tipo para futura atualização
                self.entries_tipos.append({
                    "id": id_tipo,
                    "nome": entrada_nome["entry"],
                    "categoria": entrada_categoria["entry"],
                    "valor": entrada_valor["entry"]
                })

        except sqlite3.Error as e:
            print(f"Erro ao carregar tipos de produtos: {e}")