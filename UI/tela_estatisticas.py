import customtkinter as ctk
import sqlite3
from database.setup_db import conectar
from utils.customWidgets import criar_entradas

class TelaEstatisticas(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configuração do layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.frame_title = ctk.CTkFrame(self)
        self.frame_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_title.grid_rowconfigure(0, weight=1)
        self.frame_title.grid_columnconfigure(0, weight=1)
        self.titulo = criar_entradas(self.frame_title, f"Estatísticas de Vendas {data}", "Estatísticas de Vendas", 0, 0, widget='title')

        return_button = ctk.CTkButton(self, text="Voltar", command=self.voltar)
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
        total_vendas = self.recuperar_total_vendas()
        label_total_vendas = ctk.CTkLabel(campos['frame_scroller'], text=f"Valor BRUTO de vendas: R$ {total_vendas:.2f}")
        label_total_vendas.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Total de produtos vendidos
        #total_produtos = self.recuperar_total_produtos()
        #label_total_produtos = ctk.CTkLabel(campos['frame_scroller'], text=f"Total de produtos vendidos: {total_produtos}")
        #label_total_produtos.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Produto mais vendido
        mais_vendido = self.recuperar_mais_vendido()
        label_mais_vendido = ctk.CTkLabel(campos['frame_scroller'], text=f"Produto mais vendido: {mais_vendido[0]} ({mais_vendido[1]} vendas)")
        label_mais_vendido.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Lucro líquido do dia
        lucro_liquido = self.recuperar_lucro_liquido()
        label_lucro_liquido = ctk.CTkLabel(campos['frame_scroller'], text=f"Lucro líquido do dia: R$ {lucro_liquido:.2f}")
        label_lucro_liquido.grid(row=3, column=0, padx=10, pady=10, sticky="w")



        return campos
        

    def recuperar_total_vendas(self):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(valor_total) FROM vendas_tipos WHERE data_venda = DATE('now', '-03:00')")
            total_vendas = cursor.fetchone()[0]
            #total_vendas = sum([venda[0] for venda in total_vendas])
            return total_vendas if total_vendas else 0.0
        
    def recuperar_mais_vendido(self):
        with conectar() as conn:
            cursor = conn.cursor()
            query = """
                SELECT id_tipo, quantidade_pix, quantidade_dinheiro
                FROM vendas_tipos
                WHERE data_venda = DATE('now', '-03:00')
                ORDER BY quantidade_pix + quantidade_dinheiro DESC
                LIMIT 1
            """
            cursor.execute(query)
            mais_vendido = cursor.fetchone()
            if mais_vendido:
                id_tipo, quantidade_pix, quantidade_dinheiro = mais_vendido
                cursor.execute("SELECT tipo FROM tipos WHERE id = ?", (id_tipo,))
                tipo_produto = cursor.fetchone()[0]
                return tipo_produto, quantidade_pix + quantidade_dinheiro
            else:
                return None
            
    def recuperar_lucro_liquido(self):
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(lucro_liquido) FROM vendas_tipos WHERE data_venda = DATE('now', '-03:00')")
            lucro_liquido = cursor.fetchone()[0]
            return lucro_liquido if lucro_liquido else 0.0


    def voltar(self):
        self.destroy()
        self.master.abrir_tela_caixa()