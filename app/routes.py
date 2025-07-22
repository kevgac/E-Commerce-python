from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User

# Définir un Blueprint pour les routes générales
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Exemple simplifié d'authentification
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # Attention : utilisez un chiffrement sécurisé !
        user = User.query.filter_by(username=username).first()
        if user and user.password_hash == password:
            login_user(user)  # Connecter l'utilisateur
            return redirect(url_for('main.home'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')