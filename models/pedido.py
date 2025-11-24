import mysql.connector
from config import db_config

class Pedido:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_pedidos():
        conn = Pedido.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, f.nome_empresa AS fornecedor_nome
            FROM pedidos p
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            ORDER BY p.id DESC
        """)
        pedidos = cursor.fetchall()
        conn.close()
        return pedidos

    @staticmethod
    def get_pedido(id):
        conn = Pedido.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
        pedido = cursor.fetchone()
        conn.close()
        return pedido

    @staticmethod
    def criar_pedido(fornecedor_id, usuario_id, data_pedido=None, status=None, valor_total=None):
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pedidos (fornecedor_id, usuario_id, data_pedido, status, valor_total)
            VALUES (%s, %s, %s, %s, %s)
        """, (fornecedor_id, usuario_id, data_pedido, status, valor_total))
        conn.commit()
        pedido_id = cursor.lastrowid
        conn.close()
        return pedido_id

    @staticmethod
    def add_item(pedido_id, produto_id, quantidade, preco_unitario):
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
        """, (pedido_id, produto_id, quantidade, preco_unitario))
        conn.commit()
        conn.close()

    @staticmethod
    def get_itens_por_pedido(pedido_id):
        conn = Pedido.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ip.*, p.nome AS nome_produto, p.preco AS preco_produto
            FROM itens_pedido ip
            LEFT JOIN produtos p ON ip.produto_id = p.id
            WHERE ip.pedido_id = %s
        """, (pedido_id,))
        itens = cursor.fetchall()
        conn.close()
        return itens

    @staticmethod
    def deletar_itens_por_pedido(pedido_id):
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM itens_pedido WHERE pedido_id = %s", (pedido_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar_pedido(id, fornecedor_id, data_pedido=None, status=None, valor_total=None):
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pedidos
            SET fornecedor_id=%s, data_pedido=%s, status=%s, valor_total=%s
            WHERE id=%s
        """, (fornecedor_id, data_pedido, status, valor_total, id))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_pedido(id):
        Pedido.deletar_itens_por_pedido(id)
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id=%s", (id,))
        conn.commit()
        conn.close()