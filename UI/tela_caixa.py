import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from database import caixa_db as db
from database.tipos_db import load_database_tipos
from utils.customWidgets import widget_prototype_product
from utils.sqliteAux import formatar_data_para_sqlite

'''
    Convenções:
        Variáveis:
            snake_case/lowercase
            para botões, usar o sufixo "_btn"

        Métodos:
            - layout_ = Layout de widgets
            - operational_ = Operações de banco de dados
            - linker_ = Linkar widgets entre si
            - quality_life_ = Melhorias de qualidade de vida
            - update_ = Atualizar dados na tela ou widget
'''

WIDGET_CONTAINER_KEY = "frame"
class TelaCaixa(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master, fg_color="#190028")
        self.master = master
        self.data = formatar_data_para_sqlite(data)
        self.save_info = f'Ultima vez que o caixa foi aberto: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        self.lista_produtos = []
        self.widgets_reciclados = []

        self.widgets_por_categoria = {}
        self.todos_widgets_cache = []


        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.available_products = self.layout_available_products()
        self.top_commands = self.layout_top_commands()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.update_carregar_dados_iniciais()

    # ---------- Layout ----------
    def layout_top_commands(self):
        campos = {}
        campos['formulario'] = ctk.CTkFrame(self, fg_color="#220135")
        campos['formulario'].grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        visualizar_btn = ctk.CTkButton(campos['formulario'], text="Visualizar Estatísticas do Dia", command=lambda: self.master.abrir_tela_estatisticas(self.data))
        voltar_btn = ctk.CTkButton(campos['formulario'], text="Voltar para Interface Base", command=self.voltar)
        info_label = ctk.CTkLabel(campos['formulario'], text=self.save_info)

        visualizar_btn.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="we")
        voltar_btn.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="we")
        info_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="we")

        self.categoria_var = ctk.StringVar(value="Todos")

        frame_categorias = ctk.CTkFrame(campos['formulario'])
        frame_categorias.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="we")

        categorias = ["Todos", "Bebidas", "Salgados", "Doces", "Acessórios", "Outros", "Caramelos do Vale"]
        self.cached_widgets = []

        for idx, cat in enumerate(categorias):
            rb = ctk.CTkRadioButton(frame_categorias, text=cat, variable=self.categoria_var, value=cat, command=self.update_filtrar_categoria)
            rb.grid(row=2, column=idx, padx=2, pady=(10, 0), sticky="w")
            if idx == 0:
                rb.invoke()

        return campos

    def layout_available_products(self):
        campos = {}
        campos['frame_scroller'] = ctk.CTkScrollableFrame(self, label_text="Produtos Disponíveis", fg_color="#220135", label_font=("Arial", 18, "bold"))
        campos['frame_scroller'].grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        campos['frame_scroller'].grid_columnconfigure(0, weight=1)
        campos['frame_scroller'].grid_columnconfigure(1, weight=1)
        return campos

    # ---------- Operações ----------
    def operational_obter_dados_filtrados(self, categoria):
        dados = load_database_tipos(None if categoria == "Todos" else categoria)
        estoques = {tipo[0]: db.get_estoque(tipo[0]) for tipo in dados}
        lucros = {tipo[0]: db.get_valor_unit(tipo[0]) for tipo in dados}
        return dados, estoques, lucros

    # ---------- Atualizações ----------
    def update_filtrar_categoria(self):
        categoria = self.categoria_var.get()
        frame = self.available_products['frame_scroller']
        frame._parent_canvas.yview_moveto(0)

        self.quality_life_reciclar_widgets()

        dados, estoques, lucros = self.operational_obter_dados_filtrados(categoria)
        self.update_criar_widgets_produtos(dados, frame, estoques, lucros)


    def update_criar_widgets_produtos(self, dados, frame, estoques, lucros):
        dados.sort(key=lambda x: x[1])
        categoria = self.categoria_var.get()
        self.widgets_por_categoria.setdefault(categoria, [])
        k, j = 0, 0

        for i, tipo in enumerate(dados):
            tipo_id = tipo[0]
            row, col = divmod(len(self.todos_widgets_cache), 2)
            

            # Verifica se o widget já foi criado em alguma categoria (cache global)
            widget_existente = next((w for w in self.todos_widgets_cache if w['tipo_id'] == tipo_id), None)

            if widget_existente:
                widget = widget_existente
                print(widget['row'], widget['col'])  # DEBUG: Exibe a posição do widget existente
            else:
                row, col = divmod(len(self.todos_widgets_cache), 2)
                estoque = estoques.get(tipo_id, 0)
                lucro = lucros.get(tipo_id, 0.0)

                widget = widget_prototype_product(
                    frame=frame,
                    label_txt=tipo[1],
                    preco=tipo[2],
                    base_row=row,
                    col=col,
                    tipo_id=tipo_id,
                    qtd_estoque=estoque,
                    lucro=lucro
                )

                widget['row'] = row
                widget['col'] = col
                self.todos_widgets_cache.append(widget)

            # Exibe o widget
            widget[WIDGET_CONTAINER_KEY].grid(row=widget['row'], column=widget['col'], padx=10, pady=10, sticky="nsew")
            if categoria != "Todos":
                widget[WIDGET_CONTAINER_KEY].grid(row=k, column=j, padx=10, pady=10, sticky="nsew")
                j += 1
                if j > 1:
                    j = 0
                    k += 1
            self.widgets_por_categoria[categoria].append(widget)


    def update_carregar_dados_iniciais(self):
        db.carregar_dados_vendas_do_dia(self.lista_produtos, self.data)

    # ---------- Qualidade de Vida ----------
    def quality_life_reciclar_widgets(self):
        # Esconde todos os widgets visíveis
        for widgets in self.widgets_por_categoria.values():
            for widget in widgets:
                if isinstance(widget, dict) and WIDGET_CONTAINER_KEY in widget:
                    widget[WIDGET_CONTAINER_KEY].grid_forget()

    # ---------- Navegação ----------
    def voltar(self):
        self.master.trocar_tela("compras")
