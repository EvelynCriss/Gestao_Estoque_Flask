from flask import Flask, render_template
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
from controllers import produto_controller

# Registra as rotas diretamente na aplicação
login_controller.configura_rotas(app)
fornecedor_controller.configura_rotas(app)
produto_controller.configura_rotas(app)

if __name__ == '__main__':
    app.run(debug=True)
