const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const emailForm = document.getElementById('email-form');
const fileForm = document.getElementById('file-form');
const emailText = document.getElementById('email-text');
const fileInput = document.getElementById('file-input');
const resultsSection = document.getElementById('results');
const errorSection = document.getElementById('error-message');
const categoryBadge = document.getElementById('category-badge');
const confidenceFill = document.getElementById('confidence-fill');
const confidenceText = document.getElementById('confidence-text');
const responseText = document.getElementById('response-text');
const copyResponseBtn = document.getElementById('copy-response');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetTab = button.dataset.tab;
        
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        button.classList.add('active');
        document.getElementById(`${targetTab}-tab`).classList.add('active');
        
        hideResults();
        hideError();
    });
});

emailForm.addEventListener('submit', handleEmailSubmit);
fileForm.addEventListener('submit', handleFileSubmit);

copyResponseBtn.addEventListener('click', copyResponseToClipboard);

fileInput.addEventListener('change', handleFileInputChange);

async function handleEmailSubmit(e) {
    e.preventDefault();
    
    const text = emailText.value.trim();
    if (!text) {
        showError('Por favor, insira o texto do email para análise.');
        return;
    }
    
    setLoading(emailForm, true);
    hideResults();
    hideError();
    
    try {
        const formData = new FormData();
        formData.append('email_text', text);
        
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
        } else {
            showError(data.error || 'Erro ao classificar email');
        }
    } catch (error) {
        showError('Erro de conexão. Verifique se o servidor está executando.');
        console.error('Error:', error);
    } finally {
        setLoading(emailForm, false);
    }
}

async function handleFileSubmit(e) {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        showError('Por favor, selecione um arquivo para análise.');
        return;
    }
    
    if (!file.name.endsWith('.txt')) {
        showError('Apenas arquivos .txt são suportados.');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB
        showError('Arquivo muito grande. O tamanho máximo é 10MB.');
        return;
    }
    
    setLoading(fileForm, true);
    hideResults();
    hideError();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
        } else {
            showError(data.error || 'Erro ao processar arquivo');
        }
    } catch (error) {
        showError('Erro de conexão. Verifique se o servidor está executando.');
        console.error('Error:', error);
    } finally {
        setLoading(fileForm, false);
    }
}

function handleFileInputChange(e) {
    const file = e.target.files[0];
    const label = document.querySelector('.file-upload-area label');
    
    if (file) {
        label.innerHTML = `
            <span class="upload-icon">📄</span>
            <span>Arquivo selecionado: ${file.name}</span>
            <small>Tamanho: ${formatFileSize(file.size)}</small>
        `;
        label.style.borderColor = '#667eea';
        label.style.background = '#f8f9ff';
    } else {
        label.innerHTML = `
            <span class="upload-icon">📤</span>
            <span>Clique aqui ou arraste um arquivo .txt</span>
            <small>Formatos suportados: .txt (máx. 10MB)</small>
        `;
        label.style.borderColor = '#d0d0d0';
        label.style.background = 'transparent';
    }
}

function showResults(data) {
    hideError();
    
    categoryBadge.textContent = getCategoryDisplayName(data.category);
    categoryBadge.className = `category-badge ${data.category}`;
    
    confidenceFill.style.width = `${data.confidence}%`;
    confidenceText.textContent = `${data.confidence}%`;
    
    responseText.textContent = data.suggested_response;
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    hideResults();
    document.getElementById('error-text').textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function hideError() {
    errorSection.style.display = 'none';
}

function setLoading(form, isLoading) {
    const button = form.querySelector('.btn-primary');
    if (isLoading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

async function copyResponseToClipboard() {
    try {
        const text = responseText.textContent;
        await navigator.clipboard.writeText(text);
        
        const originalText = copyResponseBtn.innerHTML;
        copyResponseBtn.innerHTML = '✅ Copiado!';
        copyResponseBtn.style.background = '#2ed573';
        
        setTimeout(() => {
            copyResponseBtn.innerHTML = originalText;
            copyResponseBtn.style.background = '';
        }, 2000);
        
    } catch (error) {
        const textArea = document.createElement('textarea');
        textArea.value = responseText.textContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        alert('Resposta copiada para a área de transferência!');
    }
}

