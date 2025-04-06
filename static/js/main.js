document.addEventListener('DOMContentLoaded', function() {
    // Funções JavaScript podem ser adicionadas aqui
    
    // Exemplo: Validação de formulário
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Validação pode ser adicionada aqui
            console.log('Formulário enviado');
        });
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});