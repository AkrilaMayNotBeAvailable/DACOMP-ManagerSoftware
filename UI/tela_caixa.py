import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import caixa_db as db
from utils.customWidgets import widget_prototype_product
from utils.sqliteAux import formatar_data_para_sqlite
from datetime import datetime

class TelaCaixa(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master, fg_color="#190028")
        self.master = master
        self.save_info = f'Ultima vez que o caixa foi aberto: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        self.data = formatar_data_para_sqlite(data)
        
        self.lista_produtos = []
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.top_commands = self.widgets_base_commands()
        self.available_products = self.widgets_available_products()
        self.after(100, lambda: db.carregar_dados_vendas_do_dia(self.lista_produtos, self.data))
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário

    # Criação da parte superior da tela de caixa:
    def widgets_base_commands(self):
        campos = {}

        campos['formulario'] = ctk.CTkFrame(self, fg_color="#220135")
        campos['formulario'].grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Criação dos botões de comando base:
        campos["visualizar_dia"] = ctk.CTkButton(campos['formulario'], text="Visualizar Estatísticas do Dia", command=lambda caixa=self.data: self.master.abrir_tela_estatisticas(caixa))
        campos["atualizar_itens"] = ctk.CTkButton(campos['formulario'], text="Atualizar Itens")
        campos["fechar_dia"] = ctk.CTkButton(campos['formulario'], text="Fechar Caixa")
        campos["btn_voltar"] = ctk.CTkButton(campos['formulario'], text="Voltar para Interface Base", command=self.voltar)
        campos["info_salvo"] = ctk.CTkLabel(campos['formulario'], text=self.save_info)

        # Setando as posições dos botões na grid
        campos["visualizar_dia"].grid(row=0, column=0, padx=5, pady=(10, 0), sticky="we")
        campos["atualizar_itens"].grid(row=0, column=1, padx=5, pady=(10, 0), sticky="we")
        campos["fechar_dia"].grid(row=0, column=2, padx=5, pady=(10, 0), sticky="we")
        campos["btn_voltar"].grid(row=0, column=3, padx=5, pady=(10, 0), sticky="we")
        campos["info_salvo"].grid(row=1, column=0, padx=5, pady=(10, 0), sticky="we")
        
        return campos
    
    def widgets_available_products(self):
        campos = {}

        campos['frame_scroller'] = ctk.CTkScrollableFrame(self, label_text="Produtos Disponíveis", fg_color="#220135", label_font=("Arial", 18, "bold"))
        campos['frame_scroller'].grid(row=1, column=0, padx=(10, 10), pady=10, sticky="nswe")
        # Tornar o frame_scroller expansível dentro da TelaCaixa
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Adiciona: configura colunas do frame_scroller
        campos['frame_scroller'].grid_columnconfigure(0, weight=1)
        campos['frame_scroller'].grid_columnconfigure(1, weight=1)

        # Cria produtos disponíveis:
        dados = self.load_database_tipos()
        produtos = self.load_database_produtos()
        #print(dados)

        filtro = []
        sem_estoque = set()

        produtos = sorted(produtos, key=lambda x: x[1], reverse=True)  # Ordena por estoque
        for item in produtos:
            if item[1] != 0:
                filtro.append(item) # Os primeiros da lista são os que tem estoque
            elif item[0] not in [i[0] for i in filtro] and item[1] == 0:
                sem_estoque.add(item) # Se não estiver na primeira lista, então não tem estoque
        
        prod = [item for item in dados if item[0] in [i[0] for i in filtro]]
        #dados += [item for item in dados if item[0] in [i[0] for i in sem_estoque]]
        # Adiciona os produtos sem estoque ao final da lista
        prod += [item for item in dados if item[0] in [i[0] for i in sem_estoque]]

        ids_sem_estoque = {i[0] for i in sem_estoque}

        #print("DADOS (tipos):", prod)
        #print("SEM ESTOQUE:", sem_estoque)
        #print("FILTRO (com estoque):", filtro)
        #print("IDs sem estoque:", ids_sem_estoque)
        for i, tipo in enumerate(prod):
            indice_coluna = i % 2
            indice_linha = i - indice_coluna
            lucro = db.get_valor_unit(tipo[0])
            if tipo[0] in ids_sem_estoque:
                campos[f'produto_{i}'] = widget_prototype_product(
                    frame= campos['frame_scroller'], 
                    label_txt= tipo[1], 
                    preco= tipo[2], 
                    base_row= indice_linha, 
                    col= indice_coluna,
                    tipo_id= tipo[0],
                    estoque='sem_estoque',
                    lucro= lucro
                )
            else:
                estoque_declarado = db.get_estoque(tipo[0])
                campos[f'produto_{i}'] = widget_prototype_product(
                    frame= campos['frame_scroller'], 
                    label_txt= tipo[1], 
                    preco= tipo[2], 
                    base_row= indice_linha, 
                    col= indice_coluna,
                    tipo_id= tipo[0],
                    qtd_estoque= estoque_declarado,
                    lucro= lucro
                )

            self.lista_produtos.append(campos[f'produto_{i}'])

        return campos

    def load_database_tipos(self):
        # Conecta ao banco de dados e busca os produtos disponíveis:
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos ORDER BY tipo ASC")
        produtos = cursor.fetchall()
        conn.close()

        return produtos
    
    def load_database_produtos(self):
        # Conecta ao banco de dados e busca os produtos disponíveis:
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id_tipo, estoque FROM produtos ORDER BY id_tipo ASC")
        produtos = cursor.fetchall()
        conn.close()

        return produtos

    def voltar(self):
        self.master.trocar_tela("compras")
