from flask import render_template, request, redirect, url_for, flash, session
from models.pedido import Pedido
from models.fornecedor import Fornecedor
from datetime import datetime


def configura_rotas(app):
    @app.route('/pedidos')
    def listar_pedidos():
        pedidos = Pedido.get_pedidos()
        return render_template('pedidos/home.html', pedidos=pedidos)



    @app.route('/pedidos/add', methods=['GET', 'POST'])
    def add_pedido():
        if request.method == 'POST':
            fornecedor_id = request.form.get('fornecedor_id')
            data_pedido = request.form.get('data_pedido')
            status = request.form.get('status')
            valor_total = request.form.get('valor_total')
            usuario_id = session.get('id')

            
            if not fornecedor_id or not usuario_id:
                flash("Fornecedor é obrigatório!", "danger")
                return redirect(url_for('add_pedido'))

           
            Pedido.criar_pedido(fornecedor_id, usuario_id, data_pedido, status, valor_total)
            flash("Pedido cadastrado com sucesso!", "success")
            return redirect(url_for('listar_pedidos'))

        fornecedores = Fornecedor.get_fornecedores()
        return render_template('pedidos/add.html', fornecedores=fornecedores)



    @app.route('/pedidos/edit/<int:id>', methods=['GET', 'POST'])
    def edit_pedido(id):
        pedido = Pedido.get_pedido(id)

        if request.method == 'POST':
            fornecedor_id = request.form.get('fornecedor_id')
            data_pedido = request.form.get('data_pedido')
            status = request.form.get('status')
            valor_total = request.form.get('valor_total')

            Pedido.atualizar_pedido(id, fornecedor_id, data_pedido, status, valor_total)
            flash("Pedido atualizado com sucesso!", "success")
            return redirect(url_for('listar_pedidos'))


        if pedido and pedido.get('data_pedido'):
            if isinstance(pedido['data_pedido'], datetime):
                pedido['data_pedido'] = pedido['data_pedido'].strftime('%Y-%m-%d')
            else:
                pedido['data_pedido'] = str(pedido['data_pedido'])[:10]

        fornecedores = Fornecedor.get_fornecedores()
        return render_template('pedidos/edit.html', pedido=pedido, fornecedores=fornecedores)



    @app.route('/pedidos/delete/<int:id>')
    def delete_pedido(id):
        Pedido.deletar_pedido(id)
        flash("Pedido deletado com sucesso!", "success")
        return redirect(url_for('listar_pedidos'))

