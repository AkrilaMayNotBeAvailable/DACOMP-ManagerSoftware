from datetime import datetime
from tkinter import messagebox

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