import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_processor import EmailProcessor
from backend.start import EmailClassifier
from response_generator import ResponseGenerator
import time

def test_email_samples():
    """Testar com amostras de email"""
    
    processor = EmailProcessor()
    classifier = EmailClassifier()
    response_gen = ResponseGenerator()
    
    test_emails = [
        {
            "content": """
            Assunto: Problema com login no sistema
            
            Prezados,
            
            Estou enfrentando dificuldades para acessar o sistema desde ontem.
            Quando tento fazer login, recebo uma mensagem de erro "Usuário não encontrado".
            
            Poderiam verificar minha conta urgentemente? Preciso acessar os relatórios hoje.
            
            Atenciosamente,
            João Silva
            """,
            "expected": "Produtivo"
        },
        {
            "content": """
            Assunto: Feliz Aniversário!
            
            Oi Maria!
            
            Parabéns pelo seu aniversário! Espero que tenha um dia maravilhoso
            cercada de pessoas queridas.
            
            Que este novo ano de vida seja repleto de alegrias e realizações!
            
            Abraços,
            Ana
            """,
            "expected": "Improdutivo"
        },
        {
            "content": """
            Assunto: Solicitação de orçamento
            
            Bom dia,
            
            Gostaria de solicitar um orçamento para desenvolvimento de um sistema
            de gestão de estoque para nossa empresa.
            
            Quando poderiam agendar uma reunião para discutir os detalhes?
            
            Aguardo retorno.
            
            Roberto Santos
            Gerente de TI
            """,
            "expected": "Produtivo"
        },
        {
            "content": """
            Obrigado pela ajuda ontem! Foi muito gentil de sua parte.
            
            Tenha um ótimo final de semana!
            
            Carlos
            """,
            "expected": "Improdutivo"
        }
    ]
    
    print("🧪 TESTE DO CLASSIFICADOR DE EMAILS")
    print("=" * 50)
    
    correct_predictions = 0
    total_tests = len(test_emails)
    
    for i, test_email in enumerate(test_emails, 1):
        print(f"\n📧 Teste {i}/{total_tests}")
        print("-" * 30)
        
        processed_text = processor.preprocess_text(test_email["content"])
        
        start_time = time.time()
        result = classifier.classify(processed_text)
        classification_time = time.time() - start_time
        
        start_time = time.time()
        response = response_gen.generate_response(
            test_email["content"], 
            result["classification"]
        )
        response_time = time.time() - start_time
        
        is_correct = result["classification"] == test_email["expected"]
        if is_correct:
            correct_predictions += 1
        
        print(f"Conteúdo: {test_email['content'][:100]}...")
        print(f"Esperado: {test_email['expected']}")
        print(f"Obtido: {result['classification']}")
        print(f"Confiança: {result['confidence']:.2f}")
        print(f"Método: {result.get('method', 'N/A')}")
        print(f"Tempo classificação: {classification_time:.3f}s")
        print(f"Tempo resposta: {response_time:.3f}s")
        print(f"Status: {'✅ CORRETO' if is_correct else '❌ INCORRETO'}")
        
        if not is_correct:
            print(f"Explicação: {result.get('explanation', 'N/A')}")
        
        print(f"\nResposta gerada:")
        print(f"'{response[:150]}{'...' if len(response) > 150 else ''}'")
    
    accuracy = (correct_predictions / total_tests) * 100
    print("\n" + "=" * 50)
    print("📊 RESULTADOS FINAIS")
    print("=" * 50)
    print(f"Acertos: {correct_predictions}/{total_tests}")
    print(f"Precisão: {accuracy:.1f}%")
    
    if accuracy >= 75:
        print("🎉 TESTE PASSOU! Sistema funcionando adequadamente.")
        return True
    else:
        print("⚠️ ATENÇÃO: Precisão abaixo do esperado.")
        return False

def test_file_processing():
    """Testar processamento de arquivos"""
    
    print("\n🔧 TESTE DE PROCESSAMENTO DE ARQUIVOS")
    print("=" * 50)
    
    processor = EmailProcessor()
    
    test_content = """
    From: test@example.com
    To: support@company.com
    Subject: Test Email
    
    Este é um email de teste para verificar o processamento.
    Contém algumas informações importantes que precisam ser analisadas.
    
    Atenciosamente,
    Usuário Teste
    """
    
    try:
        with open('test_email.txt', 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        processed = processor.process_file('test_email.txt')
        print("✅ Processamento de arquivo TXT: OK")
        print(f"Conteúdo processado: {len(processed)} caracteres")
        
        os.remove('test_email.txt')
        
    except Exception as e:
        print(f"❌ Erro no processamento TXT: {e}")
        return False
    
    return True

def test_api_components():
    """Testar componentes da API"""
    
    print("\n🔧 TESTE DE COMPONENTES")
    print("=" * 50)
    
    try:
        processor = EmailProcessor()
        classifier = EmailClassifier()
        response_gen = ResponseGenerator()
        
        print("✅ Inicialização dos componentes: OK")
        
        test_text = "Este é um teste simples de processamento."
        processed = processor.preprocess_text(test_text)
        
        if processed:
            print("✅ Pré-processamento: OK")
        else:
            print("❌ Erro no pré-processamento")
            return False
        
        result = classifier.classify(processed)
        
        if 'classification' in result and 'confidence' in result:
            print("✅ Classificação: OK")
        else:
            print("❌ Erro na classificação")
            return False
        
        response = response_gen.generate_response(test_text, result['classification'])
        
        if response and len(response) > 20:
            print("✅ Geração de resposta: OK")
        else:
            print("❌ Erro na geração de resposta")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos componentes: {e}")
        return False

def main():
    """Função principal de teste"""
    
    print("🚀 INICIANDO TESTES DO EMAIL CLASSIFIER")
    print("=" * 60)
    
    all_passed = True
    
    if not test_api_components():
        all_passed = False
    
    if not test_file_processing():
        all_passed = False
    
    if not test_email_samples():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("Sistema pronto para deploy.")
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima antes do deploy.")
        return 1

if __name__ == "__main__":
    exit(main())