from flask import Blueprint, render_template, request, redirect, url_for
from models.fornecedor import Fornecedor

# Cria o Blueprint para fornecedores
fornecedores_bp = Blueprint('fornecedores', __name__, url_prefix='/fornecedores')

# Página inicial (lista de fornecedores)
@fornecedores_bp.route('/')
def home():
    fornecedores = Fornecedor.get_fornecedores()
    return render_template('fornecedores/home.html', fornecedores=fornecedores)

# Adicionar fornecedor
@fornecedores_bp.route('/add', methods=['GET', 'POST'], endpoint='add')
def add():
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        cnpj = request.form['cnpj']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        Fornecedor.criar_fornecedor(nome_empresa, cnpj, email, telefone, endereco)
        return redirect(url_for('fornecedores.home'))
    return render_template('fornecedores/add.html')

# Editar fornecedor
@fornecedores_bp.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    fornecedor = Fornecedor.get_fornecedor(id)
    if request.method == 'POST':
        nome_empresa = request.form['nome_empresa']
        cnpj = request.form['cnpj']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        Fornecedor.atualizar_fornecedor(id, nome_empresa, cnpj, email, telefone, endereco)
        return redirect(url_for('fornecedores.home'))
    return render_template('fornecedores/edit.html', fornecedor=fornecedor)

# Deletar fornecedor
@fornecedores_bp.route('/delete/<int:id>', endpoint='delete')
def delete(id):
    Fornecedor.deletar_fornecedor(id)
    return redirect(url_for('fornecedores.home'))
