from flask import Flask, render_template
from controllers.fornecedor_controller import fornecedores_bp

app = Flask(__name__, template_folder='views/templates')



# Registrar o Blueprint
app.register_blueprint(fornecedores_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run(debug=True)


