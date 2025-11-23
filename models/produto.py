import mysql.connector
from config import db_config

class Produto:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_produtos():
        conn = Produto.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos ORDER BY id DESC")
        produtos = cursor.fetchall()
        conn.close()
        return produtos

    @staticmethod
    def get_produto(id):
        conn = Produto.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
        produto = cursor.fetchone()
        conn.close()
        return produto

    @staticmethod
    def criar_produto(nome, preco, estoque_minimo, categoria=None, unidade=None):
        conn = Produto.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, preco, estoque_minimo, categoria, unidade)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, preco, estoque_minimo, categoria, unidade))
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar_produto(id, nome, preco, estoque_minimo, categoria=None, unidade=None):
        conn = Produto.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produtos
            SET nome=%s, preco=%s, estoque_minimo=%s, categoria=%s, unidade=%s
            WHERE id=%s
        """, (nome, preco, estoque_minimo, categoria, unidade, id))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_produto(id):
        conn = Produto.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
        conn.commit()
        conn.close()