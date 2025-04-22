import sqlite3

def conectar():
    conn = sqlite3.connect("sistema_compras.db")
    cursor = conn.cursor()

    # Tabela de compras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            local TEXT,
            data_encomenda DATE,
            data_recebimento DATE,
            valor_total REAL,
            chave_nota TEXT UNIQUE
        )""")

    # Tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER,
            id_tipo INTEGER,
            validade DATE,
            cod_barras TEXT,
            nome TEXT,
            valor_unit REAL,
            quantidade INTEGER,
            estoque INTEGER,
            FOREIGN KEY (id_compra) REFERENCES compras (id)
            FOREIGN KEY (id_tipo) REFERENCES tipos (id)
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT UNIQUE,
            valor REAL
        )""")


    # Tipo Barrinha de Cereal, 2.50
    # Tipo Coca-Cola, 4.00
    # Tipo Trento, 2.50 (...)
    cursor.execute("""
        INSERT OR IGNORE INTO tipos (tipo, valor) VALUES
        ('Barra de Cereal Ritter', 2.50),
        ('Coca-Cola', 4.00),
        ('Trento', 2.50),
        ('Cápsula de Café', 2.50),
        ('Monster', 10.00)
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_tipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tipo INTEGER,
            id_produto INTEGER,
            FOREIGN KEY (id_tipo) REFERENCES tipos (id),
            FOREIGN KEY (id_produto) REFERENCES produtos (id)
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            valor REAL
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_combo INTEGER,
            id_produto INTEGER,
            FOREIGN KEY (id_combo) REFERENCES combos (id),
            FOREIGN KEY (id_produto) REFERENCES produtos (id)
        )""")

    conn.commit()
    conn.close()
