from database.setup_db import inicializar_banco
import psutil
import os

inicializar_banco()

import customtkinter as ctk

from UI.tela_caixa import TelaCaixa
from UI.tela_produto import TelaProdutos
from UI.tela_tipos import TelaTipos
from UI.tela_compras import TelaCompras
from UI.tela_estatisticas import TelaEstatisticas
from UI.tela_promos import TelaPromos

def uso_de_memoria_ram(pid):
    try:
        process = psutil.Process(pid)
        mem_info = process.memory_info()
        return mem_info.rss / (1024 * 1024)  # in MB
    except psutil.NoSuchProcess:
        return None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Compras")
        self.geometry("1200x600")

        self.pid = os.getpid()
        self.telas = {}         # Cache das telas
        self.argumentos = {}    # Argumentos usados para construir cada tela
        self.tela_atual = None

        # Configuração de grid para o layout ocupar toda a janela
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.abrir_tela_compras()

    def trocar_tela(self, nome_tela, *args):
        self.ram_usage = uso_de_memoria_ram(self.pid)
        print(f"Uso de RAM: {self.ram_usage:.2f} MB")
        #print(f"Trocar para a tela: {nome_tela}") # DEBUG
        #print(f"Argumentos: {args}") # DEBUG

        if "estatisticas" in self.telas: # Critical Update: Deve ser destruída para atualizar os dados.
            self.telas["estatisticas"].destroy()
            del self.telas["estatisticas"]
        if "caixa" in self.telas: # Critical Update: Deve ser destruída para atualizar os dados.
            self.telas["caixa"].destroy()
            del self.telas["caixa"]

        # Oculta a tela atual
        if self.tela_atual and self.tela_atual.winfo_exists():
            try:
                self.tela_atual.grid_remove()
            except Exception as e:
                print(f"Erro ao ocultar tela atual: {e}")

        argumentos_atuais = self.argumentos.get(nome_tela)
        argumentos_novos = args if args else ()

        # Se os argumentos mudaram, destrói a tela do cache
        if nome_tela in self.telas and argumentos_atuais != argumentos_novos:
            #print(f"Argumentos antigos: {argumentos_atuais} || Argumentos novos: {argumentos_novos}") # DEBUG
            #print(f"Recriando tela: {nome_tela}") # DEBUG
            self.telas[nome_tela].destroy()
            del self.telas[nome_tela]

        # Cria a tela se não existir no cache
        if nome_tela not in self.telas:
            if nome_tela == "compras":
                self.telas[nome_tela] = TelaCompras(self)
            elif nome_tela == "produtos":
                self.telas[nome_tela] = TelaProdutos(self, *args)
            elif nome_tela == "caixa":
                self.telas[nome_tela] = TelaCaixa(self, *args)
            elif nome_tela == "tipos":
                self.telas[nome_tela] = TelaTipos(self)
            elif nome_tela == "estatisticas":
                self.telas[nome_tela] = TelaEstatisticas(self, *args)
            elif nome_tela == "promos":
                self.telas[nome_tela] = TelaPromos(self)

            self.telas[nome_tela].grid(row=0, column=0, sticky="nsew")
            self.argumentos[nome_tela] = argumentos_novos  # Atualiza os argumentos

        else:
            self.telas[nome_tela].grid()

        self.tela_atual = self.telas[nome_tela]

    def abrir_tela_compras(self):
        self.trocar_tela("compras")

    def abrir_tela_produtos(self, id_compra):
        self.trocar_tela("produtos", id_compra)

    def abrir_tela_caixa(self, data):
        self.trocar_tela("caixa", data)

    def abrir_tela_tipos(self):
        self.trocar_tela("tipos")

    def abrir_tela_estatisticas(self, data):
        self.trocar_tela("estatisticas", data)

    def abrir_tela_promos(self):
        self.trocar_tela("promos")

if __name__ == "__main__":
    app = App()
    app.mainloop()