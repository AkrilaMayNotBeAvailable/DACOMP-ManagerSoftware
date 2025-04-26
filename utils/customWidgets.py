import customtkinter as ctk
from tkinter import messagebox

# Usado para modificar os valores dos spinners:
#------------------------------------------------
def change_entry(entry, delta):
    try:
        value = int(entry.get())
    except ValueError:
        value = 0
    new_value = max(value + delta, 0)
    entry.delete(0, "end")
    entry.insert(0, str(new_value))
#------------------------------------------------

# Criação do spinner:
#------------------------------------------------
def create_spinner(master, row=0, column=0, columnspan=1, initial_value="0"):
    def change_entry(entry, delta):
        try:
            value = int(entry.get())
        except ValueError:
            value = 0
        new_value = max(value + delta, 0)
        entry.delete(0, "end")
        entry.insert(0, str(new_value))

    # Container do spinner (frame interno)
    spinner_frame = ctk.CTkFrame(master, fg_color="transparent")
    spinner_frame.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky="w")

    # Campo de entrada
    entry = ctk.CTkEntry(spinner_frame, width=60, justify="center")
    entry.insert(0, initial_value)
    
    # Botão "-"
    btn_decrement = ctk.CTkButton(
        spinner_frame, text="-", width=30, height=28,
        command=lambda: change_entry(entry, -1)
    )
    

    # Botão "+"
    btn_increment = ctk.CTkButton(
        spinner_frame, text="+", width=30, height=28,
        command=lambda: change_entry(entry, 1)
    )

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
def widget_prototype_product(frame, label_txt, placeholder, base_row, col):
    product = {}

    product['frame'] = ctk.CTkFrame(frame)
    product['frame'].grid(row=base_row, column=col, padx=5, pady=5, sticky="we")
    product['frame'].grid_rowconfigure(0, weight=1)

    product['name'] = ctk.CTkLabel(product['frame'], text=label_txt)
    product['name'].grid(row=0, column=0, sticky="we", padx=5)
    product['price'] = ctk.CTkLabel(product['frame'], text=f'R$ {float(placeholder):.2f}')
    product['price'].grid(row=0, column=5, sticky="we", padx=5)


    # Cantinho do DINHEIRO:
    #------------------------------------------------
    product['money'] = ctk.CTkLabel(product['frame'], text="DINHEIRO:")
    product['money'].grid(row=1, column=0, sticky="we", padx=5)
    
    spinner_widgets_money = create_spinner(product['frame'], row=1, column=1, columnspan=3)
    product['money_control'] = spinner_widgets_money["frame"]
    product['money_entry'] = spinner_widgets_money["entry"]
    product['money_increment'] = spinner_widgets_money["increment_button"]
    product['money_decrement'] = spinner_widgets_money["decrement_button"]
    #------------------------------------------------

    # Cantinho do CARTÃO:
    #------------------------------------------------
    # TODO: Implementar o cartão
    #------------------------------------------------

    # Cantinho do PIX:
    #------------------------------------------------
    product['pix'] = ctk.CTkLabel(product['frame'], text="PIX: ")
    product['pix'].grid(row=1, column=4, sticky="w", padx=5)

    spinner_widgets = create_spinner(product['frame'], row=1, column=5, columnspan=3)
    product['pix_control'] = spinner_widgets["frame"]
    product['pix_entry'] = spinner_widgets["entry"]
    product['pix_increment'] = spinner_widgets["increment_button"]
    product['pix_decrement'] = spinner_widgets["decrement_button"]
    #------------------------------------------------
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