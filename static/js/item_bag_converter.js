document.addEventListener('DOMContentLoaded', function() {
    const converterForm = document.getElementById('converterForm');
    
    if (converterForm) {
        converterForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('xml_files');
            if (fileInput.files.length === 0) {
                e.preventDefault();
                alert('Por favor, selecione pelo menos um arquivo XML para converter');
                return false;
            }
            
            const invalidFiles = Array.from(fileInput.files).filter(
                file => !file.name.endsWith('.xml')
            );
            
            if (invalidFiles.length > 0) {
                e.preventDefault();
                alert('Por favor, selecione apenas arquivos com extensão .xml');
                return false;
            }
            
            // Mostrar loading
            const submitBtn = converterForm.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Convertendo...';
            submitBtn.disabled = true;
        });
    }
});