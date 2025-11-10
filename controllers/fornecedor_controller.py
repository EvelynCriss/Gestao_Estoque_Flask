from flask import render_template, request, redirect, url_for
from models.fornecedor import Fornecedor

def configure_routes(app):

    @app.route('/')
    def fornecedores_home():
        fornecedores = Fornecedor.get_fornecedores()
        return render_template('home.html', fornecedores=fornecedores)

    # Rota que exibe o formulário para adição de fornecedor
    @app.route('/fornecedores/fornecedores_add', methods=['GET', 'POST'])
    def fornecedores_add():
        if request.method == 'POST':
            nome_empresa = request.form['nome_empresa']
            cnpj = request.form['cnpj']
            email = request.form['email']
            telefone = request.form['telefone']
            endereco = request.form['endereco']
            Fornecedor.criar_fornecedor(nome_empresa, cnpj, email, telefone, endereco)
            return redirect(url_for('fornecedores_home'))
        return render_template('fornecedores_add.html')  # formulário para adicionar

    # Rota para edição de um fornecedor existente
    @app.route('/fornecedores/edit/<int:id>', methods=['GET', 'POST'])
    def fornecedores_edit(id):
        fornecedor = Fornecedor.get_fornecedor(id)
        if request.method == 'POST':
            nome_empresa = request.form['nome_empresa']
            cnpj = request.form['cnpj']
            email = request.form['email']
            telefone = request.form['telefone']
            endereco = request.form['endereco']
            Fornecedor.atualizar_fornecedor(id, nome_empresa, cnpj, email, telefone, endereco)
            return redirect(url_for('fornecedores_home'))
        return render_template('fornecedores_edit.html', fornecedor=fornecedor)

    # Rota para deletar um fornecedor
    @app.route('/fornecedores/delete/<int:id>')
    def fornecedores_delete(id):
        Fornecedor.deletar_fornecedor(id)
        return redirect(url_for('fornecedores_home'))