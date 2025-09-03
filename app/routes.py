from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, Product
from app import db  # Importer l'instance de `db` déjà définie dans `__init__.py`

# Définir un Blueprint pour les routes générales
main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Récupérer tous les produits de la base
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form.get('username')
        password = request.form.get('password')

        # Rechercher l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Vérification sécurisée
            login_user(user)  # Connecter l'utilisateur avec Flask-Login
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Vérifications simples :
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return redirect(url_for('main.register'))

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Nom d’utilisateur ou e-mail déjà utilisé.', 'danger')
            return redirect(url_for('main.register'))

        # Ajouter un nouvel utilisateur (Attention : sécuriser le mot de passe)
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hashage du mot de passe
        db.session.add(new_user)
        db.session.commit()

        # Connecter automatiquement l'utilisateur après l'inscription
        login_user(new_user)
        flash('Inscription réussie ! Bienvenue, ' + new_user.username, 'success')
        return redirect(url_for('main.home'))

    return render_template('register.html')


@main.route('/logout')
@login_required  # Accessible uniquement si l'utilisateur est connecté
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('main.login'))

# Route pour créer un produit
@main.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.form['image']
        stock = int(request.form['stock'])

        # Ajouter le produit dans la base
        new_product = Product(name=name, description=description, price=price, image=image, stock=stock)
        db.session.add(new_product)
        db.session.commit()

        flash('Produit ajouté avec succès !', 'success')
        return redirect(url_for('main.home'))

    return render_template('add_product.html')

@main.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès !', 'success')
    return redirect(url_for('main.home'))


@main.route('/product/<int:product_id>', methods=['GET'])
def view_product(product_id):
    # Récupérer le produit par son ID
    product = Product.query.get_or_404(product_id)  # Retourne 404 si le produit n'existe pas

    # Rendre un template avec les détails du produit
    return render_template('view_product.html', product=product)