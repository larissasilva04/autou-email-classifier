import os
import logging
from typing import Dict, Any
import openai
from dotenv import load_dotenv
import random
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Gerador de respostas automáticas para emails"""
    
    def __init__(self):
        """Inicializar o gerador de respostas"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY não encontrada. Usando respostas pré-definidas.")
            self.use_openai = False
        else:
            self.use_openai = True
            openai.api_key = self.api_key

        self.productive_templates = [
            """Prezado(a) {sender},

Obrigado por entrar em contato conosco. Recebemos sua solicitação e nossa equipe está analisando a questão.

Retornaremos com uma resposta em até 24 horas úteis.

Caso precise de suporte imediato, favor entrar em contato pelo telefone (xx) xxxx-xxxx.

Atenciosamente,
Equipe de Suporte""",

            """Olá,

Agradecemos seu email. Sua solicitação foi registrada em nosso sistema com o protocolo #{protocol}.

Nossa equipe especializada irá avaliar a situação e retornar com as informações solicitadas no menor prazo possível.

Em caso de dúvidas, favor referenciar o número do protocolo em futuras comunicações.

Cordialmente,
Central de Atendimento""",

            """Caro(a) cliente,

Confirmamos o recebimento de sua mensagem. Entendemos a importância de sua solicitação e estamos trabalhando para fornecer a melhor solução.

Previsão de resposta: até 48 horas úteis.

Agradecemos sua paciência e confiança em nossos serviços.

Atenciosamente,
Equipe Técnica"""
        ]

        self.unproductive_templates = [
            """Prezado(a) {sender},

Muito obrigado por sua mensagem! É sempre um prazer receber contato de você.

{acknowledgment}

Desejo a você um excelente dia!

Cordialmente,
[Nome]""",

            """Olá!

Agradeço imensamente por pensar em mim/nós. Sua mensagem trouxe um sorriso ao meu dia!

{acknowledgment}

Um abraço caloroso,
[Nome]""",

            """Caro(a) {sender},

Que gentileza sua! Muito obrigado por compartilhar esse momento conosco.

{acknowledgment}

Com carinho,
[Nome]"""
        ]

    def generate_response(self, email_content: str, classification: str) -> str:
        """Gerar resposta automática baseada na classificação"""
        
        if self.use_openai:
            try:
                return self._generate_with_openai(email_content, classification)
            except Exception as e:
                logger.warning(f"Erro na geração via OpenAI: {str(e)}")
                logger.info("Usando templates pré-definidos como fallback")
                return self._generate_with_templates(email_content, classification)
        else:
            return self._generate_with_templates(email_content, classification)

    def _generate_with_openai(self, email_content: str, classification: str) -> str:
        """Gerar resposta usando OpenAI GPT"""
        
        if classification.lower() == 'produtivo':
            prompt = f"""
Você é um assistente de atendimento ao cliente profissional. Gere uma resposta automática adequada para o email produtivo abaixo.

A resposta deve:
- Ser profissional e cortês
- Confirmar o recebimento da solicitação
- Indicar próximos passos ou prazo de resposta
- Ser concisa mas completa
- Estar em português brasileiro
- Incluir uma saudação e despedida apropriadas

Email recebido:
"{email_content[:500]}"

Gere uma resposta profissional:
"""
        else:
            prompt = f"""
Você é um assistente de comunicação corporativa. Gere uma resposta automática adequada para o email improdutivo abaixo.

A resposta deve:
- Ser calorosa e amigável
- Agradecer pela mensagem
- Ser breve mas cordial
- Estar em português brasileiro
- Demonstrar apreço pela comunicação

Email recebido:
"{email_content[:500]}"

Gere uma resposta calorosa e amigável:
"""

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em comunicação corporativa. Sempre responda em português brasileiro de forma profissional e adequada ao contexto."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            generated_response = response.choices[0].message.content.strip()
            
            if len(generated_response) < 50:
                raise ValueError("Resposta muito curta")
            
            return generated_response
            
        except Exception as e:
            logger.error(f"Erro na API OpenAI: {str(e)}")
            raise

    def _generate_with_templates(self, email_content: str, classification: str) -> str:
        """Gerar resposta usando templates pré-definidos"""
        
        sender_name = self._extract_sender_name(email_content)
        protocol = self._generate_protocol()
        
        if classification.lower() == 'produtivo':
            template = random.choice(self.productive_templates)
            
            response = template.format(
                sender=sender_name,
                protocol=protocol
            )
            
        else:  # improdutivo
            template = random.choice(self.unproductive_templates)
            acknowledgment = self._generate_acknowledgment(email_content)
            
            response = template.format(
                sender=sender_name,
                acknowledgment=acknowledgment
            )
        
        return response

    def _extract_sender_name(self, email_content: str) -> str:
        """Extrair nome do remetente do email"""
        
        lines = email_content.split('\n')
        
        for line in reversed(lines):
            line = line.strip()
            if line and not self._is_email_line(line) and len(line.split()) <= 3:

                if not any(char.isdigit() for char in line):
                    return line.title()
        
        import re
        patterns = [
            r'atenciosamente,?\s*([a-záàâãéêíóôõúç\s]+)',
            r'cordialmente,?\s*([a-záàâãéêíóôõúç\s]+)',
            r'abraços,?\s*([a-záàâãéêíóôõúç\s]+)',
            r'de:\s*([a-záàâãéêíóôõúç\s]+)',
            r'from:\s*([a-záàâãéêíóôõúç\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, email_content.lower())
            if match:
                name = match.group(1).strip().title()
                if len(name.split()) <= 3:
                    return name
        
        return "Cliente"

    def _is_email_line(self, line: str) -> bool:
        """Verificar se a linha contém informações de email"""
        email_indicators = ['@', 'email:', 'e-mail:', 'tel:', 'telefone:', 'www.', 'http']
        return any(indicator in line.lower() for indicator in email_indicators)

    def _generate_protocol(self) -> str:
        """Gerar número de protocolo fictício"""
        import random
        now = datetime.now()
        return f"{now.year}{now.month:02d}{random.randint(1000, 9999)}"

    def _generate_acknowledgment(self, email_content: str) -> str:
        """Gerar agradecimento específico baseado no conteúdo"""
        
        content_lower = email_content.lower()
        
        if any(word in content_lower for word in ['parabéns', 'felicitações']):
            return "Suas felicitações significam muito para nós!"
        
        elif any(word in content_lower for word in ['natal', 'ano novo', 'festas']):
            return "Retribuímos os votos de boas festas! Que o próximo período seja repleto de realizações."
        
        elif any(word in content_lower for word in ['aniversário', 'birthday']):
            return "Muito obrigado pelos parabéns! Foi muito gentil de sua parte."
        
        elif any(word in content_lower for word in ['obrigado', 'obrigada', 'agradeço']):
            return "Fico feliz em poder ajudar! Conte sempre conosco."
        
        elif any(word in content_lower for word in ['compartilhar', 'forward', 'interessante']):
            return "Obrigado por compartilhar essa informação conosco."
        
        else:
            return "Agradeço por manter contato e pensar em nós."

    def customize_response_for_context(self, response: str, email_content: str) -> str:
        """Personalizar resposta baseada no contexto do email"""
        
        content_lower = email_content.lower()
        
        if 'sistema' in content_lower or 'login' in content_lower:
            response += "\n\nPara questões técnicas urgentes, nosso suporte está disponível 24/7."
        
        elif 'reunião' in content_lower or 'meeting' in content_lower:
            response += "\n\nConfirmaremos a disponibilidade e enviaremos o convite do calendário em breve."
        
        elif 'orçamento' in content_lower or 'proposta' in content_lower:
            response += "\n\nNossa equipe comercial entrará em contato para alinhar os detalhes."
        
        elif 'urgente' in content_lower or 'emergência' in content_lower:
            response += "\n\n⚠️ Devido à urgência mencionada, priorizaremos sua solicitação."
        
        return response

    def generate_subject_suggestion(self, classification: str, original_content: str) -> str:
        """Gerar sugestão de assunto para a resposta"""
        
        if classification.lower() == 'produtivo':
            if 'suporte' in original_content.lower():
                return "Re: Confirmação de recebimento - Solicitação de Suporte"
            elif 'reunião' in original_content.lower():
                return "Re: Confirmação - Agendamento de Reunião"
            elif 'orçamento' in original_content.lower():
                return "Re: Recebido - Solicitação de Orçamento"
            else:
                return "Re: Confirmação de recebimento"
        else:
            return "Re: Muito obrigado!"