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
        cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
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
        conn = Pedido.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id=%s", (id,))
        conn.commit()
        conn.close()

