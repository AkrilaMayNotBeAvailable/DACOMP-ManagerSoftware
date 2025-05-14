# database/caixa_db.py
from database.setup_db import conectar
import sqlite3

# Função de venda
def registrar_venda(id_tipo, quantidade, forma_pagamento):
    try:
        with conectar() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT valor FROM tipos WHERE id = ?", (id_tipo,))
            valor_venda = cursor.fetchone()[0]

            quantidade_restante = quantidade
            lucro_liquido = 0.0

            cursor.execute("""
                SELECT id, estoque, valor_unit FROM produtos
                WHERE id_tipo = ? AND estoque > 0
                ORDER BY id ASC
            """, (id_tipo,))
            produtos = cursor.fetchall()

            for prod_id, estoque, valor_unit in produtos:
                if quantidade_restante <= 0:
                    break

                usado = min(estoque, quantidade_restante)

                # Atualiza estoque
                cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (usado, prod_id))

                # Registra item vendido
                cursor.execute("""
                    INSERT INTO tabela_auxiliar_FIFO (id_tipo, id_produto, quantidade, valor_unit, valor_venda, data_venda)
                    VALUES (?, ?, ?, ?, ?, DATE('now', '-03:00'))
                """, (id_tipo, prod_id, usado, valor_unit, valor_venda))

                lucro_liquido += (valor_venda - valor_unit) * usado
                quantidade_restante -= usado

            # Atualiza venda agregada
            cursor.execute("""
                INSERT INTO vendas_tipos (id_tipo, data_venda, quantidade_pix, quantidade_dinheiro, valor_total, valor_unit, lucro_liquido)
                VALUES (?, DATE('now', '-03:00'), ?, ?, ?, ?, ?)
                ON CONFLICT(id_tipo, data_venda, valor_unit) DO UPDATE SET
                    quantidade_pix = quantidade_pix + excluded.quantidade_pix,
                    quantidade_dinheiro = quantidade_dinheiro + excluded.quantidade_dinheiro,
                    valor_total = valor_total + excluded.valor_total,
                    lucro_liquido = ROUND(lucro_liquido + excluded.lucro_liquido, 2)
            """, (
                id_tipo,
                quantidade if forma_pagamento == "pix" else 0,
                quantidade if forma_pagamento == "dinheiro" else 0,
                quantidade * valor_venda,
                valor_venda,
                lucro_liquido
            ))

    except Exception as e:
        print("Erro ao registrar venda:", e)


# Função de reverter venda
def reverter_venda(id_tipo, quantidade, forma_pagamento):
    try:
        with conectar() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT valor FROM tipos WHERE id = ?", (id_tipo,))
            resultado = cursor.fetchone()
            if not resultado:
                return
            valor_venda = resultado[0]

            quantidade_restante = quantidade
            lucro_liquido_reverter = 0.0

            # Busca itens vendidos hoje, do mais recente para o mais antigo
            cursor.execute("""
                SELECT id_venda, id_produto, quantidade, valor_unit
                FROM tabela_auxiliar_FIFO
                WHERE id_tipo = ? AND data_venda = DATE('now', '-03:00') AND valor_venda = ?
                ORDER BY id_venda DESC
            """, (id_tipo, valor_venda))
            itens = cursor.fetchall()

            for id_venda, id_produto, qtd_vendida, valor_unit in itens:
                if quantidade_restante <= 0:
                    break

                devolver = min(qtd_vendida, quantidade_restante)

                # Atualiza estoque
                cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (devolver, id_produto))

                # Se toda a quantidade deste item foi revertida, remova o registro
                if devolver == qtd_vendida:
                    cursor.execute("DELETE FROM tabela_auxiliar_FIFO WHERE id_venda = ?", (id_venda,))
                else:
                    cursor.execute("""
                        UPDATE tabela_auxiliar_FIFO SET quantidade = quantidade - ?
                        WHERE id_venda = ?
                    """, (devolver, id_venda))

                lucro_liquido_reverter += (valor_venda - valor_unit) * devolver
                quantidade_restante -= devolver

            # Atualiza o resumo da venda
            cursor.execute("""
                UPDATE vendas_tipos SET
                    quantidade_pix = MAX(quantidade_pix - ?, 0),
                    quantidade_dinheiro = MAX(quantidade_dinheiro - ?, 0),
                    valor_total = MAX(valor_total - ?, 0),
                    lucro_liquido = ROUND(MAX(lucro_liquido - ?, 0), 2)
                WHERE id_tipo = ? AND data_venda = DATE('now', '-03:00') AND valor_unit = ?
            """, (
                quantidade if forma_pagamento == "pix" else 0,
                quantidade if forma_pagamento == "dinheiro" else 0,
                quantidade * valor_venda,
                lucro_liquido_reverter,
                id_tipo,
                valor_venda
            ))

            print(f"[REVERTER] Reversão finalizada para tipo {id_tipo}, forma: {forma_pagamento}, qtd: {quantidade}, lucro revertido: {lucro_liquido_reverter:.2f}")
    except Exception as e:
        print("Erro ao reverter venda:", e)




