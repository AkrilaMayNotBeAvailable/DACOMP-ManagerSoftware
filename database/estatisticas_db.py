#database/estatisticas_db.py

from database.setup_db import conectar
import sqlite3

def recuperar_total_vendas(data):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(valor_total) FROM vendas_tipos WHERE data_venda = ?", (f"{data}",))
        total_vendas = cursor.fetchone()[0]
        #total_vendas = sum([venda[0] for venda in total_vendas])
        return total_vendas if total_vendas else 0.0
    
def recuperar_mais_vendido(data):
    with conectar() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_tipo, quantidade_pix, quantidade_dinheiro
            FROM vendas_tipos
            WHERE data_venda = ?
            ORDER BY quantidade_pix + quantidade_dinheiro DESC
            LIMIT 1
        """
        cursor.execute(query, (f"{data}",))
        mais_vendido = cursor.fetchone()
        if mais_vendido:
            id_tipo, quantidade_pix, quantidade_dinheiro = mais_vendido
            cursor.execute("SELECT tipo FROM tipos WHERE id = ?", (id_tipo,))
            tipo_produto = cursor.fetchone()[0]
            return tipo_produto, quantidade_pix + quantidade_dinheiro
        else:
            return None
        
def recuperar_lucro_liquido(data):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(lucro_liquido) FROM vendas_tipos WHERE data_venda = ?", (f"{data}",))
        lucro_liquido = cursor.fetchone()[0]
        return lucro_liquido if lucro_liquido else 0.0