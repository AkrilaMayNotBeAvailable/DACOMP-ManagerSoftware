import customtkinter as ctk
from tkinter import messagebox
from database import caixa_db as db
from database.tipos_db import load_database_tipos
from database.produtos_db import load_database_produtos
from utils.customWidgets import widget_prototype_product
from utils.sqliteAux import formatar_data_para_sqlite
from datetime import datetime
import threading

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
        self.available_products = self.widgets_available_products()


        self.top_commands = self.widgets_base_commands()
        self.after(1000, lambda: db.carregar_dados_vendas_do_dia(self.lista_produtos, self.data))
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário

    # Criação da parte superior da tela de caixa:
    def widgets_base_commands(self):
        campos = {}

        campos['formulario'] = ctk.CTkFrame(self, fg_color="#220135")
        campos['formulario'].grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Criação dos botões de comando base:
        campos["visualizar_dia"] = ctk.CTkButton(campos['formulario'], text="Visualizar Estatísticas do Dia", command=lambda caixa=self.data: self.master.abrir_tela_estatisticas(caixa))
        campos["btn_voltar"] = ctk.CTkButton(campos['formulario'], text="Voltar para Interface Base", command=self.voltar)
        campos["info_salvo"] = ctk.CTkLabel(campos['formulario'], text=self.save_info)

        # Setando as posições dos botões na grid
        campos["visualizar_dia"].grid(row=0, column=0, padx=5, pady=(10, 0), sticky="we")
        campos["btn_voltar"].grid(row=0, column=1, padx=5, pady=(10, 0), sticky="we")
        campos["info_salvo"].grid(row=1, column=0, padx=5, pady=(10, 0), sticky="we")

        self.categoria_var = ctk.StringVar(value="Todos")

        campos['frame_categorias'] = ctk.CTkFrame(campos['formulario'])
        campos['frame_categorias'].grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="we")

        categorias = ["Todos", "Bebidas", "Salgados", "Doces", "Acessórios", "Outros", "Caramelos do Vale"]

        for idx, cat in enumerate(categorias):
            rb = ctk.CTkRadioButton(
                campos['frame_categorias'],
                text=cat,
                variable=self.categoria_var,
                value=cat,
                command=self.filtrar_por_categoria
            )
            if not idx:
                rb.invoke()
            rb.grid(row=2, column=idx, padx=2, pady=(10, 0), sticky="w")

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

        return campos
    
    
    def filtrar_por_categoria(self):
        if not self.available_products or 'frame_scroller' not in self.available_products:
            print("Erro: frame_scroller não está disponível ainda.")
            return

        self.available_products['frame_scroller']._parent_canvas.yview_moveto(0)

        categoria = self.categoria_var.get()
        frame = self.available_products['frame_scroller']

        # Limpa a UI
        for widget in frame.winfo_children():
            widget.destroy()
        self.lista_produtos.clear()

        # Inicia thread para carregar dados
        threading.Thread(target=self.carregar_dados_em_thread, args=(categoria,), daemon=True).start()


    # Teste de Multithreading porque esse negócio tá lento pra caralho
    def carregar_dados_em_thread(self, categoria):
        from database.tipos_db import load_database_tipos

        dados = load_database_tipos(None if categoria == "Todos" else categoria)

        # Carrega dados auxiliares em lote (ideal se você tiver funções para isso)
        estoques = {tipo[0]: db.get_estoque(tipo[0]) for tipo in dados}
        lucros = {tipo[0]: db.get_valor_unit(tipo[0]) for tipo in dados}

        # Atualiza a UI na thread principal
        frame = self.available_products['frame_scroller']
        self.after(10, lambda: self.criar_widgets_em_lotes(dados, frame, estoques, lucros))

    # Criação assincrona utilizando lotes e after();
    def criar_widgets_em_lotes(self, dados, frame, estoques, lucros, i=0, batch_size=9):
        dados.sort(key=lambda x: x[1])  # Ordena por nome do produto
        if i >= len(dados):
            return

        for j in range(i, min(i + batch_size, len(dados))):
            tipo = dados[j]
            indice_coluna = j % 2
            indice_linha = j - indice_coluna

            estoque_declarado = estoques.get(tipo[0], 0)
            lucro = lucros.get(tipo[0], 0.0)

            widget = widget_prototype_product(
                frame=frame,
                label_txt=tipo[1],
                preco=tipo[2],
                base_row=indice_linha,
                col=indice_coluna,
                tipo_id=tipo[0],
                qtd_estoque=estoque_declarado,
                lucro=lucro
            )

            frame.grid_rowconfigure(indice_linha, weight=1)
            self.lista_produtos.append(widget)

        self.after(100, lambda: self.criar_widgets_em_lotes(dados, frame, estoques, lucros, i + batch_size))



    def voltar(self):
        self.master.trocar_tela("compras")
