from flask import render_template, request, redirect, url_for, flash
from models.fornecedor import Fornecedor


def configura_rotas(app):
# ===== Página inicial (lista de fornecedores) =====
    @app.route('/fornecedores')
    def listar_fornecedores():
        fornecedores = Fornecedor.get_fornecedores()
        return render_template('fornecedores/home.html', fornecedores=fornecedores)


# ===== Adicionar fornecedor =====
    @app.route('/fornecedores/add', methods=['GET', 'POST'])
    def add_fornecedor():
        if request.method == 'POST':
            nome_empresa = request.form.get('nome_empresa')
            cnpj = request.form.get('cnpj')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            endereco = request.form.get('endereco')

            # Validação dos campos obrigatórios
            if not nome_empresa or not cnpj:
                flash("Nome da empresa e CNPJ são obrigatórios!", "danger")
                return redirect(url_for('add_fornecedor'))

            # Se passou na validação, cria fornecedor
            Fornecedor.criar_fornecedor(nome_empresa, cnpj, email, telefone, endereco)
            flash("Fornecedor cadastrado com sucesso!", "success")
            return redirect(url_for('listar_fornecedores'))

        return render_template('fornecedores/add.html')


# ===== Editar fornecedor =====
    @app.route('/fornecedores/edit/<int:id>', methods=['GET', 'POST'])
    def edit_fornecedor(id):
        fornecedor = Fornecedor.get_fornecedor(id)

        if request.method == 'POST':
            nome_empresa = request.form['nome_empresa']
            cnpj = request.form['cnpj']
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            endereco = request.form.get('endereco')

            Fornecedor.atualizar_fornecedor(id, nome_empresa, cnpj, email, telefone, endereco)
            flash("Fornecedor atualizado com sucesso!", "success")
            return redirect(url_for('home'))

        return render_template('fornecedores/edit.html', fornecedor=fornecedor)


    # ===== Deletar fornecedor =====
    @app.route('/fornecedores/delete/<int:id>')
    def delete_fornecedor(id):
        Fornecedor.deletar_fornecedor(id)
        flash("Fornecedor deletado com sucesso!", "success")
        return redirect(url_for('home'))
