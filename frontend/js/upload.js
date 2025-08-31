function getCategoryDisplayName(category) {
    const names = {
        'spam': 'Spam',
        'promocional': 'Promocional',
        'trabalho': 'Trabalho',
        'pessoal': 'Pessoal',
        'importante': 'Importante',
        'erro': 'Erro',
        'indefinido': 'Indefinido'
    };
    return names[category] || category;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

const fileUploadArea = document.querySelector('.file-upload-area label');

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.style.borderColor = '#667eea';
    fileUploadArea.style.background = '#f8f9ff';
});

fileUploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    if (!fileInput.files[0]) {
        fileUploadArea.style.borderColor = '#d0d0d0';
        fileUploadArea.style.background = 'transparent';
    }
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
            fileInput.files = files;
            handleFileInputChange({ target: { files: [file] } });
        } else {
            showError('Apenas arquivos .txt são suportados.');
        }
    }
});

emailText.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.max(200, this.scrollHeight) + 'px';
});

const sampleEmails = [
    "PARABÉNS! Você ganhou um iPhone 15! Clique aqui para resgatar seu prêmio agora mesmo!",
    "Oi! Como você está? Há muito tempo que não nos falamos. Que tal marcarmos um café?",
    "Reunião de equipe agendada para amanhã às 14h. Por favor, confirme sua presença.",
    "Nova coleção de inverno disponível! Aproveite o desconto de 20% até domingo.",
    "Lembrete: sua conta de energia vence amanhã. Evite o corte do fornecimento."
];

const addSampleBtn = document.createElement('button');
addSampleBtn.type = 'button';
addSampleBtn.className = 'btn-secondary';
addSampleBtn.innerHTML = '🎲 Exemplo Aleatório';
addSampleBtn.style.marginBottom = '10px';
addSampleBtn.style.width = '100%';

addSampleBtn.addEventListener('click', () => {
    const randomEmail = sampleEmails[Math.floor(Math.random() * sampleEmails.length)];
    emailText.value = randomEmail;
    emailText.style.height = 'auto';
    emailText.style.height = Math.max(200, emailText.scrollHeight) + 'px';
});

const textTab = document.getElementById('text-tab');
textTab.insertBefore(addSampleBtn, emailText);

document.addEventListener('DOMContentLoaded', () => {
    console.log('Classificador de Emails carregado com sucesso!');
    
    fetch('/')
        .then(response => {
            if (response.ok) {
                console.log('Servidor conectado com sucesso!');
            }
        })
        .catch(error => {
            console.warn('Verifique se o servidor Flask está executando:', error);
        });
});