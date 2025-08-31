📧 AutoU Classificador de Emails
Sistema inteligente de classificação de emails e geração de respostas automáticas desenvolvido para o processo seletivo da AutoU.
🎯 Visão Geral
Esta aplicação utiliza inteligência artificial para:

Classificar emails em categorias "Produtivo" ou "Improdutivo"
Gerar respostas automáticas apropriadas para cada categoria
Processar arquivos .txt e .pdf ou texto direto
Interface moderna e intuitiva baseada no design da AutoU

🚀 Demo
Link da aplicação: https://seu-app.vercel.app
Exemplos de Uso
Email Produtivo:
Assunto: Problema com login no sistema
Estou enfrentando dificuldades para acessar...
→ Classificação: Produtivo (85% confiança)
→ Resposta: Email de suporte técnico profissional
Email Improdutivo:
Assunto: Feliz Aniversário!
Parabéns pelo seu aniversário...
→ Classificação: Improdutivo (92% confiança)  
→ Resposta: Agradecimento caloroso e cordial

🛠️ Tecnologias Utilizadas

Frontend

HTML5 Semântico com estrutura acessível
CSS3 Avançado com animações e gradientes
JavaScript Vanilla para interações dinâmicas
Design System baseado na identidade visual da AutoU

Backend

Python 3.8+ como linguagem principal
Flask para API REST
OpenAI GPT-3.5 para classificação inteligente
NLTK para processamento de linguagem natural
PyPDF2 para leitura de arquivos PDF

Deploy e Infraestrutura

Vercel para hospedagem gratuita
Git/GitHub para controle de versão
Environment Variables para configuração segura

📁 Estrutura do Projeto
AUTO U/
├── frontend/
│   └── index.html          # Interface principal
├── backend/
│   ├── app.py              # Servidor Flask principal
│   ├── email_processor.py  # Processamento de emails
│   ├── classifier.py       # Classificação com IA
│   ├── response_generator.py # Geração de respostas
│   ├── analytics.py        # Sistema de métricas
│   └── requirements.txt    # Dependências Python
├── tests/
│   └── test_classifier.py  # Testes automatizados
├── vercel.json            # Configuração de deploy
├── .env.example           # Exemplo de variáveis de ambiente
└── README.md             # Esta documentação

⚡ Instalação e Uso
1. Pré-requisitos

Python 3.8 ou superior
Conta na OpenAI (para chave da API)
Node.js (para deploy na Vercel)

2. Configuração Local
bash# Clone o repositório
git clone https://github.com/seu-usuario/email-classifier.git
cd email-classifier

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate # Windows

# Instale dependências
pip install -r backend/requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com sua OPENAI_API_KEY
3. Execução Local
bash# Execute o servidor de desenvolvimento
cd backend
python app.py

# Acesse http://localhost:5000
4. Testes
bash# Execute os testes automatizados
python tests/test_classifier.py
🌐 Deploy na Vercel
1. Configuração da Vercel
bash# Instale a CLI da Vercel
npm i -g vercel

# Faça login
vercel login

# Execute o deploy
vercel --prod
2. Variáveis de Ambiente
No dashboard da Vercel, configure:

OPENAI_API_KEY: Sua chave da API OpenAI
FLASK_ENV: production

3. Domínio Personalizado (Opcional)
Configure um domínio personalizado nas configurações do projeto na Vercel.
🎨 Design e UX
Paleta de Cores (AutoU)

Laranja Principal: #FF6B35
Azul Principal: #1E40AF
Azul Escuro: #0F172A
Verde Sucesso: #10B981
Amarelo Atenção: #F59E0B

Características do Design

✨ Animações suaves para melhor experiência
📱 Design responsivo para todos os dispositivos
🎯 Foco na usabilidade com feedback visual claro
🚀 Loading states para transparência do processo
🔔 Notificações para confirmação de ações

