from database.setup_db import inicializar_banco
inicializar_banco()

import customtkinter as ctk

from UI.tela_caixa import TelaCaixa
from UI.tela_produto import TelaProdutos
from UI.tela_tipos import TelaTipos
from UI.tela_compras import TelaCompras
from UI.tela_estatisticas import TelaEstatisticas

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Compras")
        self.geometry("1200x600")
        self.tela_atual = None
        self.abrir_tela_compras()

    # Tela de Compras:
    def abrir_tela_compras(self):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = TelaCompras(self)

    # Tela de Produtos:
    def abrir_tela_produtos(self, id_compra):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = TelaProdutos(self, id_compra)

    # Tela de Caixa:
    def abrir_tela_caixa(self):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = TelaCaixa(self)
        
    def abrir_tela_tipos(self):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = TelaTipos(self)

    def abrir_tela_estatisticas(self):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.tela_atual = TelaEstatisticas(self, "Hoje")

if __name__ == "__main__":
    app = App()
    app.mainloop()
