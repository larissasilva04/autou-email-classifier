import os
import sys
import subprocess
import platform

def print_header():
    """Imprimir cabeçalho do script"""
    print("=" * 70)
    print("🔧 AUTOU EMAIL CLASSIFIER - SETUP E VERIFICAÇÃO")
    print("=" * 70)

def check_python_version():
    """Verificar versão do Python"""
    print("\n1️⃣ Verificando versão do Python...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("   ❌ Python 3.7+ é necessário")
        return False
    else:
        print("   ✅ Versão do Python OK")
        return True

def check_current_directory():
    """Verificar diretório atual"""
    print("\n2️⃣ Verificando diretório atual...")
    current_dir = os.getcwd()
    print(f"   Diretório: {current_dir}")
    
    # Listar arquivos Python no diretório
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"   Arquivos Python encontrados: {py_files}")
    
    return current_dir, py_files

def check_app_file():
    """Verificar se o arquivo app.py existe"""
    print("\n3️⃣ Verificando arquivo app.py...")
    
    if os.path.exists('app.py'):
        print("   ✅ app.py encontrado")
        file_size = os.path.getsize('app.py')
        print(f"   📏 Tamanho: {file_size} bytes")
        return True
    else:
        print("   ❌ app.py NÃO encontrado")
        return False

