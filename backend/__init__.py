import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail

db = SQLAlchemy()
session = Session()
mail = Mail()

# Load environment variables from the .env file
load_dotenv()

def create_app():
    # app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    app = Flask(__name__)    
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://bookshop.up.railway.app"}})
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE')
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=int(os.getenv('PSLT')))
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #! Allow HTTP requests, not HTTPS

    db.init_app(app)
    session.init_app(app)
    mail.init_app(app)

    from .views.login import login as login_blueprint
    from .views.register import register as register_blueprint
    from .views.logout import logout as logout_blueprint
    from .views.dashboard import dashboard as dashboard_blueprint
    from .views.home import home as home_blueprint
    from .views.cart import cart as cart_blueprint
    from .views.book import book as book_blueprint
    from .views.category import category as category_blueprint
    from .views.cart_items import cart_items as cart_items_blueprint
    from .views.shop import shop as shop_blueprint
    from .views.wishlist import wishlist as wishlist_blueprint
    from .views.details import details as details_blueprint
    from .views.reset_password import reset as reset_blueprint
    from .views.admin import admin as admin_blueprint

    app.register_blueprint(login_blueprint, url_prefix='/')
    app.register_blueprint(register_blueprint, url_prefix='/')
    app.register_blueprint(logout_blueprint, url_prefix='/')
    app.register_blueprint(dashboard_blueprint, url_prefix='/')
    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(cart_blueprint, url_prefix='/')
    app.register_blueprint(book_blueprint, url_prefix='/')
    app.register_blueprint(category_blueprint, url_prefix='/')
    app.register_blueprint(cart_items_blueprint, url_prefix='/')
    app.register_blueprint(shop_blueprint, url_prefix='/')
    app.register_blueprint(wishlist_blueprint, url_prefix='/')
    app.register_blueprint(details_blueprint, url_prefix='/')
    app.register_blueprint(reset_blueprint, url_prefix='/')
    app.register_blueprint(admin_blueprint, url_prefix='/')


    
    # # Serve React's static files from the build folder
    # @app.route('/')
    # @app.route('/<path:path>')
    # def serve_react(path=None):
    #     if path is None or path == 'index.html':
    #         return send_from_directory(app.static_folder, 'index.html')
    #     else:
    #         # For everything else, serve the index.html
    #         if path.startswith('static/') or '.' in path:
    #             # Serve static files directly (e.g., images, css, js)
    #             return send_from_directory(app.static_folder, path)
    #         else:
    #             return send_from_directory(app.static_folder, 'index.html')
    
    with app.app_context():
        db.create_all()
        
    return app
