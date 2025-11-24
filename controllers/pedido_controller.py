from flask import render_template, request, redirect, url_for, session
from models.pedido import Pedido
from models.fornecedor import Fornecedor
from models.produto import Produto
from datetime import datetime

def configura_rotas(app):

    @app.route('/pedidos')
    def listar_pedidos():
        pedidos = Pedido.get_pedidos()
        
        for p in pedidos:
            # Formata data
            dp = p.get('data_pedido')
            if dp:
                try:
                    if isinstance(dp, datetime):
                        p['data_pedido'] = dp.strftime('%d/%m/%Y')
                    else:
                        s = str(dp)
                        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                            try:
                                parsed = datetime.strptime(s[:19], fmt) if len(s) >= 19 else datetime.strptime(s, fmt)
                                p['data_pedido'] = parsed.strftime('%d/%m/%Y')
                                break
                            except Exception:
                                continue
                except Exception:
                    p['data_pedido'] = str(dp)

            # Formata valor total
            vt = p.get('valor_total')
            if vt is None:
                p['valor_total'] = '-'
            else:
                try:
                    num = float(vt)
                    s = f"{num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    p['valor_total'] = f"R$ {s}"
                except Exception:
                    p['valor_total'] = str(vt)

        return render_template('pedidos/home.html', pedidos=pedidos)

    @app.route('/pedidos/add', methods=['GET', 'POST'])
    def add_pedido():
        if request.method == 'POST':
            fornecedor_id = request.form.get('fornecedor_id')
            data_pedido = request.form.get('data_pedido')
            status = request.form.get('status')
            usuario_id = session.get('id')

            pedido_id = Pedido.criar_pedido(fornecedor_id, usuario_id, data_pedido, status, None)

            produto_ids = request.form.getlist('produto_id[]')
            quantidades = request.form.getlist('quantidade[]')
            total_calc = 0

            for i, pid in enumerate(produto_ids):
                if not pid:
                    continue
                quantidade = int(quantidades[i]) if i < len(quantidades) and quantidades[i] else 0
                prod = Produto.get_produto(pid)
                preco_unit = float(prod['preco']) if prod and prod.get('preco') is not None else 0.0

                if quantidade > 0:
                    Pedido.add_item(pedido_id, pid, quantidade, preco_unit)
                    total_calc += quantidade * preco_unit

            Pedido.atualizar_pedido(pedido_id, fornecedor_id, data_pedido, status, total_calc)
            return redirect(url_for('listar_pedidos'))

        fornecedores = Fornecedor.get_fornecedores()
        produtos = Produto.get_produtos()
        return render_template('pedidos/add.html', fornecedores=fornecedores, produtos=produtos)

    @app.route('/pedidos/edit/<int:id>', methods=['GET', 'POST'])
    def edit_pedido(id):
        pedido = Pedido.get_pedido(id)

        # Formata data para input
        if pedido and pedido.get('data_pedido'):
            dp = pedido.get('data_pedido')
            try:
                if isinstance(dp, str):
                    s = dp
                    if len(s) >= 19:
                        parsed = datetime.strptime(s[:19], '%Y-%m-%d %H:%M:%S')
                    else:
                        parsed = datetime.strptime(s[:10], '%Y-%m-%d')
                    pedido['data_pedido'] = parsed.strftime('%Y-%m-%d')
                elif isinstance(dp, datetime):
                    pedido['data_pedido'] = dp.strftime('%Y-%m-%d')
            except Exception:
                pedido['data_pedido'] = str(dp)[:10]

        if request.method == 'POST':
            fornecedor_id = request.form.get('fornecedor_id')
            data_pedido = request.form.get('data_pedido')
            status = request.form.get('status')

            Pedido.deletar_itens_por_pedido(id)

            produto_ids = request.form.getlist('produto_id[]')
            quantidades = request.form.getlist('quantidade[]')
            total_calc = 0

            for i, pid in enumerate(produto_ids):
                if not pid:
                    continue
                quantidade = int(quantidades[i]) if i < len(quantidades) and quantidades[i] else 0
                prod = Produto.get_produto(pid)
                preco_unit = float(prod['preco']) if prod and prod.get('preco') is not None else 0.0

                if quantidade > 0:
                    Pedido.add_item(id, pid, quantidade, preco_unit)
                    total_calc += quantidade * preco_unit

            Pedido.atualizar_pedido(id, fornecedor_id, data_pedido, status, total_calc)
            return redirect(url_for('listar_pedidos'))

        fornecedores = Fornecedor.get_fornecedores()
        produtos = Produto.get_produtos()
        itens = Pedido.get_itens_por_pedido(id)

        return render_template('pedidos/edit.html', pedido=pedido, fornecedores=fornecedores, produtos=produtos, itens=itens)

    @app.route('/pedidos/delete/<int:id>')
    def delete_pedido(id):
        Pedido.deletar_pedido(id)
        return redirect(url_for('listar_pedidos'))
