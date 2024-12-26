import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações base"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao-nao-usar-em-producao'
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Sistema
    APP_NAME = os.environ.get('APP_NAME', 'Controle do Motorista')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@brsinformatica.com.br')
    DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'pt-BR')
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 10))
    
    # Backup
    BACKUP_ENABLED = os.environ.get('BACKUP_ENABLED', 'True').lower() in ['true', 'on', '1']
    BACKUP_DIR = os.environ.get('BACKUP_DIR', 'backups')
    MAX_BACKUP_FILES = int(os.environ.get('MAX_BACKUP_FILES', 5))
    
    # Segurança
    SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 30))
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=SESSION_LIFETIME)
    PASSWORD_MIN_LENGTH = int(os.environ.get('PASSWORD_MIN_LENGTH', 6))
    MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', 3))
    LOCKOUT_TIME = int(os.environ.get('LOCKOUT_TIME', 300))  # em segundos

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Em produção, certifique-se de definir uma chave secreta forte
    SECRET_KEY = os.environ.get('SECRET_KEY') or None
    if not SECRET_KEY:
        raise ValueError("Nenhuma chave secreta definida em produção!")
    
    # Configurações adicionais de segurança para produção
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

class TestingConfig(Config):
    """Configurações de teste"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Dicionário com as configurações disponíveis
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

# Configurações de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    },
    'loggers': {
        'werkzeug': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'sqlalchemy': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': False
        },
        'error_logger': {
            'level': 'ERROR',
            'handlers': ['error_file'],
            'propagate': False
        }
    }
}

# Configurações de cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}

# Configurações de upload de arquivos
UPLOAD_CONFIG = {
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif', 'pdf'},
    'UPLOAD_FOLDER': 'uploads'
}

# Configurações de paginação
PAGINATION_CONFIG = {
    'PER_PAGE': ITEMS_PER_PAGE,
    'CSS_FRAMEWORK': 'bootstrap5',
    'LINK_SIZE': '3',
    'SHOW_SINGLE_PAGE': False,
    'DISPLAY_MSG': 'Mostrando {start} a {end} de {total} registros'
}

# Configurações de API
API_CONFIG = {
    'VERSION': '1.0',
    'TITLE': APP_NAME,
    'DESCRIPTION': 'API do sistema de controle de motoristas',
    'CONTACT_EMAIL': ADMIN_EMAIL,
    'RATE_LIMIT': '100 per minute'
} 