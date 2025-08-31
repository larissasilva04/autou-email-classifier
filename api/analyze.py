from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import re
import random
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=['*'])

def classify_email_professional(text):
    """Classificação profissional de email"""
    
    text_lower = text.lower().strip()
    
    # Palavras-chave ponderadas (versão profissional)
    productive_keywords = {
        # Problemas técnicos (peso alto)
        'problema': 4, 'erro': 4, 'bug': 4, 'falha': 4, 'defeito': 3,
        'não funciona': 5, 'parou de funcionar': 5, 'travou': 3,
        
        # Suporte e ajuda (peso alto)
        'suporte': 3, 'ajuda': 3, 'assistência': 3, 'socorro': 4,
        'dúvida': 2, 'questão': 2, 'esclarecimento': 2,
        
        # Urgência (peso muito alto)
        'urgente': 5, 'emergência': 5, 'crítico': 5, 'imediato': 4,
        'asap': 4, 'prioridade': 3, 'importante': 2,
        
        # Negócios
        'reunião': 2, 'meeting': 2, 'proposta': 3, 'orçamento': 3,
        'contrato': 3, 'projeto': 2, 'deadline': 3, 'prazo': 3,
        
        # Ações
        'implementar': 2, 'desenvolver': 2, 'criar': 2, 'modificar': 2,
        'corrigir': 3, 'resolver': 3, 'atualizar': 2, 'status': 2
    }
    
    unproductive_keywords = {
        # Felicitações
        'parabéns': 4, 'felicitações': 4, 'congratulações': 3,
        
        # Datas especiais
        'aniversário': 3, 'natal': 4, 'ano novo': 4, 'festas': 2,
        
        # Agradecimentos
        'obrigado': 2, 'obrigada': 2, 'agradecimento': 3, 'gratidão': 3,
        
        # Social
        'café': 1, 'almoço': 1, 'jantar': 1, 'happy hour': 2,
        'fim de semana': 1, 'feriado': 1, 'férias': 2,
        
        # Entretenimento
        'piada': 3, 'engraçado': 2, 'funny': 2, 'humor': 2
    }
    
    # Calcular scores
    productive_score = 0
    unproductive_score = 0
    found_keywords = []
    
    for keyword, weight in productive_keywords.items():
        if keyword in text_lower:
            productive_score += weight
            found_keywords.append(f'"{keyword}" (+{weight}P)')
    
    for keyword, weight in unproductive_keywords.items():
        if keyword in text_lower:
            unproductive_score += weight
            found_keywords.append(f'"{keyword}" (+{weight}I)')
    
    # Análise estrutural
    question_count = text.count('?')
    if question_count > 0:
        productive_score += question_count * 2
        found_keywords.append(f'{question_count} pergunta(s) (+{question_count * 2}P)')
    
    exclamation_count = text.count('!')
    if exclamation_count > 3:
        unproductive_score += min(exclamation_count - 3, 3)
        found_keywords.append(f'exclamações excessivas (+{min(exclamation_count - 3, 3)}I)')
    elif exclamation_count > 0 and any(urgent in text_lower for urgent in ['urgente', 'emergência']):
        productive_score += exclamation_count
        found_keywords.append(f'exclamações urgentes (+{exclamation_count}P)')
    
    # Análise de comprimento
    word_count = len(text.split())
    if word_count > 100:
        productive_score += 2
        found_keywords.append('email longo (+2P)')
    elif word_count < 15:
        if unproductive_score == 0:
            unproductive_score += 1
            found_keywords.append('email muito curto (+1I)')
    
    # Determinar classificação
    total_score = productive_score + unproductive_score
    
    if total_score == 0:
        # Sem indicadores - análise de contexto
        if word_count > 50 and question_count > 0:
            classification = 'Produtivo'
            confidence = 0.65
            explanation = 'Email com perguntas e tamanho médio, provável solicitação.'
        elif word_count > 80:
            classification = 'Produtivo'
            confidence = 0.70
            explanation = 'Email longo sem palavras-chave específicas, classificado como produtivo por precaução.'
        else:
            classification = 'Improdutivo'
            confidence = 0.60
            explanation = 'Email curto sem indicadores claros de produtividade.'
    else:
        if productive_score > unproductive_score:
            classification = 'Produtivo'
            confidence_ratio = productive_score / total_score
            confidence = min(0.95, 0.65 + confidence_ratio * 0.30)
            explanation = f'Email produtivo (score: {productive_score} vs {unproductive_score}). '
        else:
            classification = 'Improdutivo'
            confidence_ratio = unproductive_score / total_score
            confidence = min(0.95, 0.65 + confidence_ratio * 0.30)
            explanation = f'Email improdutivo (score: {unproductive_score} vs {productive_score}). '
        
        # Adicionar palavras-chave principais
        if found_keywords:
            explanation += f'Principais indicadores: {", ".join(found_keywords[:5])}'
            if len(found_keywords) > 5:
                explanation += f' e mais {len(found_keywords) - 5}.'
    
    return {
        'classification': classification,
        'confidence': round(confidence, 3),
        'explanation': explanation,
        'analysis_details': {
            'scores': {
                'productive': productive_score,
                'unproductive': unproductive_score,
                'total': total_score
            },
            'text_stats': {
                'word_count': word_count,
                'char_count': len(text),
                'question_count': question_count,
                'exclamation_count': exclamation_count
            },
            'found_keywords': found_keywords[:10]
        }
    }

