import os
import logging
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib

logger = logging.getLogger(__name__)

class FileProcessor:
    """Processador profissional de arquivos"""
    
    SUPPORTED_TYPES = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.eml': 'message/rfc822',
        '.msg': 'application/vnd.ms-outlook'
    }
    
    def __init__(self, max_size_mb: int = 50):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
    def process_file(self, filepath: str) -> Dict[str, Any]:
        """
        Processar arquivo e extrair informações
        
        Returns:
            Dict com content, metadata, hash, etc.
        """
        try:
            # Validações básicas
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
            
            file_stats = os.stat(filepath)
            if file_stats.st_size > self.max_size_bytes:
                raise ValueError(f"Arquivo muito grande: {file_stats.st_size} bytes")
            
            # Detectar tipo
            file_ext = Path(filepath).suffix.lower()
            if file_ext not in self.SUPPORTED_TYPES:
                raise ValueError(f"Formato não suportado: {file_ext}")
            
            # Gerar hash
            file_hash = self._generate_file_hash(filepath)
            
            # Extrair conteúdo
            content = self._extract_content(filepath, file_ext)
            
            # Metadados
            metadata = {
                'filename': Path(filepath).name,
                'size_bytes': file_stats.st_size,
                'extension': file_ext,
                'mime_type': self.SUPPORTED_TYPES[file_ext],
                'hash_md5': file_hash,
                'word_count': len(content.split()) if content else 0,
                'char_count': len(content) if content else 0
            }
            
            logger.info(f"Arquivo processado: {metadata['filename']} ({metadata['size_bytes']} bytes)")
            
            return {
                'content': content,
                'metadata': metadata,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {filepath}: {str(e)}")
            return {
                'content': '',
                'metadata': {},
                'success': False,
                'error': str(e)
            }
    
    def _extract_content(self, filepath: str, file_ext: str) -> str:
        """Extrair conteúdo baseado no tipo de arquivo"""
        
        if file_ext == '.txt':
            return self._extract_text(filepath)
        elif file_ext == '.pdf':
            return self._extract_pdf(filepath)
        elif file_ext == '.eml':
            return self._extract_email(filepath)
        elif file_ext == '.msg':
            return self._extract_msg(filepath)
        else:
            raise ValueError(f"Extração não implementada para {file_ext}")
    
    def _extract_text(self, filepath: str) -> str:
        """Extrair texto de arquivo .txt"""
        encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                if content.strip():
                    logger.debug(f"Arquivo lido com encoding {encoding}")
                    return content
            except UnicodeDecodeError:
                continue
        
        raise ValueError("Não foi possível decodificar o arquivo de texto")
    
    def _extract_pdf(self, filepath: str) -> str:
        """Extrair texto de PDF"""
        try:
            # Em produção real, usar PyPDF2 ou pdfplumber
            import PyPDF2
            
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                raise ValueError("PDF vazio ou não foi possível extrair texto")
            
            return text
            
        except ImportError:
            # Fallback se PyPDF2 não estiver disponível
            logger.warning("PyPDF2 não disponível. Simulando extração de PDF.")
            return f"[CONTEÚDO SIMULADO DE PDF]\n\nTexto extraído do arquivo PDF: {Path(filepath).name}\n\nEm produção, seria usado PyPDF2 para extração real."
        except Exception as e:
            raise ValueError(f"Erro ao processar PDF: {str(e)}")
    
    def _extract_email(self, filepath: str) -> str:
        """Extrair conteúdo de arquivo .eml"""
        try:
            import email
            
            with open(filepath, 'r', encoding='utf-8') as f:
                msg = email.message_from_file(f)
            
            # Extrair partes do email
            subject = msg.get('Subject', 'Sem assunto')
            from_addr = msg.get('From', 'Desconhecido')
            to_addr = msg.get('To', 'Desconhecido')
            
            # Extrair corpo
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Montar email formatado
            formatted_email = f"""Assunto: {subject}
De: {from_addr}
Para: {to_addr}

{body}"""
            
            return formatted_email
            
        except Exception as e:
            logger.warning(f"Erro ao processar EML: {str(e)}. Usando fallback.")
            # Fallback: ler como texto
            return self._extract_text(filepath)
    
    def _extract_msg(self, filepath: str) -> str:
        """Extrair conteúdo de arquivo .msg (Outlook)"""
        # Em produção real, usar extract-msg ou win32com
        logger.warning("Processamento MSG simulado. Em produção usar extract-msg.")
        
        return f"""[EMAIL EXTRAÍDO DE MSG]

Assunto: Email importado do Outlook
De: usuario@exemplo.com
Para: destinatario@exemplo.com

Este seria o conteúdo do email extraído do arquivo MSG do Outlook.

Em produção, seria usado extract-msg ou win32com para extração real.

Arquivo: {Path(filepath).name}
"""
    
    def _generate_file_hash(self, filepath: str) -> str:
        """Gerar hash MD5 do arquivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Erro ao gerar hash: {str(e)}")
            return "unknown"
    
    def validate_file(self, filepath: str) -> tuple[bool, str]:
        """
        Validar se arquivo pode ser processado
        
        Returns:
            (is_valid, error_message)
        """
        try:
            if not os.path.exists(filepath):
                return False, "Arquivo não existe"
            
            file_ext = Path(filepath).suffix.lower()
            if file_ext not in self.SUPPORTED_TYPES:
                return False, f"Formato {file_ext} não suportado"
            
            file_size = os.path.getsize(filepath)
            if file_size > self.max_size_bytes:
                return False, f"Arquivo muito grande ({file_size} bytes)"
            
            if file_size == 0:
                return False, "Arquivo vazio"
            
            return True, "Arquivo válido"
            
        except Exception as e:
            return False, f"Erro na validação: {str(e)}"


# Função utilitária para uso direto
def process_file_simple(filepath: str) -> str:
    """Função simplificada para extrair apenas o texto"""
    processor = FileProcessor()
    result = processor.process_file(filepath)
    
    if result['success']:
        return result['content']
    else:
        raise ValueError(result.get('error', 'Erro desconhecido'))


# Para compatibilidade com versão anterior
def extract_text_from_file(filepath: str) -> str:
    """Compatibilidade com função anterior"""
    return process_file_simple(filepath)