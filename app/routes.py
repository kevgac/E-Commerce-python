from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required
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
# @main.route('/add', methods=['GET', 'POST'])
# @login_required  # Accessible uniquement si l'utilisateur est connecté
# def add_product():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         price = float(request.form['price'])
#         image = request.form['image']
#         stock = int(request.form['stock'])

#         # Ajouter le produit dans la base
#         new_product = Product(name=name, description=description, price=price, image=image, stock=stock)
#         db.session.add(new_product)
#         db.session.commit()

#         flash('Produit ajouté avec succès !', 'success')
#         return redirect(url_for('main.home'))

#     return render_template('add_product.html')

# @main.route('/delete/<int:product_id>', methods=['POST'])
# def delete_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     db.session.delete(product)
#     db.session.commit()
#     flash('Produit supprimé avec succès !', 'success')
#     return redirect(url_for('main.home'))


@main.route('/product/<int:product_id>', methods=['GET'])
def view_product(product_id):
    # Récupérer le produit par son ID
    product = Product.query.get_or_404(product_id)  # Retourne 404 si le produit n'existe pas

    # Rendre un template avec les détails du produit
    return render_template('view_product.html', product=product)


@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Vérifier si le panier existe dans la session, sinon l'initialiser.
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    # Récupérer le produit à partir de la base de données
    product = Product.query.get_or_404(product_id)

    # Vérifier si le produit est déjà dans le panier
    if str(product_id) in cart:
        # Si le produit existe déjà, augmenter la quantité
        cart[str(product_id)]['quantity'] += 1
    else:
        # Si le produit n'est pas dans le panier, l'ajouter
        cart[str(product_id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1
        }

    # Mettre à jour la session
    session['cart'] = cart
    flash(f"Le produit '{product.name}' a été ajouté à votre panier.", 'success')

    # Rediriger vers la page d'accueil ou une autre page
    return redirect(url_for('main.home'))

@main.route('/cart')
def view_cart():
    # Récupérer le panier depuis la session
    cart = session.get('cart', {})
    
    # Calculer le total du panier
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    return render_template('view_cart.html', cart=cart, total=total)


@main.route('/remove_from_cart/<int:product_id>', methods=['GET', 'POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})

    # Supprimer le produit du panier s'il existe
    if str(product_id) in cart:
        del cart[str(product_id)]
        flash('Produit supprimé du panier.', 'success')
    
    # Mettre à jour la session
    session['cart'] = cart

    return redirect(url_for('main.view_cart'))


@main.route('/admin')

@main.route('/make_admin/<int:user_id>', methods=['GET'])
@login_required
def make_admin(user_id):
    # Vérification du statut admin de l'utilisateur connecté
    if not current_user.is_admin:
        flash("Accès refusé : Seuls les administrateurs peuvent effectuer cette action.", 'danger')
        return redirect(url_for('main.home'))

    # Mettre à jour un utilisateur spécifique
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()

    return f"L'utilisateur {user.username} est maintenant un administrateur."

@login_required
def admin_dashboard():
    # Vérifier si l'utilisateur connecté est admin
    if not current_user.is_admin:
        flash("Accès refusé : cette page est réservée aux administrateurs.", 'danger')
        return redirect(url_for('main.home'))
    
    # Récupérer les produits pour les afficher dans le tableau de bord admin
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@main.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Accès refusé : cette page est réservée aux administrateurs.", 'danger')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        image = request.form['image']

        # Créer un nouveau produit
        product = Product(name=name, description=description, price=price, stock=int(stock), image=image)
        db.session.add(product)
        db.session.commit()
        
        flash("Produit ajouté avec succès !", 'success')
        return redirect(url_for('main.admin_dashboard'))

    return render_template('add_product.html')

@main.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("Accès refusé.", 'danger')
        return redirect(url_for('main.home'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    flash("Produit supprimé avec succès !", 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash("Accès refusé.", 'danger')
        return redirect(url_for('main.home'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.image = request.form['image']

        db.session.commit()
        flash("Produit modifié avec succès !", 'success')
        return redirect(url_for('main.admin_dashboard'))

    return render_template('edit_product.html', product=product)