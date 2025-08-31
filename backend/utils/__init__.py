__version__ = "2.0.0"
__author__ = "AutoU Email Classifier Team"

# Importações para facilitar o uso
from .file_reader import FileProcessor
from .text_processor import TextCleaner
from .validators import EmailValidator
from .helpers import generate_protocol, calculate_confidence

# Lista de exports públicos
__all__ = [
    'FileProcessor',
    'TextCleaner', 
    'EmailValidator',
    'generate_protocol',
    'calculate_confidence'
]

# Configurações do módulo
DEFAULT_CONFIDENCE_THRESHOLD = 0.7
SUPPORTED_FILE_TYPES = ['txt', 'pdf', 'eml', 'msg']
MAX_FILE_SIZE_MB = 50

# Funções utilitárias rápidas
def get_version():
    """Retorna a versão do módulo"""
    return __version__

def get_supported_formats():
    """Retorna formatos de arquivo suportados"""
    return SUPPORTED_FILE_TYPES.copy()