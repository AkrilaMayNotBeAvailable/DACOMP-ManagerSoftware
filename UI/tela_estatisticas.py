import customtkinter as ctk
from database import estatisticas_db as db
from utils.customWidgets import criar_entradas

class TelaEstatisticas(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.data = data
        
        # Configuração do layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.frame_title = ctk.CTkFrame(self)
        self.frame_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_columnconfigure(0, weight=1)
        self.titulo = criar_entradas(self.frame_title, f"Estatísticas de Vendas {self.data}", "Estatísticas de Vendas", 0, 0, widget='title')

        return_button = ctk.CTkButton(self, text="Voltar", command=lambda data=self.data: self.voltar(data))
        return_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.frame_dados = self.estatisticas_widgets()
        self.frame_dados['frame_scroller'].grid_rowconfigure(0, weight=1)
        self.frame_dados['frame_scroller'].grid_columnconfigure(0, weight=1)

    def estatisticas_widgets(self):
        campos = {}
        campos['frame_scroller'] = ctk.CTkScrollableFrame(self, label_text="Estatísticas de Vendas")
        campos['frame_scroller'].grid(row=1, column=0, columnspan=2, sticky="nswe")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ''' O que mostrar nas estatisticas:
            - Total de vendas do dia
            - Total de produtos vendidos
            - Produto mais vendido
            - Produto menos vendido
            - Total de vendas por categoria
        '''
        # Total de vendas do dia
        total_vendas = db.recuperar_total_vendas(self.data)
        if total_vendas is None:
            total_vendas = 0.0
        label_total_vendas = ctk.CTkLabel(campos['frame_scroller'], text=f"Valor BRUTO de vendas: R$ {total_vendas:.2f}")
        label_total_vendas.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Produto mais vendido
        mais_vendido = db.recuperar_mais_vendido(self.data)
        if mais_vendido is None:
            mais_vendido = ("Nenhum produto vendido", 0)
        else:
            mais_vendido = (mais_vendido[0], mais_vendido[1])
        label_mais_vendido = ctk.CTkLabel(campos['frame_scroller'], text=f"Produto mais vendido: {mais_vendido[0]} ({mais_vendido[1]} vendas)")
        label_mais_vendido.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Lucro líquido do dia
        lucro_liquido = db.recuperar_lucro_liquido(self.data)
        if lucro_liquido is None:
            lucro_liquido = 0.0
        label_lucro_liquido = ctk.CTkLabel(campos['frame_scroller'], text=f"Lucro líquido do dia: R$ {lucro_liquido:.2f}")
        label_lucro_liquido.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        return campos

    def voltar(self, data):
        #self.destroy()
        self.master.trocar_tela("caixa", data)