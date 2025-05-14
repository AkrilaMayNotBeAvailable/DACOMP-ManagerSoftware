import customtkinter as ctk
from tkinter import messagebox
from database import compras_db as db
from database.caixa_db import buscar_caixa
from utils.customWidgets import criar_entradas
import utils.sqliteAux as sqliteAux
from datetime import date
from PIL import Image, ImageTk
import pywinstyles

class TelaCompras(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.info_labels = {}

        # Display image on a Label widget.
        display_height = self.master.winfo_screenheight()
        display_width = self.master.winfo_screenwidth()

        # -- Frescura
        #--------------------------------------------------------
        try:
            image = Image.open("bg.jpg") # Inserir caminho para imagem de fundo
            
            ctk_image = ctk.CTkImage(light_image=image,
            dark_image=image, 
            size=(display_width, display_height))

            # Cria a label com a imagem de fundo
            background_label = ctk.CTkLabel(self, image=ctk_image, text="")
            background_label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        except FileNotFoundError:
            # Não encontrou a imagem, configura a cor de fundo padrão.
            self.configure(fg_color="#000001")
        except Exception as e: # Qualquer outro erro, configura a cor de fundo padrão.
            print(f"Erro ao carregar a imagem de fundo: {e}")
            self.configure(fg_color="#000001")
        #--------------------------------------------------------
        # -- Fim da frescura

        # Expandir a tela inteira
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Coluna das compras
        self.grid_columnconfigure(1, weight=1)  # Coluna lateral (histórico/caixa)

        # Frame principal de compras
        purchases = ctk.CTkFrame(self, corner_radius=24, bg_color="#000001")
        purchases.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        purchases.grid_rowconfigure(0, weight=1)
        purchases.grid_columnconfigure(0, weight=1)
        purchases.grid_columnconfigure(1, weight=1)

        # Frame lateral de histórico/caixas
        caixas = ctk.CTkFrame(self, corner_radius=24, bg_color="#000001")
        caixas.grid(row=0, column=1, padx=10, pady=10, sticky="new")
        caixas.grid_rowconfigure(0, weight=1)
        caixas.grid_columnconfigure(0, weight=1)
        caixas.grid_columnconfigure(1, weight=1)
        pywinstyles.set_opacity(purchases, color="#000001")
        pywinstyles.set_opacity(caixas, color="#000001")


        self.campos = self.inicializar_tela_de_compras(purchases)
        self.inicializar_historico_caixa(caixas)

        # Frame lateral com compras anteriores
        self.frame_compras = ctk.CTkScrollableFrame(self.campos['compras'], label_text="Compras Anteriores", 
            fg_color="transparent", width=300)
        self.frame_compras.grid(row=0, column=1, padx=(10, 20), pady=10, rowspan=20, sticky="nsew")

        # Frame lateral com histórico de caixa
        self.frame_caixa = ctk.CTkScrollableFrame(self.campos['historico_caixa'], label_text="Histórico de Caixas",)
        self.frame_caixa.grid(row=0, column=1, padx=(10, 20), pady=10, rowspan=20, sticky="nsew")

        self.atualizar_lista_compras()
        self.atualizar_caixas()

    def inicializar_tela_de_compras(self, frame):
        campos = {}

        # Cria o frame de compras
        campos['compras'] = ctk.CTkFrame(frame, corner_radius=24, fg_color="transparent")
        campos['compras'].grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")
        campos['compras'].grid_columnconfigure(0, weight=1)
        campos['compras'].grid_columnconfigure(1, weight=1)

        campos['titulo'] = criar_entradas(
            frame=campos['compras'], label_txt="Informar uma nova compra", 
            base_row=0, col=0, widget='title'
        )

        campos['nome_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Nome do Estabelecimento",
            base_row=1, col=0, widget='entry',
            placeholder="Digite o nome"
        )

        campos['data_encomenda_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Data de Encomenda",
            base_row=3, col=0, widget='entry_autofill',
            placeholder=date.today().strftime("%d/%m/%y")
        )

        campos['data_recebimento_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Data de Recebimento",
            base_row=5, col=0, widget='entry_autofill',
            placeholder=date.today().strftime("%d/%m/%y")
        )

        campos['valor_nota_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Valor da Nota Fiscal",
            base_row=7, col=0, widget='entry', placeholder="Ex: 12.50 ou ignore"
        )

        campos['chave_acesso_entry'] = criar_entradas(
            frame=campos['compras'], label_txt="Chave de Acesso da Nota Fiscal",
            base_row=9, col=0, widget='entry', placeholder="4325 0345 5439 ..."
        )

        campos['submit'] = ctk.CTkButton(
            campos['compras'], text="Criar Compra", command=self.abrir_nova_compra
        )
        campos['abrir_caixa'] = ctk.CTkButton(
            campos['compras'], text="Abrir Caixa", command=lambda caixa=date.today().strftime("%d/%m/%y"): self.abrir_novo_caixa(sqliteAux.formatar_data_para_sqlite(caixa))
        )
        campos['abrir_tipos'] = ctk.CTkButton(
            campos['compras'], text="Abrir Tipos", command=self.abrir_tela_tipos
        )

        campos['submit'].grid(row=11, column=0, padx=5, pady=(15, 5), sticky="we")
        campos['abrir_caixa'].grid(row=13, column=0, padx=5, pady=5, sticky="we")
        campos['abrir_tipos'].grid(row=15, column=0, padx=5, pady=5, sticky="we")

        return campos

    def inicializar_historico_caixa(self, frame):
        self.campos['historico_caixa'] = ctk.CTkFrame(frame, fg_color="transparent")
        self.campos['historico_caixa'].grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")
        self.campos['historico_caixa'].grid_columnconfigure(0, weight=1)
        self.campos['historico_caixa'].grid_columnconfigure(1, weight=1)

        self.campos['titulo_historico'] = criar_entradas(
            frame=self.campos['historico_caixa'], label_txt="Resumo do Caixa",
            base_row=0, col=0, widget='title'
        )

    def atualizar_caixas(self):
        caixas = set(buscar_caixa())
        caixas = sorted(caixas, reverse=True) # Ordena por data
        self.frame_caixa.grid_columnconfigure(0, weight=1)
        for i, caixa in enumerate(caixas):
            botao = ctk.CTkButton(
                self.frame_caixa, text=caixa, 
                command=lambda i=caixa: self.mostrar_resumo_caixa(i),
                anchor="w"
            )
            botao.grid(row=i+1, column=0, padx=20, pady=5, sticky="ew")

    def mostrar_resumo_caixa(self, data):
        resumo = sqliteAux.recuperar_informacoes_caixa(data)
        if self.info_labels is not None: # Se já mostra um resumo, destrói os labels antigos
            for label in self.info_labels.values():
                label.destroy()
        

        self.info_labels["data_caixa"] = ctk.CTkLabel(
            self.campos['historico_caixa'], 
            text=f"Data do Caixa:\n {data}", 
            width=200
        )
        self.info_labels["lucro"] = ctk.CTkLabel(
            self.campos['historico_caixa'], 
            text=f"Lucro líquido:\n R$ {resumo['lucro_liquido']:.2f}", 
            width=200
        )
        self.info_labels["vendidos"] = ctk.CTkLabel(
            self.campos['historico_caixa'], 
            text=f"Produto mais vendido:\n {resumo['vendidos'][0]} ({resumo['vendidos'][1]} vendas)", 
            width=200
        )
        self.info_labels["bruto"] = ctk.CTkLabel(
            self.campos['historico_caixa'], 
            text=f"Valor bruto:\n R$ {resumo['valor_bruto']:.2f}", 
            width=200
        )
        self.info_labels["editar_caixa"] = ctk.CTkButton(
            self.campos['historico_caixa'], 
            text="Editar Caixa", 
            command=lambda i=data: self.master.abrir_tela_caixa(i),
            width=200
        )

        # Adiciona os widgets na tela utilizando o sistema de grid
        #---------------------------------------------------------
        self.info_labels["data_caixa"].grid(row=1, column=0, padx=5, pady=5, sticky="nswe")
        self.info_labels["lucro"].grid(row=2, column=0, padx=5, pady=5, sticky="nswe")
        self.info_labels["vendidos"].grid(row=3, column=0, padx=5, pady=5, sticky="nswe")
        self.info_labels["bruto"].grid(row=4, column=0, padx=5, pady=5, sticky="nswe")
        self.info_labels["editar_caixa"].grid(row=5, column=0, padx=5, pady=5, sticky="nswe")

    def atualizar_lista_compras(self):
        compras = db.carregar_compras() # Lista
        # Limpa os botões antigos
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        for i, compra in enumerate(compras):
            nome, data, chave, valor = compra
            texto = f"{nome} - {data} - {chave}"
            botao = ctk.CTkButton(
                self.frame_compras, 
                text=texto, 
                command=lambda i=(nome, data, valor, chave): self.selecionar_compra(i),
                anchor="w",
                width=300
            )
            botao.pack(fill="x", padx=5, pady=5)

    def abrir_nova_compra(self):
        try:
            local = self.campos['nome_entry']['entry'].get() # Nome do local de compra
            if not local: # O maluco não preencheu o campo
                messagebox.showerror("Erro", "Nome do local de compra não pode ser vazio.")
                return

            encomenda_data = sqliteAux.formatar_data_para_sqlite(self.campos['data_encomenda_entry']['entry'].get())
            if encomenda_data is None: # Não colocou a data ou não está no formato correto
                return
            
            recebimento_data = sqliteAux.formatar_data_para_sqlite(self.campos['data_recebimento_entry']['entry'].get())
            if recebimento_data is None: # Não colocou a data ou não está no formato correto
                return

            valor = sqliteAux.formatar_valor_para_sqlite(self.campos['valor_nota_entry']['entry'].get())
            if valor is None: # Não colocou o valor ou não está no formato correto
                messagebox.showerror("Erro", "Valor da nota fiscal inválido.")
                return

            chave = self.campos['chave_acesso_entry']['entry'].get() # Precisa ser informada e necessita ser única!
            if not chave: # Não colocou a chave no troço
                messagebox.showerror("Erro", "Chave de acesso da nota fiscal não pode ser vazia.")
                return
            #-------------------------------------------------------------------
            dados = ( local, encomenda_data, recebimento_data, valor, chave ) # Armazena os dados

            db.criar_compra(dados)
            self.atualizar_lista_compras()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a compra: {e}")
        except ValueError as ve:
            messagebox.showerror("Erro", f"Erro ao criar a compra: {ve}")

    def selecionar_compra(self, id_compra):
        self.master.abrir_tela_produtos(id_compra)

    def abrir_novo_caixa(self, data):
        print(f"[CAIXA] Abrindo caixa para a data: {sqliteAux.formatar_data_para_sqlite(data)}")
        self.master.abrir_tela_caixa(data)
        
    def abrir_tela_tipos(self):
        self.master.abrir_tela_tipos()
