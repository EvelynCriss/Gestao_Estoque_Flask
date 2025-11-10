import mysql.connector
from config import db_config

def inicia_bd():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão com o BD: {err}")
        return None

# Modelo para representar um fornecedor
class Fornecedor:
    @staticmethod
    def get_fornecedores():
        fornecedores = []
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM gestao_estoque.fornecedores")
                fornecedores = cursor.fetchall()
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao buscar fornecedores: {err}")
            finally:
                cursor.close()
                conn.close()
        return fornecedores

# Criação de um novo fornecedor
    @staticmethod
    def criar_fornecedor(nome_empresa, cnpj, email, telefone, endereco):
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO gestao_estoque.fornecedores (nome_empresa, cnpj, email, telefone, endereco) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (nome_empresa, cnpj, email, telefone, endereco))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao criar fornecedor: {err}")
                conn.rollback() # Desfaz a transação em caso de erro
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def get_fornecedor(id):
        fornecedor = None
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM gestao_estoque.fornecedores WHERE id = %s", (id,))
                fornecedor = cursor.fetchone()
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao buscar fornecedor: {err}")
            finally:
                cursor.close()
                conn.close()
        return fornecedor

    @staticmethod
    def atualizar_fornecedor(id, nome_empresa, cnpj, email, telefone, endereco):
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor()
            try:
                query = "UPDATE gestao_estoque.fornecedores SET nome_empresa=%s, cnpj=%s, email=%s, telefone=%s, endereco=%s WHERE id=%s"
                cursor.execute(query, (nome_empresa, cnpj, email, telefone, endereco, id))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar fornecedor: {err}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def deletar_fornecedor(id):
        conn = inicia_bd()
        if conn:
            cursor = conn.cursor()
            try:
                query = "DELETE FROM gestao_estoque.fornecedores WHERE id = %s"
                cursor.execute(query, (id,))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao deletar fornecedor: {err}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()