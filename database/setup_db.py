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
    #---------------------
    # A tabela Tipo armazena os tipos de produtos disponíveis no sistema.
    # Cada tipo tem um ID único, um nome e um valor de venda.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tipo (
            ID_Tipo INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Tipo TEXT NOT NULL,
            Valor_de_Venda REAL DEFAULT 0
        );
    """)

    # Dados iniciais (só se o banco não existia)
    if not banco_existe:
        cursor.execute("""
            INSERT OR IGNORE INTO Tipo (Nome_Tipo, Valor_de_Venda) VALUES
            ('Barra de Cereal Ritter', 2.50),
            ('Coca-Cola', 4.00),
            ('Trento', 2.50),
            ('Cápsula de Café', 2.50),
            ('Monster', 10.00)
        """)

    # Tabela de combos
    #---------------------
    # Combos (promoções) são conjuntos de tipos que podem ser vendidos juntos.
    # Cada combo tem um nome e um valor de venda.
    # A tabela combos armazena os combos disponíveis.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Combos (
            ID_Combo INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Combo TEXT UNIQUE,
            Valor_Venda REAL DEFAULT 0
        )""")
    
    # Tabela de tipos em combos
    #---------------------
    # A tabela Combo_Tipo relaciona os tipos aos combos.
    # Cada entrada nesta tabela indica que um tipo específico faz parte de um combo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Combo_Tipo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Tipo INTEGER,
            ID_Combo INTEGER,
            FOREIGN KEY(ID_Tipo) REFERENCES Tipo(ID_Tipo),
            FOREIGN KEY(ID_Combo) REFERENCES Combo(ID_Combo)
        );
    """)
    
    # Vendas por tipo
    #---------------------
    # Esta tabela registra as vendas agregadas por tipo de produto.
    # Cada entrada contém a data da venda, a quantidade vendida por forma de pagamento (PIX ou dinheiro),
    # o valor total da venda, o valor unitário e o lucro líquido.
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

    # Tabela auxiliar FIFO
    #---------------------
    # Esta tabela auxilia no controle de estoque utilizando o método FIFO (First In, First Out).
    # Cada venda registrada aqui contém o ID do tipo, ID do produto, quantidade vendida,
    # valor unitário, valor de venda e a data da venda.
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
