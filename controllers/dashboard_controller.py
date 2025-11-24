from flask import render_template, redirect, url_for, session, send_file
import mysql.connector
from config import db_config
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import requests

def configura_rotas(app):
    # === DASHBOARD ===
    @app.route('/dashboard')
    def dashboard():
        if 'loggedin' not in session:
            return redirect(url_for('login'))

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

    # Estatísticas
        cursor.execute("SELECT COUNT(*) AS total FROM produtos")
        total_produtos = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM pedidos WHERE status = 'aprovado'")
        pedidos_aprovados = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM pedidos WHERE status = 'pendente'")
        pedidos_pendentes = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM produtos
            WHERE estoque_minimo > 0
        """)
        estoque_baixo = cursor.fetchone()['total']

        conn.close()

        stats = {
            'total_produtos': total_produtos,
            'pedidos_aprovados': pedidos_aprovados,
            'pedidos_pendentes': pedidos_pendentes,
            'estoque_baixo': estoque_baixo
        }

        # ===== API de Cotação (AwesomeAPI) =====
        try:
            response = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL', timeout=5)
            data = response.json()
            cotacao_usd = float(data['USDBRL']['bid'])
        except Exception as e:
            cotacao_usd = f"Erro ao obter cotação ({e})"

        return render_template('dashboard.html', stats=stats, cotacao_usd=cotacao_usd)


    # === DOWNLOAD DE RELATÓRIO ===
    @app.route('/baixar_relatorio_excel')
    def baixar_relatorio_excel():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nome, categoria, unidade, preco, estoque_minimo FROM produtos")
        produtos = cursor.fetchall()
        conn.close()

        wb = Workbook()
        ws = wb.active
        ws.title = "Produtos"

        headers = ['ID', 'Nome', 'Categoria', 'Unidade', 'Preço', 'Estoque Mínimo']
        ws.append(headers)

        for col in range(1, len(headers)+1):
            cell = ws.cell(row=1, column=col)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

        for produto in produtos:
            ws.append([
                produto['id'],
                produto['nome'],
                produto['categoria'],
                produto['unidade'],
                float(produto['preco']),
                produto['estoque_minimo']
            ])

        for column_cells in ws.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 2

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="relatorio_produtos.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
