# database/produtos_db.py
import random
from database.setup_db import conectar

DB_PATH = "sistema_compras.db"

def gerar_codigo_barras_unico():
    with conectar() as conn:
        cursor = conn.cursor()
        while True:
            codigo = ''.join([str(random.randint(0, 9)) for _ in range(13)])
            cursor.execute("SELECT 1 FROM produtos WHERE cod_barras = ?", (codigo,))
            if not cursor.fetchone():
                return codigo

def buscar_id_tipo_por_nome(tipo_nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tipos WHERE tipo = ?", (tipo_nome,))
        return cursor.fetchone()

'''
    CRUD de produtos:
        - Inserir produto
        - O read tá na interface.
        - Atualizar produto
        - Remover produto 
'''
def inserir_produto(dados):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (id_compra, id_tipo, validade, cod_barras, nome, valor_unit, quantidade, estoque)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conn.commit()

def recuperar_produtos_por_compra(id_compra, ordenacao=0):
    with conectar() as conn:
        cursor = conn.cursor()
        query = " SELECT * FROM produtos WHERE id_compra = ?"
        if ordenacao == 1:
            query += " ORDER BY nome ASC"
        elif ordenacao == 2:
            query += " ORDER BY valor_unit ASC"
        elif ordenacao == 3:
            query += " ORDER BY quantidade DESC"
        elif ordenacao == 4:
            query += " ORDER BY id_tipo ASC"
        cursor.execute(query, (id_compra,))
        return cursor.fetchall()

def atualizar_produto(id_prod, dados):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produtos
            SET nome = ?, valor_unit = ?, quantidade = ?, estoque = ?, cod_barras = ?, validade = ?, id_tipo = ?
            WHERE id = ?
        """, (*dados, id_prod))
        conn.commit()

def remover_produto(id_produto):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
