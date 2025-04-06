import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-segura'
    SESSION_COOKIE_NAME = 'painel_session'
    USERS = {
        'admin': {'password': 'admin123', 'name': 'Administrador'},
        'user': {'password': 'user123', 'name': 'Usuário Padrão'}
    }
    
    # Configurações para uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'xml'}
    
    # Criar pasta de uploads se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)