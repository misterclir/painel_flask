from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from auth.utils import authenticate_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = authenticate_user(username, password)
        if user:
            session['user'] = user
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuário ou senha incorretos', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você foi desconectado', 'info')
    return redirect(url_for('auth.login'))