🧠 Como Funciona
1. Processamento de Input
python# Upload de arquivo ou texto direto
input → EmailProcessor → texto limpo
2. Classificação Inteligente
python# Duas estratégias de classificação
texto → OpenAI GPT-3.5 → classificação + confiança
   ↓ (fallback)
texto → regras + palavras-chave → classificação
3. Geração de Resposta
python# Resposta contextualizada
(email + classificação) → ResponseGenerator → resposta personalizada
📊 Métricas e Analytics
O sistema coleta automaticamente:

Total de análises realizadas
Distribuição de classificações (Produtivo vs Improdutivo)
Métodos utilizados (OpenAI vs Regras)
Tipos de arquivo processados
Tempos de resposta médios
Taxa de sucesso da aplicação

Acesso às Métricas
bashGET /api/metrics
🔧 Configurações Avançadas
Personalizações do Classificador
python# Adicionar palavras-chave personalizadas
productive_keywords = {
    'sua_palavra': peso,
    # ...
}
Ajuste de Templates de Resposta
python# Personalizar templates no response_generator.py
productive_templates = [
    "Seu template personalizado aqui..."
]
🐛 Troubleshooting
Problemas Comuns
1. Erro de API OpenAI
Solução: Verifique se a OPENAI_API_KEY está configurada corretamente
2. Arquivo não processado
Solução: Verifique se o arquivo é .txt ou .pdf e menor que 10MB
3. Deploy falha na Vercel
Solução: Confirme que o vercel.json está na raiz e as dependências estão corretas
Logs e Debug
bash# Ativar modo debug local
export FLASK_DEBUG=True
python app.py
🧪 Testes
Casos de Teste Incluídos

Emails Produtivos:

Solicitações de suporte
Problemas técnicos
Pedidos de orçamento
Agendamento de reuniões


Emails Improdutivos:

Felicitações
Agradecimentos
Mensagens sociais
Forwards informativos



Executar Testes
bash# Teste completo do sistema
python tests/test_classifier.py

# Teste específico de componentes
python -m pytest tests/ -v

🚀 Próximas Melhorias
Funcionalidades Futuras

 Multi-idiomas (inglês, espanhol)
 Categorias customizáveis pelo usuário
 Integração com email (IMAP/POP3)
 Dashboard de analytics visual
 API de webhook para integrações
 Histórico de classificações
 Feedback do usuário para melhoria do modelo

Melhorias Técnicas

 Cache Redis para otimização
 Rate limiting por IP
 Logs estruturados com ELK Stack
 Monitoramento com health checks
 Testes de carga automatizados

👥 Contribuição
Como Contribuir

Fork o projeto
Crie uma branch para sua feature (git checkout -b feature/nova-feature)
Commit suas mudanças (git commit -m 'Adiciona nova feature')
Push para a branch (git push origin feature/nova-feature)
Abra um Pull Request

Padrões de Código

Python: PEP 8
JavaScript: ES6+ com comentários
CSS: BEM methodology
Commits: Conventional Commits

📄 Licença
Este projeto foi desenvolvido para o processo seletivo da AutoU.
📞 Contato
Desenvolvedor: Larissa Silva
Email: ls8730084@gmail.com
LinkedIn: https://www.linkedin.com/in/larissasilva-costa/

🎯 Sobre o Desafio AutoU
Este projeto foi desenvolvido como parte do processo seletivo da AutoU, demonstrando:

✅ Resolução de problemas complexos com tecnologia
✅ Autonomia na escolha de ferramentas e abordagens
✅ Foco na experiência do usuário final
✅ Qualidade técnica e boas práticas
✅ Deploy funcional em ambiente de produção

Critérios Atendidos

✅ Interface Web HTML com upload de arquivos
✅ Backend Python com processamento NLP
✅ Classificação IA usando OpenAI GPT
✅ Respostas automáticas contextualizadas
✅ Hospedagem na nuvem (Vercel)
✅ Design excepcional baseado na AutoU
✅ Funcionalidades avançadas (métricas, testes)

⚡ Desenvolvido com paixão por tecnologia para a AutoU