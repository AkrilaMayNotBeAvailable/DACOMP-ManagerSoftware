import customtkinter as ctk
import sqlite3

def criar_entradas(frame, label_txt, placeholder, base_row, col, mode=1):
    label = ctk.CTkLabel(frame, text=label_txt)
    label.grid(row=base_row, column=col, sticky="w", padx=5)
    entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
    if mode == 1:
        entry.grid(row=base_row + 1, column=col, padx=0, pady=(0, 10), columnspan=1, sticky="we")
    else:
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=0, column=col, padx=5, pady=5, sticky="we")
    return entry


class TelaTipos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Configuração do layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Título da tela
        titulo = ctk.CTkLabel(self, text="Tipos de Produtos", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, sticky="w")
        
        # Criar entradas para adicionar tipos de produtos
        self.entry_tipo_produto = criar_entradas(
            frame=self,
            label_txt="Tipo de Produto:",
            placeholder="Digite o tipo de produto",
            base_row=1,
            col=0,
        )
        self.entry_tipo_valor = criar_entradas(
            frame=self,
            label_txt="Valor de Produto:",
            placeholder="Digite o valor de produto",
            base_row=1,
            col=1,
        )
        
        # Botão para salvar o tipo de produto
        btn_salvar = ctk.CTkButton(self, text="Salvar Tipo de Produto", command=self.salvar_tipo_produto)
        btn_salvar.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        btn_voltar = ctk.CTkButton(self, text="Voltar para Interface Base", command=self.voltar)
        btn_voltar.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        
        # Lista para exibir os tipos de produtos cadastrados
        self.lista_tipos = ctk.CTkTextbox(self, height=440)
        self.lista_tipos.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.atualizar_tipos()
        
    def atualizar_tipos(self):
        try:
            # Conecta ao banco de dados
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()
            
            # Consulta os tipos de produtos no banco de dados
            cursor.execute("SELECT tipo, valor FROM tipos")
            tipos = cursor.fetchall()
            conn.close()
            
            # Limpa a lista exibida
            self.lista_tipos.delete("1.0", "end")
            
            # Adiciona os tipos de produtos na lista exibida
            for tipo, valor in tipos:
                self.lista_tipos.insert("end", f"{tipo}, {valor}\n")
        except sqlite3.Error as e:
            print(f"Erro ao carregar tipos de produtos: {e}")
        
    def salvar_tipo_produto(self):
        # Obtém o texto do campo de entrada
        tipo_produto = self.entry_tipo_produto.get()
        tipo_valor = self.entry_tipo_valor.get()
        
        if tipo_produto.strip():
            if not tipo_valor.strip():
                tipo_valor = 0.0
            try:
                # Conecta ao banco de dados
                conn = sqlite3.connect("sistema_compras.db")
                cursor = conn.cursor()
                
                # Insere o tipo de produto no banco de dados
                cursor.execute("INSERT INTO tipos (tipo, valor) VALUES (?, ?)", (tipo_produto, tipo_valor))
                conn.commit()
                conn.close()
                
                # Adiciona o tipo de produto na lista exibida
                self.lista_tipos.insert("end", f"{tipo_produto}, {tipo_valor}\n")
                self.entry_tipo_produto.delete(0, "end")
            except sqlite3.IntegrityError:
                print("O tipo de produto já existe no banco de dados.")
        else:
            print("O campo de tipo de produto está vazio.")

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()