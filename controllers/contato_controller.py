from flask import render_template, request
from models.contato import salvar_mensagem

def configura_rotas(app):

    @app.route('/contato', methods=['GET'])
    def contato_form():
        return render_template('contato.html')

    @app.route('/contato', methods=['POST'])
    def contato_enviar():
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        salvar_mensagem(nome, email, mensagem)

        return render_template('contato.html', mensagem="Mensagem enviada com sucesso!")
