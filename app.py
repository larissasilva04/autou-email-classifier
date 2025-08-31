from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

def classify_email(text):
    """Classificação de email"""
    text_lower = text.lower()
    
    # Palavras produtivas
    productive_words = ['problema', 'erro', 'ajuda', 'suporte', 'urgente', 'importante', 'reunião', 'projeto', 'bug', 'falha', 'dúvida', 'solicitação', 'pedido']
    
    # Palavras improdutivas  
    unproductive_words = ['parabéns', 'aniversário', 'obrigado', 'feliz', 'natal', 'café', 'almoço', 'fim de semana', 'férias', 'piada']
    
    prod_score = sum(1 for word in productive_words if word in text_lower)
    unprod_score = sum(1 for word in unproductive_words if word in text_lower)
    
    # Considerar perguntas como produtivas
    question_count = text.count('?')
    if question_count > 0:
        prod_score += question_count
    
    if prod_score > unprod_score:
        return 'Produtivo', min(0.95, 0.6 + (prod_score * 0.1))
    elif unprod_score > prod_score:
        return 'Improdutivo', min(0.95, 0.6 + (unprod_score * 0.1))
    else:
        # Se não há indicadores claros, considerar neutro mas tendendo a produtivo
        return 'Produtivo', 0.5

def generate_response(text, classification):
    """Gerar resposta automática"""
    if classification == 'Produtivo':
        responses = [
            "Obrigado por entrar em contato. Recebemos sua solicitação e retornaremos em até 24 horas úteis.",
            "Agradecemos seu contato. Nossa equipe está analisando sua questão e responderá brevemente.",
            "Sua solicitação foi registrada. Entraremos em contato assim que possível."
        ]
    else:
        responses = [
            "Muito obrigado por sua mensagem! É sempre um prazer receber contato de você.",
            "Agradeço imensamente por pensar em nós. Sua mensagem trouxe alegria ao nosso dia!",
            "Que gentileza sua! Muito obrigado por compartilhar esse momento conosco."
        ]
    
    import random
    return random.choice(responses)

# Servir o arquivo index.html como página principal
@app.route('/')
def index():
    try:
        return send_from_directory('.', 'index.html')
    except:
        # Se index.html não existir, retornar página de status
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AutoU Email Classifier</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                .container { 
                    background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px);
                    padding: 40px; 
                    border-radius: 20px; 
                    text-align: center; 
                    border: 1px solid rgba(255,255,255,0.2);
                    max-width: 600px;
                }
                h1 { font-size: 3em; margin-bottom: 20px; }
                .status { 
                    background: rgba(16, 185, 129, 0.2); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin: 20px 0;
                    border: 1px solid rgba(16, 185, 129, 0.3);
                }
                .endpoints { 
                    background: rgba(255,255,255,0.1); 
                    padding: 20px; 
                    border-radius: 15px; 
                    margin-top: 20px;
                    text-align: left;
                }
                .endpoint { 
                    background: rgba(255,255,255,0.1); 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 10px; 
                }
                code { 
                    background: rgba(0,0,0,0.3); 
                    padding: 5px 10px; 
                    border-radius: 5px; 
                    font-family: 'Courier New', monospace;
                    display: block;
                    margin-top: 5px;
                }
                .note { 
                    background: rgba(255, 193, 7, 0.2); 
                    padding: 15px; 
                    border-radius: 10px; 
                    margin-top: 20px;
                    border: 1px solid rgba(255, 193, 7, 0.3);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 AutoU Email Classifier</h1>
                
                <div class="status">
                    <h2>✅ Backend Ativo!</h2>
                    <p>Servidor Flask funcionando na porta 5000</p>
                </div>
                
                <div class="endpoints">
                    <h3>📡 Endpoints Disponíveis:</h3>
                    
                    <div class="endpoint">
                        <strong>POST /api/analyze</strong>
                        <p>Analisar email</p>
                        <code>curl -X POST -H "Content-Type: application/json" -d '{"text":"Preciso de ajuda"}' http://localhost:5000/api/analyze</code>
                    </div>
                    
                    <div class="endpoint">
                        <strong>GET /api/health</strong>
                        <p>Status da API</p>
                        <code>http://localhost:5000/api/health</code>
                    </div>
                    
                    <div class="endpoint">
                        <strong>GET /api/test</strong>
                        <p>Teste do classificador</p>
                        <code>http://localhost:5000/api/test</code>
                    </div>
                </div>
                
                <div class="note">
                    <h3>📝 Nota:</h3>
                    <p>Para usar a interface completa, coloque o arquivo index.html na mesma pasta que app.py</p>
                </div>
            </div>
        </body>
        </html>
        """

# Servir arquivos estáticos (CSS, JS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory('.', filename)
    except:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OK',
        'message': 'AutoU Email Classifier funcionando!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': ['/api/health', '/api/analyze', '/api/test'],
        'version': '1.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # Obter texto do request
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '') if data else ''
        else:
            text = request.form.get('text', '')
        
        if not text or len(text.strip()) < 5:
            return jsonify({'error': 'Texto muito curto ou vazio'}), 400
        
        # Classificar
        classification, confidence = classify_email(text)
        
        # Gerar resposta sugerida
        suggested_response = generate_response(text, classification)
        
        return jsonify({
            'classification': classification,
            'confidence': confidence,
            'suggested_response': suggested_response,
            'analysis': {
                'word_count': len(text.split()),
                'char_count': len(text),
                'has_question': '?' in text,
                'has_exclamation': '!' in text
            },
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/test')
def test():
    test_cases = [
        {
            'text': 'Estou com problema no sistema, preciso de ajuda urgente!',
            'expected': 'Produtivo'
        },
        {
            'text': 'Parabéns pelo aniversário! Feliz aniversário!',
            'expected': 'Improdutivo'
        },
        {
            'text': 'Reunião marcada para discutir o projeto importante.',
            'expected': 'Produtivo'
        },
        {
            'text': 'Obrigado pelo café da manhã! Foi muito gostoso.',
            'expected': 'Improdutivo'
        }
    ]
    
    results = []
    for i, case in enumerate(test_cases):
        classification, confidence = classify_email(case['text'])
        results.append({
            'test_id': i + 1,
            'text': case['text'],
            'expected': case['expected'],
            'got': classification,
            'confidence': confidence,
            'correct': classification == case['expected']
        })
    
    correct_count = sum(1 for r in results if r['correct'])
    accuracy = (correct_count / len(results)) * 100
    
    return jsonify({
        'test_results': results,
        'summary': {
            'total_tests': len(results),
            'correct': correct_count,
            'accuracy': f"{accuracy:.1f}%"
        },
        'status': 'success'
    })

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == '__main__':
    print("🚀 AutoU Email Classifier - Iniciando...")
    print("📡 Servidor: http://localhost:5000")
    print("🏥 Health: http://localhost:5000/api/health")
    print("🧪 Test: http://localhost:5000/api/test")
    print("⚠️  Mantenha este terminal aberto")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # Para Vercel
    application = app