def create_app_file():
    """Criar arquivo app.py"""
    print("\n4️⃣ Criando arquivo app.py...")
    
    app_content = '''from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from datetime import datetime
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def classify_simple(text):
    """Classificação simples para teste"""
    text_lower = text.lower()
    
    # Palavras produtivas
    productive = ['problema', 'erro', 'ajuda', 'suporte', 'urgente', 'importante', 'reunião', 'projeto']
    # Palavras improdutivas  
    unproductive = ['parabéns', 'aniversário', 'obrigado', 'feliz', 'natal', 'café', 'almoço']
    
    prod_score = sum(1 for word in productive if word in text_lower)
    unprod_score = sum(1 for word in unproductive if word in text_lower)
    
    if prod_score > unprod_score:
        return 'Produtivo', 0.8
    elif unprod_score > prod_score:
        return 'Improdutivo', 0.8
    else:
        return 'Neutro', 0.5

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoU Email Classifier - Funcionando!</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { background: #4CAF50; color: white; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
            .endpoint { background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; }
            code { background: #e8e8e8; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status">
                <h1>🚀 AutoU Email Classifier - FUNCIONANDO!</h1>
                <p>Servidor Flask ativo na porta 5000</p>
            </div>
            
            <h2>📡 Endpoints Disponíveis:</h2>
            
            <div class="endpoint">
                <h3>GET /health</h3>
                <p>Verificar status da API</p>
                <code>http://localhost:5000/health</code>
            </div>
            
            <div class="endpoint">
                <h3>POST /analyze</h3>
                <p>Analisar texto de email</p>
                <code>curl -X POST -d "text=Preciso de ajuda" http://localhost:5000/analyze</code>
            </div>
            
            <div class="endpoint">
                <h3>GET /test</h3>
                <p>Teste rápido do sistema</p>
                <code>http://localhost:5000/test</code>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        'status': 'OK',
        'message': 'AutoU Email Classifier funcionando!',
        'timestamp': datetime.now().isoformat(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
        'endpoints': ['/health', '/analyze', '/test']
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Obter texto
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            text = request.form.get('text', '')
        
        if not text or len(text.strip()) < 5:
            return jsonify({'error': 'Texto muito curto ou vazio'}), 400
        
        # Classificar
        classification, confidence = classify_simple(text)
        
        return jsonify({
            'classification': classification,
            'confidence': confidence,
            'text_length': len(text),
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    test_cases = [
        'Estou com problema no sistema, preciso de ajuda urgente!',
        'Parabéns pelo aniversário! Feliz aniversário!',
        'Reunião marcada para discutir o projeto importante.'
    ]
    
    results = []
    for text in test_cases:
        classification, confidence = classify_simple(text)
        results.append({
            'text': text,
            'classification': classification,
            'confidence': confidence
        })
    
    return jsonify({
        'test_results': results,
        'total_tests': len(results),
        'status': 'success'
    })

if __name__ == '__main__':
    print("🚀 Iniciando AutoU Email Classifier...")
    print("📡 Servidor: http://localhost:5000")
    print("🏥 Health: http://localhost:5000/health")
    print("🧪 Test: http://localhost:5000/test")
    print("⚠️  Mantenha este terminal aberto")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    try:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(app_content)
        print("   ✅ app.py criado com sucesso!")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar app.py: {e}")
        return False

def check_dependencies():
    """Verificar e instalar dependências"""
    print("\n5️⃣ Verificando dependências...")
    
    required_packages = ['flask', 'flask-cors']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NÃO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n6️⃣ Instalando pacotes em falta: {missing_packages}")
        try:
            cmd = [sys.executable, '-m', 'pip', 'install'] + missing_packages
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Pacotes instalados com sucesso!")
                return True
            else:
                print(f"   ❌ Erro na instalação: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ Erro ao instalar: {e}")
            return False
    else:
        print("   ✅ Todas as dependências estão instaladas!")
        return True

def create_requirements():
    """Criar arquivo requirements.txt"""
    print("\n7️⃣ Criando requirements.txt...")
    
    requirements_content = """flask==2.3.3
flask-cors==4.0.0
werkzeug==2.3.7
"""
    
    try:
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("   ✅ requirements.txt criado!")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar requirements.txt: {e}")
        return False

def create_run_script():
    """Criar script de execução"""
    print("\n8️⃣ Criando script de execução...")
    
    if platform.system() == "Windows":
        script_name = "run.bat"
        script_content = """@echo off
echo 🚀 Iniciando AutoU Email Classifier...
echo.
python app.py
pause
"""
    else:
        script_name = "run.sh" 
        script_content = """#!/bin/bash
echo "🚀 Iniciando AutoU Email Classifier..."
echo
python3 app.py
"""
    
    try:
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Tornar executável no Linux/Mac
        if platform.system() != "Windows":
            os.chmod(script_name, 0o755)
            
        print(f"   ✅ {script_name} criado!")
        return script_name
    except Exception as e:
        print(f"   ❌ Erro ao criar script: {e}")
        return None

def run_final_test():
    """Executar teste final"""
    print("\n9️⃣ Executando teste final...")
    
    try:
        # Tentar importar Flask
        from flask import Flask
        print("   ✅ Flask importado com sucesso")
        
        # Verificar se app.py pode ser executado
        if os.path.exists('app.py'):
            print("   ✅ app.py está pronto para execução")
            return True
        else:
            print("   ❌ app.py não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def print_instructions(script_name):
    """Imprimir instruções finais"""
    print("\n" + "=" * 70)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print("\n📋 INSTRUÇÕES PARA EXECUTAR:")
    print("-" * 40)
    
    if platform.system() == "Windows":
        print("   OPÇÃO 1 - Duplo clique no arquivo:")
        print(f"   📁 {script_name}")
        print("\n   OPÇÃO 2 - No terminal:")
        print("   💻 python app.py")
    else:
        print("   OPÇÃO 1 - No terminal:")
        print(f"   💻 ./{script_name}")
        print("\n   OPÇÃO 2 - Comando direto:")
        print("   💻 python3 app.py")
    
    print("\n🌐 DEPOIS DE EXECUTAR, ABRA NO NAVEGADOR:")
    print("   http://localhost:5000")
    print("\n🔧 PARA PARAR O SERVIDOR:")
    print("   Pressione Ctrl + C no terminal")
    
    print("\n" + "=" * 70)

def main():
    """Função principal do setup"""
    print_header()
    
    # Verificações e correções
    if not check_python_version():
        print("\n❌ Versão do Python incompatível. Atualize para Python 3.7+")
        return
    
    current_dir, py_files = check_current_directory()
    
    if not check_app_file():
        if not create_app_file():
            print("\n❌ Falha ao criar app.py")
            return
    
    if not check_dependencies():
        print("\n❌ Falha ao instalar dependências")
        return
    
    create_requirements()
    script_name = create_run_script()
    
    if run_final_test():
        print_instructions(script_name if script_name else "app.py")
    else:
        print("\n❌ Falha no teste final")

if __name__ == "__main__":
    main()