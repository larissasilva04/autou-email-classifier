import re
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import logging
import string

logger = logging.getLogger(__name__)

class EmailProcessor:
    """Classe para processamento e limpeza de emails"""
    
    def __init__(self):
        """Inicializar o processador"""
        self._download_nltk_data()
        self.stemmer = RSLPStemmer()
        
        try:
            self.stop_words = set(stopwords.words('portuguese'))
            self.stop_words.update([
                'email', 'assunto', 'de', 'para', 'cc', 'cco', 'enviado', 
                'recebido', 'data', 'hora', 'anexo', 'att', 'atenciosamente',
                'cordialmente', 'abraços', 'saudações', 'prezado', 'prezada',
                'sr', 'sra', 'senhor', 'senhora', 'obrigado', 'obrigada'
            ])
        except:
            logger.warning("Stopwords portuguesas não encontradas, usando lista básica")
            self.stop_words = {'de', 'a', 'o', 'e', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'não', 'é', 'se', 'por', 'mais'}

    def _download_nltk_data(self):
        """Download dos dados necessários do NLTK"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/rslp')
        except LookupError:
            logger.info("Baixando dados do NLTK...")
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)  
                nltk.download('rslp', quiet=True)
            except:
                logger.warning("Não foi possível baixar alguns dados do NLTK")

    def process_file(self, filepath):
        """Processar arquivo e extrair texto"""
        try:
            if filepath.lower().endswith('.pdf'):
                return self._extract_pdf_text(filepath)
            elif filepath.lower().endswith('.txt'):
                return self._extract_txt_text(filepath)
            else:
                raise ValueError("Formato de arquivo não suportado")
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {filepath}: {str(e)}")
            raise

    def _extract_pdf_text(self, filepath):
        """Extrair texto de arquivo PDF"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
            raise
        
        if not text.strip():
            raise ValueError("PDF vazio ou não foi possível extrair texto")
        
        return text

    def _extract_txt_text(self, filepath):
        """Extrair texto de arquivo TXT"""
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as file:
                        text = file.read()
                    if text.strip():
                        return text
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Não foi possível decodificar o arquivo")
            
        except Exception as e:
            logger.error(f"Erro ao ler arquivo TXT: {str(e)}")
            raise

    def preprocess_text(self, text):
        """Pré-processar texto para análise"""
        try:
            text = self._remove_email_headers(text)
            
            text = text.lower()
            
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\d+', ' ', text)
            
            text = re.sub(r'\s+', ' ', text)
            
            tokens = word_tokenize(text)
            
            tokens = [
                token for token in tokens 
                if token not in self.stop_words 
                and len(token) > 2
                and not token.isdigit()
            ]
            
            stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
            
            return ' '.join(stemmed_tokens)
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {str(e)}")
            return text  

    def _remove_email_headers(self, text):
        """Remover headers e metadados comuns de emails"""
        header_patterns = [
            r'From:.*?\n',
            r'To:.*?\n', 
            r'Subject:.*?\n',
            r'Date:.*?\n',
            r'CC:.*?\n',
            r'BCC:.*?\n',
            r'Sent:.*?\n',
            r'De:.*?\n',
            r'Para:.*?\n',
            r'Assunto:.*?\n',
            r'Data:.*?\n',
            r'Enviado em:.*?\n'
        ]
        
        for pattern in header_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not self._is_signature_line(line):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def _is_signature_line(self, line):
        """Verificar se uma linha parece ser de assinatura"""
        signature_indicators = [
            '@', 'tel:', 'telefone:', 'cel:', 'celular:', 
            'skype:', 'linkedin:', 'www.', 'http',
            'atenciosamente', 'cordialmente', 'abraços',
            'departamento', 'empresa', 'ltd', 'ltda'
        ]
        
        line_lower = line.lower()
        return any(indicator in line_lower for indicator in signature_indicators)

    def extract_email_features(self, text):
        """Extrair características específicas do email"""
        features = {}
        
        features['length'] = len(text)
        features['word_count'] = len(text.split())
        
        features['exclamation_marks'] = text.count('!')
        features['question_marks'] = text.count('?')
        features['capital_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        urgency_words = ['urgente', 'emergência', 'imediato', 'rápido', 'asap']
        features['urgency_score'] = sum(1 for word in urgency_words if word in text.lower())
        
        question_words = ['como', 'quando', 'onde', 'por que', 'qual', 'quem']
        features['question_score'] = sum(1 for word in question_words if word in text.lower())
        
        gratitude_words = ['obrigado', 'obrigada', 'agradeço', 'grato', 'grata']
        features['gratitude_score'] = sum(1 for word in gratitude_words if word in text.lower())
        
        features['has_attachment'] = any(word in text.lower() for word in ['anexo', 'attachment', 'arquivo'])
        features['has_link'] = 'http' in text.lower() or 'www.' in text.lower()
        
        return features

    def clean_for_display(self, text, max_length=500):
        """Limpar texto para exibição"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        if max_length and len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text.strip()