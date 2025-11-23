// Aguarda o DOM estar completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== FLASH MESSAGES / ALERTS =====
    
    // Fechar alertas manualmente (clicando no X)
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Auto-fechar alertas após 5 segundos
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
    
    
    // ===== CONFIRMAÇÃO DE EXCLUSÃO =====
    
    // Adiciona confirmação em botões/links de deletar
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 
                          'Tem certeza que deseja deletar este item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    
    // ===== MÁSCARAS DE INPUT (OPCIONAL) =====
    
    // Máscara para CNPJ: 00.000.000/0000-00
    const cnpjInputs = document.querySelectorAll('input[name="cnpj"]');
    cnpjInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 14) {
                value = value.replace(/^(\d{2})(\d)/, '$1.$2');
                value = value.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
                value = value.replace(/\.(\d{3})(\d)/, '.$1/$2');
                value = value.replace(/(\d{4})(\d)/, '$1-$2');
                e.target.value = value;
            }
        });
    });
    
    // Máscara para Telefone: (00) 00000-0000
    const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
    telefoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/^(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
                e.target.value = value;
            }
        });
    });
    
    
    // ===== HIGHLIGHT DA LINHA DA TABELA AO PASSAR O MOUSE =====
    
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    
    // ===== FEEDBACK VISUAL AO SUBMETER FORMULÁRIO =====
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '⏳ Processando...';
            }
        });
    });
    
});


// Função para exibir um alerta customizado
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="close-alert">&times;</button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || 
                          document.querySelector('.main-content');
    
    if (flashContainer) {
        flashContainer.insertAdjacentElement('afterbegin', alertDiv);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
        
        // Botão de fechar
        alertDiv.querySelector('.close-alert').addEventListener('click', function() {
            alertDiv.style.display = 'none';
        });
    }
}

// Função para formatar CNPJ
function formatCNPJ(cnpj) {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
}

// Função para formatar Telefone
function formatTelefone(tel) {
    return tel.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
}