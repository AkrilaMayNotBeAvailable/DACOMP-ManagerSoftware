from datetime import datetime
from tkinter import messagebox
from database import estatisticas_db as db

'''
"""Aceita datas DD/MM/AAAA ou DD/MM/AA e converte para AAAA-MM-DD"""
def formatar_data_para_sqlite(data_str):
    try:
        if len(data_str.split('/')[-1]) == 2:  # ano com 2 dígitos
            data = datetime.strptime(data_str, "%d/%m/%y")
        else:
            data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erro", f"Data inválida: {data_str}. Formato esperado: DD/MM/AAAA ou DD/MM/AA")
        return None  # ou lançar uma exceção
'''
from datetime import datetime
from tkinter import messagebox

def formatar_data_para_sqlite(data_str):
    """Aceita datas nos formatos DD/MM/AAAA, DD/MM/AA ou AAAA-MM-DD e converte para AAAA-MM-DD"""
    formatos_aceitos = ["%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"]
    
    for formato in formatos_aceitos:
        try:
            data = datetime.strptime(data_str, formato)
            return data.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Se nenhum formato for válido
    messagebox.showerror("Erro", f"Data inválida: {data_str}. Formatos aceitos: DD/MM/AAAA, DD/MM/AA ou AAAA-MM-DD")
    return None

"""Converte um valor digitado com vírgula para ponto e retorna como float."""
def formatar_valor_para_sqlite(valor_str):
    try:
        # Remove espaços
        valor_str = valor_str.strip()
        # Substitui vírgula por ponto
        valor_str = valor_str.replace(',', '.')
        # Converte para float
        return float(valor_str)
    except ValueError:
        return None  # Ou lança um erro, dependendo da estratégia
    
def recuperar_informacoes_caixa(data):
    lucro_liquido = db.recuperar_lucro_liquido(data)
    vendidos = db.recuperar_mais_vendido(data)
    valor_bruto = db.recuperar_total_vendas(data)

    if vendidos is None:
        vendidos = ("Nenhum produto vendido", 0)
    else:
        vendidos = (vendidos[0], vendidos[1])
        
    if lucro_liquido is None:
        lucro_liquido = 0.0

    if valor_bruto is None:
        valor_bruto = 0.0

    return {
        "lucro_liquido": lucro_liquido,
        "vendidos": vendidos,
        "valor_bruto": valor_bruto
    }
