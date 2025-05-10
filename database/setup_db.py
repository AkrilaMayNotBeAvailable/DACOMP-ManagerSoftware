# database/setup_db.py
import sqlite3
import os

''' Startup do banco de dados:
    - Cria o banco de dados se não existir
    - Cria as tabelas necessárias
    - Insere dados iniciais (tipos de produtos)

    Criado para organizar testes iniciais e facilitar a manutenção do código.
'''

DB_PATH = "sistema_compras.db"

# Conecta ao banco de dados e retorna a conexão
def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    # Verifica se o arquivo do banco já existe
    banco_existe = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
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
            FOREIGN KEY (id_compra) REFERENCES compras (id),
            FOREIGN KEY (id_tipo) REFERENCES tipos (id)
        )""")

    # Tabela de tipos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT UNIQUE,
            valor REAL
        )""")

    # Dados iniciais (só se o banco não existia)
    if not banco_existe:
        cursor.execute("""
            INSERT OR IGNORE INTO tipos (tipo, valor) VALUES
            ('Barra de Cereal Ritter', 2.50),
            ('Coca-Cola', 4.00),
            ('Trento', 2.50),
            ('Cápsula de Café', 2.50),
            ('Monster', 10.00)
        """)

    # Relação entre produtos e tipos (se precisar no futuro)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_tipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tipo INTEGER,
            id_produto INTEGER,
            FOREIGN KEY (id_tipo) REFERENCES tipos (id),
            FOREIGN KEY (id_produto) REFERENCES produtos (id)
        )""")

    # Tabela de combos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE,
            valor REAL
        )""")

    # Relação entre combos e produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_combo INTEGER,
            id_produto INTEGER,
            FOREIGN KEY (id_combo) REFERENCES combos (id),
            FOREIGN KEY (id_produto) REFERENCES produtos (id)
        )""")
    
    # Vendas por tipo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas_tipos (
        id INTEGER PRIMARY KEY,
        id_tipo INTEGER,
        data_venda DATE,
        quantidade_pix INTEGER DEFAULT 0,
        quantidade_dinheiro INTEGER DEFAULT 0,
        valor_total REAL DEFAULT 0,
        valor_unit REAL DEFAULT 0,
        lucro_liquido REAL DEFAULT 0,
        UNIQUE(id_tipo, data_venda, valor_unit)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tabela_auxiliar_FIFO (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_tipo INTEGER,
        id_produto INTEGER,
        quantidade INTEGER,
        valor_unit REAL,
        valor_venda REAL,
        data_venda DATE
    )
    """)
    

    conn.commit()
    conn.close()
