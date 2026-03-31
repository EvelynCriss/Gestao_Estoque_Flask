
document.addEventListener('DOMContentLoaded', function() {

    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
    
    
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
    
    
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    
    
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


function formatCNPJ(cnpj) {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
}


function formatTelefone(tel) {
    return tel.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
}

(function(){
    document.addEventListener('DOMContentLoaded', function(){
        const container = document.getElementById('pedido-items');
        if(!container) return; 

        let produtosData = [];
        try{
            const raw = container.getAttribute('data-produtos') || '[]';
            produtosData = JSON.parse(raw);
        }catch(e){
            produtosData = [];
        }

        const itemsBody = container.querySelector('#items-body');
        const addBtn = container.querySelector('#add-item');

        function buildOptionsHtml(){
            return produtosData.map(p => `<option value="${p.id}">${p.nome}</option>`).join('');
        }

        function createRow(){
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <select name="produto_id[]" class="form-control">
                        <option value="">Selecione um produto</option>
                        ${buildOptionsHtml()}
                    </select>
                </td>
                <td><input type="number" name="quantidade[]" class="form-control" min="1" value="1"></td>
                <td>
                    <input type="hidden" name="preco_unitario[]" class="preco-hidden" value="0.00">
                    <input type="text" class="form-control preco-display" value="0.00" readonly>
                </td>
                <td><button type="button" class="btn btn-danger btn-sm remove-item">Remover</button></td>
            `;
            return tr;
        }

        function setPriceForRow(selectEl){
            const row = selectEl.closest('tr');
            if(!row) return;
            const hid = row.querySelector('.preco-hidden');
            const disp = row.querySelector('.preco-display');
            const pid = selectEl.value;
            const prod = produtosData.find(p => String(p.id) === String(pid));
            const price = prod && prod.preco ? Number(prod.preco).toFixed(2) : Number(0).toFixed(2);
            if(hid) hid.value = price;
            if(disp) disp.value = price;
        }

        if(itemsBody){
            const selects = itemsBody.querySelectorAll('select[name="produto_id[]"]');
            selects.forEach(s => setPriceForRow(s));
        }

        if(addBtn){
            addBtn.addEventListener('click', function(){
                const row = createRow();
                itemsBody.appendChild(row);
            });
        }

        if(itemsBody){
            itemsBody.addEventListener('click', function(e){
                if(e.target && e.target.classList.contains('remove-item')){
                    const tr = e.target.closest('tr');
                    if(tr) tr.remove();
                }
            });

            itemsBody.addEventListener('change', function(e){
                if(e.target && e.target.name === 'produto_id[]'){
                    setPriceForRow(e.target);
                }
            });
        }
    });
})();