def generate_professional_response(email_content, classification):
    """Gerar resposta profissional contextualizada"""
    
    # Extrair nome do remetente
    lines = email_content.split('\n')
    sender_name = "Cliente"
    
    for line in reversed(lines):
        line = line.strip()
        if len(line) > 2 and len(line) < 40 and not '@' in line:
            words = line.split()
            if len(words) <= 3 and not any(char.isdigit() for char in line):
                sender_name = line.title()
                break
    
    # Gerar protocolo único
    protocol = f"AU{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(10, 99)}"
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    if classification.lower() == 'produtivo':
        # Detectar tipo de solicitação
        content_lower = email_content.lower()
        
        if any(word in content_lower for word in ['urgente', 'emergência', 'crítico']):
            return f"""Prezado(a) {sender_name},

🚨 SOLICITAÇÃO URGENTE RECEBIDA

Protocolo: #{protocol}
Recebido: {timestamp}
Status: PRIORIDADE MÁXIMA

Nossa equipe de suporte foi imediatamente acionada e está priorizando seu atendimento.

⏰ Primeira resposta: até 2 horas
🔧 Resolução estimada: 4-6 horas
📱 Suporte urgente: (11) 9999-9999

Acompanhe em tempo real: https://status.autou.io/#{protocol}

Atenciosamente,
Equipe de Suporte AutoU
Central de Atendimento 24/7"""

        elif any(word in content_lower for word in ['reunião', 'meeting', 'proposta', 'comercial']):
            return f"""Prezado(a) {sender_name},

Agradecemos seu contato comercial!

📊 Detalhes da solicitação:
   • Protocolo: #{protocol}
   • Recebido: {timestamp}
   • Tipo: Oportunidade Comercial
   • Status: Em análise

💼 Nossa equipe comercial irá:
   ✓ Analisar suas necessidades
   ✓ Preparar proposta personalizada
   ✓ Agendar apresentação
   ✓ Acompanhar todo o processo

📅 Retorno comercial: até 48h úteis
📧 Contato: comercial@autou.io
📞 WhatsApp: (11) 99999-8888

Cordialmente,
Equipe Comercial AutoU
"Transformando processos através da tecnologia" """

        else:
            return f"""Prezado(a) {sender_name},

Obrigado por entrar em contato com o suporte AutoU.

📋 Sua solicitação foi registrada:
   • Protocolo: #{protocol}
   • Data/Hora: {timestamp}
   • Categoria: Suporte Técnico
   • Status: Em análise

👨‍💻 Nossa equipe irá:
   1. Analisar sua questão detalhadamente
   2. Replicar o cenário descrito
   3. Desenvolver a melhor solução
   4. Implementar e validar

⏰ Prazo de resposta: até 24 horas úteis
🌐 Acompanhar: https://suporte.autou.io/#{protocol}

Atenciosamente,
Equipe Técnica AutoU
suporte@autou.io | (11) 3333-4444"""

    else:  # Improdutivo
        content_lower = email_content.lower()
        
        if any(word in content_lower for word in ['parabéns', 'felicitações', 'aniversário']):
            return f"""Caro(a) {sender_name},

🎉 Que alegria receber sua mensagem de felicitação!

Muito obrigado por pensar em nós neste momento especial. Gestos como o seu tornam nossa jornada ainda mais significativa.

✨ Retribuímos os votos de felicidade e sucesso!

Que este seja o início de muitas conquistas e realizações incríveis.

A equipe AutoU torce sempre por você! 🌟

Com muito carinho,
Família AutoU 💙"""

        elif any(word in content_lower for word in ['obrigado', 'obrigada', 'agradecimento']):
            return f"""Prezado(a) {sender_name},

😊 Seu agradecimento iluminou nosso dia!

É uma honra fazer parte da sua jornada e saber que nosso trabalho fez a diferença.

Na AutoU, acreditamos que relacionamentos genuínos são a base de tudo. Mensagens como a sua nos motivam a sempre buscar a excelência.

Conte sempre conosco para o que precisar!

Tenha uma excelente semana!

Com gratidão,
Equipe AutoU 💙"""

        else:
            return f"""Olá {sender_name}!

Que bom receber seu contato! 😊

É sempre um prazer manter essa conexão com pessoas especiais como você.

Espero que seu dia esteja sendo incrível e cheio de boas energias!

Um abraço caloroso,
Time AutoU 🤗"""