def carregar_dados_vendas_do_dia(lista_produtos, data):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_tipo, quantidade_pix, quantidade_dinheiro, valor_unit 
                FROM vendas_tipos 
                WHERE data_venda = ?
            """, (data,))
            registros = cursor.fetchall()
            print(f"[ATUALIZAR] Registros encontrados: {registros}")

            vendas_por_tipo = {}
            for id_tipo, qtd_pix, qtd_dinheiro, valor_unit in registros:
                if id_tipo not in vendas_por_tipo:
                    vendas_por_tipo[id_tipo] = {'pix': 0, 'dinheiro': 0}
                vendas_por_tipo[id_tipo]['pix'] += qtd_pix
                vendas_por_tipo[id_tipo]['dinheiro'] += qtd_dinheiro

            for produto in lista_produtos:
                tipo_id = produto.get("tipo_id")
                if tipo_id in vendas_por_tipo:
                    vendas = vendas_por_tipo[tipo_id]
                    produto['pix_entry'].delete(0, "end")
                    produto['money_entry'].delete(0, "end")
                    produto['pix_entry'].insert(0, str(vendas['pix']))
                    produto['money_entry'].insert(0, str(vendas['dinheiro']))
                    #print(f"[ATUALIZAR] Tipo {tipo_id} | Pix: {vendas['pix']} | Dinheiro: {vendas['dinheiro']}")

    except Exception as e:
        print("Erro ao carregar vendas do dia:", e)

def buscar_caixa():
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT data_venda FROM vendas_tipos
                LIMIT 30
            """)
            caixa = cursor.fetchall()
            print(f"[BUSCAR] Registros encontrados: {caixa}")
            # Se não houver registros, retorna uma lista vazia
            if not caixa:
                return []
            # Se houver registros, retorna a lista de caixas
            return [item[0] for item in caixa]
    except sqlite3.Error as e:
        print(f"Erro ao buscar caixa: {e}")
        return []
            
def get_estoque(tipo_id):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT estoque FROM produtos WHERE id_tipo = ?
            """, (tipo_id,))
            estoque = cursor.fetchall()

            # Se não houver registros, retorna 0
            if not estoque:
                return 0
            # Se houver registros, retorna a soma dos estoques
            return sum(item[0] for item in estoque)
    except sqlite3.Error as e:
        print(f"Erro ao buscar estoque: {e}")
        return 0
    
def get_valor_unit(tipo_id):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT valor_unit 
                FROM produtos 
                WHERE id_tipo = ? AND estoque > 0
                ORDER BY id ASC
            """, (tipo_id,))
            valor_unit = cursor.fetchall()
            cursor.execute("""
                SELECT valor 
                FROM tipos 
                WHERE id = ?
                ORDER BY id ASC
            """, (tipo_id,))
            valor_venda = cursor.fetchall()
            print(f"[BUSCAR] Valor de venda encontrado: {valor_venda}")
            print(f"[BUSCAR] Valor unitário encontrado: {valor_unit}")
            # Se não houver registros, retorna 0
            if not valor_unit:
                return 0
            # Se houver registros, retorna o valor unitário
            return valor_venda[0][0] - valor_unit[0][0]
    except sqlite3.Error as e:
        print(f"Erro ao buscar valor unitário: {e}")
        return 0