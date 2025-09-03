from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_bcrypt import Bcrypt 

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Configurations nécessaires
    app.config['SECRET_KEY'] = '0123456789abcdef'  # Clé secrète pour les sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # Base de données SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactiver les notifications de modifications

    # Initialiser les extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # bcrypt.init_app(app)  # Initialisation de Bcrypt
    login_manager.login_view = 'main.login'  # Vue pour la connexion de l'utilisateur

    with app.app_context():
        # Importer les modèles et les blueprints APRES initialisation pour éviter les importations circulaires
        from .models import User  # Import des modèles après initialisation de l'extension db
        from .routes import main  # Blueprint des routes
        app.register_blueprint(main)

    return app

# Définition de la fonction user_loader pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Importer User ici pour éviter les imports circulaires
    return User.query.get(int(user_id))  # Charge l'utilisateur en fonction de l'ID