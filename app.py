from flask import Flask, render_template, session, redirect, url_for
from config import SECRET_KEY, db_config

app = Flask(
    __name__,
    static_folder='views/static',
    template_folder='views/templates'
)
app.secret_key = SECRET_KEY


# ROTAS PÚBLICAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


# Importa e os controllers
from controllers import login_controller
from controllers import fornecedor_controller
from controllers import pedido_controller
from controllers import produto_controller

# Registra as rotas diretamente na aplicação
login_controller.configura_rotas(app)
fornecedor_controller.configura_rotas(app)
pedido_controller.configura_rotas(app)
produto_controller.configura_rotas(app)


#
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        # Aqui você pode buscar dados do banco para exibir no dashboard
        stats = {
            'total_produtos': 245,
            'pedidos_concluidos': 87,
            'pedidos_pendentes': 12,
            'estoque_baixo': 8
        }
        return render_template('dashboard.html', stats=stats, nome=session['nome'])
    return redirect(url_for('login'))



# ===== TRATAMENTO DE ERROS =====

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
