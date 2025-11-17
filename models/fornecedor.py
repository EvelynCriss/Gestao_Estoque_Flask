import mysql.connector
from config import db_config

class Fornecedor:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_fornecedores():
        conn = Fornecedor.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fornecedores ORDER BY id DESC")
        fornecedores = cursor.fetchall()
        conn.close()
        return fornecedores

    @staticmethod
    def get_fornecedor(id):
        conn = Fornecedor.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fornecedores WHERE id = %s", (id,))
        fornecedor = cursor.fetchone()
        conn.close()
        return fornecedor

    @staticmethod
    def criar_fornecedor(nome_empresa, cnpj, email=None, telefone=None, endereco=None):
        conn = Fornecedor.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fornecedores (nome_empresa, cnpj, email, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome_empresa, cnpj, email, telefone, endereco))
        conn.commit()
        conn.close()

    @staticmethod
    def atualizar_fornecedor(id, nome_empresa, cnpj, email=None, telefone=None, endereco=None):
        conn = Fornecedor.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fornecedores
            SET nome_empresa=%s, cnpj=%s, email=%s, telefone=%s, endereco=%s
            WHERE id=%s
        """, (nome_empresa, cnpj, email, telefone, endereco, id))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_fornecedor(id):
        conn = Fornecedor.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fornecedores WHERE id=%s", (id,))
        conn.commit()
        conn.close()
