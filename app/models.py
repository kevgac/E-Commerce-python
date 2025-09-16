from app import db  # Importez uniquement `db`, sans bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Indique si l'utilisateur est un admin

    # Méthode pour définir un mot de passe sans hashage
    def set_password(self, password):
        self.password_hash = password  # Aucun hashage (pas de sécurité ‒ pour démo uniquement)

    # Méthode pour vérifier le mot de passe sans hashage
    def check_password(self, password):
        return self.password_hash == password

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)  # ID unique pour chaque produit
    name = db.Column(db.String(100), nullable=False)  # Nom du produit
    description = db.Column(db.Text, nullable=True)  # Description détaillée
    price = db.Column(db.Float, nullable=False)  # Prix
    image = db.Column(db.String(300), nullable=True)  # URL de l'image du produit (optionnel)
    stock = db.Column(db.Integer, default=0)  # Quantité en stock

    def __repr__(self):
        return f"<Produit {self.name}>"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', secondary='order_product', backref='orders')

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)