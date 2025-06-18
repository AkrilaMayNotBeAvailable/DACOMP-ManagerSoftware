from database.setup_db import conectar
from database.tipos_db import recuperar_tipos

def inserir_promo(nome, valor, tipos):
    ''' Passo 1: Insere informações bases do combo na tabela Combos
        Passo 2: Insere os tipos selecionados na tabela relacional Combo_Tipo
        Retorna o ID do combo inserido ou None em caso de erro.
    '''
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Combos (Nome_Combo, Valor_Venda) VALUES (?, ?)", (nome, valor))
            id_combo = cursor.lastrowid

            for tipo, _ in tipos: # Insere os tipos na tabela relacional
                cursor.execute("""
                    INSERT INTO Combo_Tipo (ID_Tipo, ID_Combo)
                    VALUES (?, ?)
                """, (tipo, id_combo))

            conn.commit()
            return id_combo
    except Exception as e:
        print(f"Erro ao inserir combo: {e}")
        return None
    
def recuperar_promos():
    ''' Recupera todas as promoções do banco de dados.
        Retorna uma lista de dicionários com os dados das promoções.
    '''
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.ID_Combo, c.Nome_Combo, c.Valor_Venda
                FROM Combos c
            """)
            promos = cursor.fetchall()
            return [{'id': row[0], 'nome': row[1], 'valor': row[2]} for row in promos]
    except Exception as e:
        print(f"Erro ao recuperar promoções: {e}")
        return []
    
def recuperar_produtos_promo(combo_id):
    ''' Recupera os produtos associados a uma promoção específica.
        Retorna uma lista de dicionários com os dados dos produtos.
    '''
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.ID_Tipo, t.Nome_Tipo
                FROM Tipo t
                JOIN Combo_Tipo ct ON t.ID_Tipo = ct.ID_Tipo
                WHERE ct.ID_Combo = ?
            """, (combo_id,))
            produtos = cursor.fetchall()
            return [{'id': row[0], 'nome': row[1]} for row in produtos]
    except Exception as e:
        print(f"Erro ao recuperar produtos da promoção: {e}")
        return []
    
def recuperar_tipos_dict():
    tipos = recuperar_tipos()  # [(id, nome, valor, categoria), ...]
    return {nome: (id_tipo, valor) for id_tipo, nome, categoria, valor in tipos}
    
def atualizar_promo(combo_id, nome, valor, tipos, is_ID=False):
    ''' Atualiza as informações de uma promoção existente.
        Passo 1: Atualiza as informações bases do combo na tabela Combos
        Passo 2: Atualiza os tipos selecionados na tabela relacional Combo_Tipo
        Retorna True se a atualização for bem-sucedida, False em caso de erro.
    '''
    print(f"Atualizando promo: {combo_id}, {nome}, {valor}, {tipos}")  # DEBUG
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Combos SET Nome_Combo = ?, Valor_Venda = ? WHERE ID_Combo = ?", (nome, valor, combo_id))

            # Limpa os tipos antigos
            cursor.execute("DELETE FROM Combo_Tipo WHERE ID_Combo = ?", (combo_id,))
            print(f"Tipos antigos removidos para o combo {combo_id}")

            if not is_ID:
                _loc = []
                for tipo in tipos:
                    cursor.execute("SELECT ID_Tipo FROM Tipo WHERE Nome_Tipo = ?", (tipo,))
                    _loc.append(cursor.fetchone()[0])
                tipos = _loc # recupera o ID dos tipos enviados como parametro

            # Insere os novos tipos
            for tipo in tipos:
                cursor.execute("""
                    INSERT INTO Combo_Tipo (ID_Tipo, ID_Combo)
                    VALUES (?, ?)
                """, (tipo, combo_id))

            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao atualizar promo: {e}")
        return False
    
def excluir_promo(combo_id):
    ''' Exclui uma promoção do banco de dados.
        Retorna True se a exclusão for bem-sucedida, False em caso de erro.
    '''
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Combo_Tipo WHERE ID_Combo = ?", (combo_id,))
            cursor.execute("DELETE FROM Combos WHERE ID_Combo = ?", (combo_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao excluir promo: {e}")
        return False