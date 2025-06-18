# database/tipos.py
from database.setup_db import conectar
'''
    CRUD de tipos de produtos:
        - Inserir tipo de produto
        - Atualizar tipo de produto
        - Remover tipo de produto
'''
def inserir_tipo_produto(tipo_produto, tipo_categoria, tipo_valor):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tipo (Nome_Tipo, Categoria, Valor_de_Venda) VALUES (?, ?, ?)", (tipo_produto, tipo_categoria, tipo_valor))
        conn.commit()
        print(f"Tipo de produto '{tipo_produto}' inserido com sucesso.")

def atualizar_tipo_produto(id_tipo, tipo_nome, categoria, tipo_valor):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Tipo SET Nome_Tipo = ?, Categoria = ?, Valor_de_Venda = ? WHERE ID_Tipo = ?", (tipo_nome, categoria, tipo_valor, id_tipo))
        conn.commit()
        print(f"Tipo de produto com ID {id_tipo} atualizado para '{tipo_nome}' com valor {tipo_valor} e categoria {categoria}.")

def atualizar_todos_tipos(id_tipo, dados):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Tipo
            SET Nome_Tipo = ?, Categoria = ?, Valor_de_Venda = ?
            WHERE ID_Tipo = ?
        """, (*dados, id_tipo))
        conn.commit()

def recuperar_tipos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Tipo, Nome_Tipo, Categoria, Valor_de_Venda FROM Tipo ORDER BY Nome_Tipo")
        return cursor.fetchall()

def remover_tipo_produto(id_tipo):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Tipo WHERE ID_Tipo = ?", (id_tipo,))
        conn.commit()
        print(f"Tipo de produto com ID {id_tipo} removido com sucesso.")
    
def load_database_tipos(categoria=None):
    with conectar() as conn:
        cursor = conn.cursor()
        
        if categoria:
            cursor.execute("SELECT ID_Tipo, Nome_Tipo, Valor_de_Venda FROM Tipo WHERE Categoria = ?", (categoria,))
        else:
            cursor.execute("SELECT ID_Tipo, Nome_Tipo, Valor_de_Venda FROM Tipo")
    
    return cursor.fetchall()

def recover_types_by_ordering(order=0):
    with conectar() as conn:
        cursor = conn.cursor()
        query = " SELECT * FROM Tipo"
        if order == 1:
            query += " ORDER BY ID_Tipo ASC"
        elif order == 2:
            query += " ORDER BY Nome_Tipo ASC"
        elif order == 3:
            query += " ORDER BY Categoria ASC"
        elif order == 4:
            query += " ORDER BY Valor_de_Venda DESC"
        cursor.execute(query)
        return cursor.fetchall()
