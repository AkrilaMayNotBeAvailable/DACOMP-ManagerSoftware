# Database/compras.py
from database.setup_db import conectar
import sqlite3

''' CRUD de compras:
    - criar_compra
    - carregar_compras
'''
def criar_compra(dados):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO compras (local, data_encomenda, data_recebimento, valor_total, chave_nota)
                VALUES (?, ?, ?, ?, ?)
            """, dados)
            conn.commit()
            return cursor.lastrowid  # Retorna o ID da compra criada
    except sqlite3.Error as e:
        print(f"Erro ao criar compra: {e}")
        return None
    
def carregar_compras():
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT local, data_encomenda, chave_nota FROM compras ORDER BY id DESC")
            compras = cursor.fetchall()
            return compras
    except sqlite3.Error as e:
        print(f"Erro ao carregar compras: {e}")
        return []