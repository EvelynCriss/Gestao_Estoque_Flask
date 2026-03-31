from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
from models.login import Login   


def configura_rotas(app):

    @app.route('/')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg = ''

        if 'loggedin' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            remember = request.form.get('remember')

            usuario = Login.get_email(email)

            if usuario and check_password_hash(usuario['senha'], senha):
                session['loggedin'] = True
                session['id'] = usuario['id']
                session['nome'] = usuario['nome']
                session['email'] = usuario['email']
                session.permanent = True if remember else False
                
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                msg = 'E-mail ou senha incorretos!'

        return render_template('usuarios/login.html', msg=msg) 

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logout realizado com sucesso!', 'info')
        return redirect(url_for('index'))  
    @app.route('/registro', methods=['GET', 'POST'])
    def registro():
        msg = ''

        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            
            if not nome or not email or not senha:
                msg = 'Preencha todos os campos!'
                return render_template('usuarios/registro.html', msg=msg)

            if Login.get_email(email):
                msg = 'Este e-mail já está registrado!'
                return render_template('usuarios/registro.html', msg=msg)

            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError:
                msg = 'E-mail inválido!'
                return render_template('usuarios/registro.html', msg=msg)

            Login.criar_login_usuario(nome, email, senha)
            flash('Registrado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))

        return render_template('usuarios/registro.html', msg=msg)