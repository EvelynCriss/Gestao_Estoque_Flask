import mysql.connector
from config import db_config

def salvar_mensagem(nome, email, mensagem):
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    sql = """
        INSERT INTO mensagens_contato (nome, email, mensagem)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nome, email, mensagem))
    conexao.commit()

    cursor.close()
    conexao.close()
