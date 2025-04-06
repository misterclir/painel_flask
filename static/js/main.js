document.addEventListener('DOMContentLoaded', function() {
    // Fun��es JavaScript podem ser adicionadas aqui
    
    // Exemplo: Valida��o de formul�rio
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Valida��o pode ser adicionada aqui
            console.log('Formul�rio enviado');
        });
    });
    
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});