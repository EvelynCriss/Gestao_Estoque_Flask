from flask import render_template, request, redirect, url_for, flash
from models.produto import Produto


def configura_rotas(app):
# lista de produtos
    @app.route('/produtos')
    def listar_produtos():
        produtos = Produto.get_produtos()
        return render_template('produtos/home.html', produtos=produtos)


# ===== Adicionar produto =====
    @app.route('/produtos/add', methods=['GET', 'POST'])
    def add_produto():
        if request.method == 'POST':
            nome = request.form.get('nome')
            preco = request.form.get('preco')
            # converter o preço para formato float
            preco = preco.replace('.', '').replace(',', '.')

            estoque_minimo = request.form.get('estoque_minimo')
            categoria = request.form.get('categoria')
            unidade = request.form.get('unidade')

            # Validação dos campos obrigatórios
            if not nome or not preco or not estoque_minimo:
                flash("Nome, preco e estoque são obrigatórios!", "danger")
                return redirect(url_for('add_produto'))

            # Se passou na validação, cria produto
            Produto.criar_produto(nome, preco, estoque_minimo, categoria, unidade)
            flash("Produto cadastrado com sucesso!", "success")
            return redirect(url_for('listar_produtos'))

        return render_template('produtos/add.html')


# ===== Editar produto =====
    @app.route('/produtos/edit/<int:id>', methods=['GET', 'POST'])
    def edit_produto(id):
        produto = Produto.get_produto(id)

        if request.method == 'POST':
            nome = request.form.get('nome')
            preco = request.form.get('preco')
            # converter o preço para formato float
            preco = preco.replace('.', '').replace(',', '.')
            estoque_minimo = request.form.get('estoque_minimo')
            categoria = request.form.get('categoria')
            unidade = request.form.get('unidade')

            Produto.atualizar_produto(id, nome, preco, estoque_minimo, categoria, unidade)
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for('listar_produtos'))

        return render_template('produtos/edit.html', produto=produto)


    # ===== Deletar produto =====
    @app.route('/produtos/delete/<int:id>')
    def delete_produto(id):
        Produto.deletar_produto(id)
        flash("Produto deletado com sucesso!", "success")
        return redirect(url_for('listar_produtos'))