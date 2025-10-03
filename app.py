from flask import Flask
import database as db
from routes.main import main
from routes.posts import posts
from routes.comments import comments
from routes.reactions import reactions
from routes.admin import admin
from routes.stats import stats
from routes.search import search
from routes.profile import profile
from routes.reports import reports
from routes.karma import karma
from routes.auth import auth
from datetime import datetime
import os

def create_app():
    """Função de fábrica para criar a aplicação Flask."""
    
    # Força caminhos absolutos para templates e static
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    
    # Carrega configurações
    app.config.from_pyfile(os.path.join(base_dir, 'config.py'))
    
    # Configuração para sessões
    app.secret_key = os.environ.get('SECRET_KEY', 'entrelinhas_secret_key_dev')
    
    # Inicializa o banco de dados
    db.init_db()
    
    # Registra os blueprints
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(reactions)
    app.register_blueprint(admin)
    app.register_blueprint(stats)
    app.register_blueprint(search)
    app.register_blueprint(profile)
    app.register_blueprint(reports)
    app.register_blueprint(karma)
    app.register_blueprint(auth)
    
    # Contexto global para templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app

# Cria a aplicação
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)