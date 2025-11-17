from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
from models.login import Login   


def configura_rotas(app):

    @app.route('/')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg = ''

        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            usuario = Login.get_email(email)

            if usuario and check_password_hash(usuario['senha'], senha):
                session['loggedin'] = True
                session['id'] = usuario['id']
                session['nome'] = usuario['nome']
                return redirect(url_for('home'))
            else:
                msg = 'E-mail ou senha incorretos!'

        return render_template('login/login.html', msg=msg)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        msg = ''

        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')

            # Verifica campos
            if not nome or not email or not senha:
                msg = 'Preencha todos os campos!'
                return render_template('login/registro.html', msg=msg)

            # Email já existe?
            if Login.get_email(email):
                msg = 'Este e-mail já está registrado!'
                return render_template('login/registro.html', msg=msg)

            # Valida email
            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError:
                msg = 'E-mail inválido!'
                return render_template('login/registro.html', msg=msg)

            # Cria usuário
            Login.criar_login_usuario(nome, email, senha)
            flash('Registrado com sucesso! Faça o login.')
            return redirect(url_for('login'))

        return render_template('login/registro.html', msg=msg)

    @app.route('/home')
    def home():
        if 'loggedin' in session:
            return render_template('login/home.html', nome=session['nome'])
        return redirect(url_for('login'))

    @app.route('/perfil')
    def perfil():
        if 'loggedin' in session:
            usuario = Login.get_id(session['id'])
            return render_template('login/perfil.html', usuario=usuario)
        return redirect(url_for('login'))