# ENDPOINT PRINCIPAL
@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """Endpoint principal para análise de emails"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        start_time = time.time()
        
        # Obter dados da request
        data = request.get_json() if request.is_json else {}
        text = data.get('text') or request.form.get('text') or ''
        
        # Validações
        if not text or len(text.strip()) < 10:
            return jsonify({
                'error': 'Texto muito curto',
                'message': 'Email deve ter pelo menos 10 caracteres',
                'received_length': len(text) if text else 0
            }), 400
        
        if len(text) > 50000:  # 50k chars max para Vercel
            return jsonify({
                'error': 'Texto muito longo',
                'message': 'Limite de 50.000 caracteres para processamento'
            }), 400
        
        # Classificar email
        classification_result = classify_email_professional(text)
        
        # Gerar resposta
        suggested_response = generate_professional_response(
            text, 
            classification_result['classification']
        )
        
        # Calcular tempo de processamento
        processing_time = round(time.time() - start_time, 3)
        
        # Resposta da API
        response_data = {
            'status': 'success',
            'classification': classification_result['classification'],
            'confidence': classification_result['confidence'],
            'explanation': classification_result['explanation'],
            'suggested_response': suggested_response,
            'processing_metrics': {
                'total_time_seconds': processing_time,
                'content_length': len(text),
                'words_count': len(text.split()),
                'algorithm': 'Professional Rule-Based + ML Features'
            },
            'analysis_details': classification_result['analysis_details'],
            'api_info': {
                'version': '2.0.0-vercel',
                'environment': 'serverless',
                'timestamp': datetime.now().isoformat(),
                'request_id': f"req_{int(time.time())}{random.randint(100, 999)}"
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        error_message = str(e)
        
        return jsonify({
            'status': 'error',
            'error': 'Erro no processamento',
            'message': error_message,
            'api_info': {
                'version': '2.0.0-vercel',
                'timestamp': datetime.now().isoformat()
            }
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'AutoU Email Classifier API - Vercel Edition',
        'version': '2.0.0-vercel',
        'environment': 'serverless',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/analyze',
            '/api/health'
        ]
    })

# Para Vercel Serverless Functions
def handler(request):
    with app.test_request_context(path=request.url, method=request.method):
        return app.full_dispatch_request()

# Export para Vercel
from werkzeug.wrappers import Response

def lambda_handler(event, context):
    return handler(event)