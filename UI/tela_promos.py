import customtkinter as ctk
from tkinter import ttk, messagebox
from utils.customWidgets import criar_entradas
from utils.sqliteAux import formatar_valor_para_sqlite
import database.promo_db as promo_db

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


class TelaPromos(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.layout_widgets = {}
        self.products_in_promo = []
        self.tipos_dict = promo_db.recuperar_tipos_dict()  # Dicionário de tipos de produtos

        self.layout_base_frames()
        self.layout_tree_view()
        self.update_tree_view([])
        self.layout_promo_frame()
        self.linker_tree_view_promo_frame(self.layout_widgets['tree_view'])
        self.layout_widgets['tree_view'].bind("<<TreeviewSelect>>", self.linker_tree_view_promo_frame)


    def layout_base_frames(self):
        self.layout_widgets['container'] = ctk.CTkFrame(self) # Main
        self.layout_widgets['frame_titulo'] = ctk.CTkFrame(self.layout_widgets['container']) # Título
        self.layout_widgets['TreeView'] = ctk.CTkFrame(self.layout_widgets['container']) # TreeView
        self.layout_widgets['frame_produtos'] = ctk.CTkFrame(self.layout_widgets['container']) # Promochecker

        titulo = criar_entradas(self.layout_widgets['frame_titulo'], "Gerenciador de Promoções", base_row=0, col=0)
        retorno = ctk.CTkButton(self.layout_widgets['frame_titulo'], text="Voltar à tela inicial", command=lambda : self.voltar())  # Voltar para a tela anterior
        retorno.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.layout_widgets['container'].grid(row=0, column=0, sticky="nsew")
        self.layout_widgets['container'].grid_rowconfigure(0, weight=0)
        self.layout_widgets['container'].grid_rowconfigure(1, weight=1)
        self.layout_widgets['container'].grid_columnconfigure(0, weight=1)
        self.layout_widgets['container'].grid_columnconfigure(1, weight=1)

        self.layout_widgets['frame_titulo'].grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        self.layout_widgets['TreeView'].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.layout_widgets['TreeView'].grid_rowconfigure(0, weight=1)
        self.layout_widgets['TreeView'].grid_columnconfigure(0, weight=1)

        self.layout_widgets['frame_produtos'].grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.layout_widgets['frame_produtos'].grid_columnconfigure(0, weight=1)

    def layout_tree_view(self):
        self.quality_life_ttk_styles()
        self.layout_widgets['tree_view'] = ttk.Treeview(self.layout_widgets['TreeView'], columns=("ID", "Nome", "Valor"), show="headings")
        self.layout_widgets['tree_view'].heading("ID", text="ID")
        self.layout_widgets['tree_view'].heading("Nome", text="Nome")
        self.layout_widgets['tree_view'].heading("Valor", text="Valor de Venda (R$)")
        self.layout_widgets['tree_view'].grid(row=0, column=0, sticky="nsew")

    def update_tree_view(self, data):
        data = data or promo_db.recuperar_promos()  # Recupera promoções do banco de dados se não houver dados fornecidos
        #print(f"Atualizando TreeView com dados: {data}")
        self.layout_widgets['tree_view'].delete(*self.layout_widgets['tree_view'].get_children())
        
        for item in data:
            self.layout_widgets['tree_view'].insert("", "end", values=(item['id'], item['nome'], item['valor']))

    def layout_promo_frame(self):
        titulo = criar_entradas(self.layout_widgets['frame_produtos'], "Editor de promoção", base_row=0, col=0)
        entry_nome = ctk.CTkEntry(self.layout_widgets['frame_produtos'], placeholder_text="Nome da Promoção")
        entry_valor = ctk.CTkEntry(self.layout_widgets['frame_produtos'], placeholder_text="Valor da Promoção")
        criar_promo_btn = ctk.CTkButton(self.layout_widgets['frame_produtos'], text="Criar Promoção Nova", command=lambda : self.operational_inserir_promo(entry_nome.get(), formatar_valor_para_sqlite(entry_valor.get())))
        atualizar_btn = ctk.CTkButton(self.layout_widgets['frame_produtos'], text="Atualizar Promoção", command=lambda: self.operational_atualizar_promo(self.layout_widgets['tree_view'].selection()[0], entry_nome.get(), entry_valor.get()))
        remover_btn = ctk.CTkButton(self.layout_widgets['frame_produtos'], text="Remover Promoção", command=lambda: self.operational_remover_promo())

        self.layout_inserir_novo_produto()

        entry_nome.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        entry_valor.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        criar_promo_btn.grid(row=3, column=0, padx=5, pady=5, sticky="sw")
        atualizar_btn.grid(row=3, column=1, padx=5, pady=5, sticky="sw")
        remover_btn.grid(row=3, column=2, padx=5, pady=5, sticky="sw")


    def layout_inserir_novo_produto(self):
        container = ctk.CTkFrame(self.layout_widgets['frame_produtos'])
        container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(container, label_text="Produtos na Promoção")
        adicionar_produto_btn = ctk.CTkButton(container, text="Adicionar Produto", command=lambda: self.layout_inserir_produto(self.scrollable_frame))
        limpar_campos_btn = ctk.CTkButton(container, text="Limpar Campos", command=self.quality_life_clear_entries)

        self.scrollable_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        adicionar_produto_btn.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        limpar_campos_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def layout_inserir_produto(self, frame, recovered_Data=None):
        if recovered_Data is None:
            if len(self.products_in_promo) >= 10: # Limite para usuário boca aberta
                messagebox.showerror("Erro", "Máximo de 10 produtos por promoção atingido.")
                return
            else:
                novo_produto = ctk.CTkComboBox(frame, values=list(self.tipos_dict.keys()))
                novo_produto.grid(row=len(self.products_in_promo), column=0, padx=5, pady=5, sticky="ew")
                remover_produto_btn = ctk.CTkButton(frame, text="Remover Produto")
                remover_produto_btn.grid(row=len(self.products_in_promo), column=1, padx=5, pady=5, sticky="ew")

                widget_data = {
                    'combo': novo_produto,
                    'remover_btn': remover_produto_btn
                }

                self.products_in_promo.append(widget_data)
                remover_produto_btn.configure(command=lambda: self.layout_remover_produto(widget_data))

            
        else:
            for produto in recovered_Data:
                novo_produto = ctk.CTkComboBox(frame, values=list(self.tipos_dict.keys()))
                novo_produto.set(produto['nome'])
                novo_produto.grid(row=len(self.products_in_promo), column=0, padx=5, pady=5, sticky="ew")
                remover_produto_btn = ctk.CTkButton(frame, text="Remover Produto")
                remover_produto_btn.grid(row=len(self.products_in_promo), column=1, padx=5, pady=5, sticky="ew")

                widget_data = {
                    'combo': novo_produto,
                    'remover_btn': remover_produto_btn
                }

                self.products_in_promo.append(widget_data)
                remover_produto_btn.configure(command=lambda wd = widget_data: self.layout_remover_produto(wd))

    def layout_remover_produto(self, produto):
        if produto in self.products_in_promo:
            produto['combo'].grid_forget()
            produto['remover_btn'].grid_forget()
            self.products_in_promo.remove(produto)
        else:
            messagebox.showerror("Erro", "Produto não encontrado na lista de promoções.")

    def linker_tree_view_promo_frame(self, event):
        selected_item = self.layout_widgets['tree_view'].selection()
        if selected_item:
            item_values = self.layout_widgets['tree_view'].item(selected_item, 'values')
            self.selected_promo_id = item_values[0] if item_values else None
            if self.products_in_promo:
                for produto in self.products_in_promo:
                    produto['combo'].grid_forget()
                    produto['remover_btn'].grid_forget()
            self.products_in_promo.clear()  # Limpa a lista de produtos na promoção
            self.layout_inserir_produto(self.scrollable_frame, promo_db.recuperar_produtos_promo(item_values[0]))  # Recupera produtos da promoção selecionada
            if item_values:
                promo_id, promo_nome, promo_valor = item_values

                self.layout_widgets['frame_produtos'].children['!ctkentry'].delete(0, 'end')
                self.layout_widgets['frame_produtos'].children['!ctkentry'].insert(0, promo_nome)
                self.layout_widgets['frame_produtos'].children['!ctkentry2'].delete(0, 'end')
                self.layout_widgets['frame_produtos'].children['!ctkentry2'].insert(0, promo_valor)

    def operational_inserir_promo(self, nome, valor):
        try:
            if not nome or not valor: # Error handle
                messagebox.showerror("Erro", "Nome e valor da promoção são obrigatórios.")
                return None
            if not self.products_in_promo: # Error handle
                messagebox.showerror("Erro", "Nenhum produto adicionado à promoção.")
                return None
            
            produtos = [produto['combo'].get() for produto in self.products_in_promo if produto['combo'].get()]
            id_list = [self.tipos_dict[produto] for produto in produtos if produto in self.tipos_dict]

            ret = promo_db.inserir_promo(nome, valor, id_list)  # Chama a função de inserção no banco de dados
            if ret:
                messagebox.showinfo("Sucesso", f"Promoção '{nome}' inserida com sucesso!")
                self.update_tree_view(promo_db.recuperar_promos())
            else:
                messagebox.showerror("Erro", "Falha ao inserir promoção no banco de dados.")
                return None

        except Exception as e:
            print(f"Erro ao inserir promoção: {e}")
            return None
    
    def operational_atualizar_promo(self, promo_id, nome, valor):
        if not promo_id:
            messagebox.showerror("Erro", "Nenhuma promoção selecionada para atualizar.")
            return
        if not nome or not valor:
            messagebox.showerror("Erro", "Nome e valor da promoção são obrigatórios.")
            return
        if not self.products_in_promo:
            messagebox.showerror("Erro", "Nenhum produto adicionado à promoção.")
            return
        
        promo_db.atualizar_promo(self.selected_promo_id, nome, valor, [produto['combo'].get() for produto in self.products_in_promo if produto['combo'].get()])
        self.update_tree_view(promo_db.recuperar_promos())
    
    def operational_remover_promo(self):
        if not self.selected_promo_id:
            messagebox.showerror("Erro", "Nenhuma promoção selecionada para remover.")
            return
        
        confirm = messagebox.askyesno("Confirmar Remoção", "Você tem certeza que deseja remover esta promoção?")
        if confirm:
            promo_db.excluir_promo(self.selected_promo_id)
            self.update_tree_view(promo_db.recuperar_promos())
            self.quality_life_clear_entries()
            messagebox.showinfo("Sucesso", "Promoção removida com sucesso!")

    def quality_life_clear_entries(self):
        while len(self.products_in_promo) > 0:
            produto = self.products_in_promo[0]
            self.layout_remover_produto(produto)
        self.layout_widgets['frame_produtos'].children['!ctkentry'].delete(0, 'end')
        self.layout_widgets['frame_produtos'].children['!ctkentry2'].delete(0, 'end')

    def quality_life_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",  
            fieldbackground="#2b2b2b",
            rowheight=25
        )
        style.map("Treeview",
            background=[("selected", "#444444")],
            foreground=[("selected", "white")]
        )

    def voltar(self):
        self.master.abrir_tela_compras()