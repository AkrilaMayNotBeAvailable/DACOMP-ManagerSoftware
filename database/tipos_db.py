# database/tipos.py
from database.setup_db import conectar
import sqlite3

'''
    CRUD de tipos de produtos:
        - Inserir tipo de produto
        - Atualizar tipo de produto
        - Remover tipo de produto
'''
def inserir_tipo_produto(tipo_produto, tipo_valor):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tipos (tipo, valor) VALUES (?, ?)", (tipo_produto, tipo_valor))
        conn.commit()
        print(f"Tipo de produto '{tipo_produto}' inserido com sucesso.")

def atualizar_tipo_produto(id_tipo, tipo_nome, tipo_valor):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tipos SET tipo = ?, valor = ? WHERE id = ?", (tipo_nome, tipo_valor, id_tipo))
        conn.commit()
        print(f"Tipo de produto com ID {id_tipo} atualizado para '{tipo_nome}' com valor {tipo_valor}.")

def recuperar_tipos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, valor FROM tipos ORDER BY tipo")
        return cursor.fetchall()

def remover_tipo_produto(id_tipo):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipos WHERE id = ?", (id_tipo,))
        conn.commit()
        print(f"Tipo de produto com ID {id_tipo} removido com sucesso.")