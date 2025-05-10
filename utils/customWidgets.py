import customtkinter as ctk
from tkinter import messagebox

from database import caixa_db as db

# Criação do spinner:
#------------------------------------------------
def create_spinner(master, row=0, column=0, columnspan=1, initial_value="0", on_change=None, on_revert=None):
    def change_entry(entry, delta):
        try:
            value = int(entry.get())
        except ValueError:
            value = 0
        new_value = value + delta
        entry.delete(0, "end")
        entry.insert(0, str(new_value))
        
        if delta > 0 and on_change:
            on_change(new_value, delta)
        elif delta < 0 and on_revert:
            print(new_value)
            if new_value < 0:
                messagebox.showwarning("Atenção", "Valor não pode ser menor que zero.")
                new_value = 0
                entry.delete(0, "end")
                entry.insert(0, str(new_value))
            else:
                on_revert(new_value, delta)

    spinner_frame = ctk.CTkFrame(master, fg_color="transparent")
    spinner_frame.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky="w")

    entry = ctk.CTkEntry(spinner_frame, width=60, justify="center" )
    entry.insert(0, initial_value)

    btn_decrement = ctk.CTkButton(spinner_frame, text="-", width=30, height=28, command=lambda: change_entry(entry, -1), fg_color="#6f0c0c", hover_color="#5f0c0c")
    btn_increment = ctk.CTkButton(spinner_frame, text="+", width=30, height=28, command=lambda: change_entry(entry, 1), fg_color="#0c6f23", hover_color="#0c5f23")

    btn_decrement.pack(side="left", padx=2)
    entry.pack(side="left", padx=2)
    btn_increment.pack(side="left", padx=2)

    return {
        "frame": spinner_frame,
        "entry": entry,
        "increment_button": btn_increment,
        "decrement_button": btn_decrement
    }
#------------------------------------------------


# Auxiliar para criar entradas de texto:
#------------------------------------------------
def widget_prototype_product(frame, label_txt, tipo_id, preco, base_row, col):
    def on_pix_change(new_value, delta):
        db.registrar_venda(tipo_id, 1, "pix")

    def on_pix_revert(new_value, delta):
        db.reverter_venda(tipo_id, 1, "pix")

    def on_money_change(new_value, delta):
        db.registrar_venda(tipo_id, 1, "dinheiro")

    def on_money_revert(new_value, delta):
        db.reverter_venda(tipo_id, 1, "dinheiro")

    product = {}
    product['frame'] = ctk.CTkFrame(frame)
    product['frame'].grid(row=base_row, column=col, padx=10, pady=10, sticky="nswe")
    product['frame'].grid_rowconfigure(0, weight=1)
    product['frame'].grid_rowconfigure(1, weight=0)  # Linha do dinheiro e pix
    product['frame'].grid_columnconfigure(0, weight=1)  # Expande o nome
    
    product['subframe'] = ctk.CTkFrame(product['frame']) # A porcaria do frame que tem que ter o columnspan
    product['subframe'].grid(row=0, column=0, columnspan=8, padx=5, pady=5, sticky="we")

    # Configura o layout do subframe com 3 colunas
    product['subframe'].grid_columnconfigure(0, weight=0)  # Label nome
    product['subframe'].grid_columnconfigure(1, weight=1)  # Espaço expansível
    product['subframe'].grid_columnconfigure(2, weight=0)  # Label preço

    # Nome à esquerda
    product['name'] = ctk.CTkLabel(product['subframe'], text=label_txt, font=("Arial", 16, "bold"))
    product['name'].grid(row=0, column=0, sticky="w", padx=(10, 5))

    # Preço à direita
    product['price'] = ctk.CTkLabel(product['subframe'], text=f'R$ {float(preco):.2f}', font=("Arial", 16, "bold"))
    product['price'].grid(row=0, column=2, sticky="e", padx=(5, 10))
    # Dinheiro
    product['money'] = ctk.CTkLabel(product['frame'], text="DINHEIRO:")
    product['money'].grid(row=1, column=0, sticky="we", padx=5)
    spinner_widgets_money = create_spinner(product['frame'], row=1, column=1, columnspan=3, on_change=on_money_change, on_revert=on_money_revert)
    product['money_entry'] = spinner_widgets_money["entry"]

    # Pix
    product['pix'] = ctk.CTkLabel(product['frame'], text="PIX: ")
    product['pix'].grid(row=1, column=4, sticky="w", padx=5)
    spinner_widgets_pix = create_spinner(product['frame'], row=1, column=5, columnspan=3, on_change=on_pix_change, on_revert=on_pix_revert)
    product['pix_entry'] = spinner_widgets_pix["entry"]

    product['tipo_id'] = tipo_id

    return product
#------------------------------------------------


# Criação do scrollable frame:
def widget_scrollable_form(frame, row=0, column=0, columnspan=1):
    scrollable_frame = ctk.CTkScrollableFrame(frame, width=300, label_text="Itens da Compra")
    scrollable_frame.grid(row=row, column=column, columnspan=columnspan, pady=10, sticky="nswe")

    # Configuração do scrollable frame
    scrollable_frame.grid_rowconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    return scrollable_frame
#------------------------------------------------

''' Dado um Widget, cria label e widget de entrada. Utilzando grids para posicionar os widgets.
        > label_txt: Texto do label.
        > placeholder: Placeholder do widget de entrada.
        > base_row: Linha base para o grid.
        > col: Coluna base para o grid.
        > widget: Tipo de widget a ser criado. Pode ser 'entry' ou 'combobox'.
    Retorna um dicionário com o label e o widget criado. 
        >> Chaves: 'label', 'entry' ou 'combobox'.
'''
def criar_entradas(frame, label_txt='N/A', placeholder='', base_row=0, col=0, widget='title', ): # mudei isso
    custom_widget = {}
    

    if widget == 'title': # Título
        label = ctk.CTkLabel(frame, text=label_txt, font=("Arial", 16, "bold"))
        label.grid(row=base_row, column=col, sticky="w", padx=5)
        custom_widget['title'] = label
    else:
        label = ctk.CTkLabel(frame, text=label_txt)
        label.grid(row=base_row, column=col, sticky="w", padx=5)
        custom_widget['label'] = label

    if widget == 'entry': # Entrada de texto
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=base_row + 1, column=col, padx=5, pady=(0, 0), columnspan=1, sticky="we")
        custom_widget['entry'] = entry
    
    elif widget == 'entry_autofill': # Entrada de texto com autocompletar
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.insert(0, placeholder)
        entry.grid(row=base_row + 1, column=col, padx=5, pady=(0, 0), columnspan=1, sticky="we")
        custom_widget['entry'] = entry
    
    elif widget == 'combobox': # Entrada de Combobox
        entry = ctk.CTkComboBox(frame, values=placeholder)
        entry.grid(row=base_row + 1, column=col, padx=5, pady=(0, 0), columnspan=1, sticky="we")
        custom_widget['combobox'] = entry

    return custom_widget