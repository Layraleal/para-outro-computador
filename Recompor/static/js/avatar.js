function selecionarAvatar(img) {
    // Remove a seleção anterior
    document.querySelectorAll('.avatar-option').forEach(el => {
        el.classList.remove('selecionado');
    });

    // Adiciona destaque ao selecionado
    img.classList.add('selecionado');

    // Atualiza o campo hidden e a pré-visualização
    const valor = img.getAttribute('data-value');
    document.getElementById('avatar-selecionado').value = valor;
    document.getElementById('preview').src = '/static/img/' + valor;
}

function previewImportado(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('preview').src = e.target.result;
            document.querySelectorAll('.avatar-option').forEach(el => {
                el.classList.remove('selecionado');
            });
            document.getElementById('avatar-selecionado').value = '';
        };
        reader.readAsDataURL(file);
    }
}
