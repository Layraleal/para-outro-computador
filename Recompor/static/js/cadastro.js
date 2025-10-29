// Variável com o caminho base das imagens (deve estar na template Django)
  const caminhoBase = "{% static 'img/' %}";

  function abrirModal() {
    document.getElementById('modalFotos').style.display = 'flex';
  }

  function fecharModal() {
    document.getElementById('modalFotos').style.display = 'none';
  }

  function confirmarEscolha() {
    fecharModal(); // Fecha o modal

}

  function selecionarFoto(nomeFoto) {
    const caminhoBase = "/static/img/";
    document.getElementById('foto').value = nomeFoto; // Atualiza o campo oculto
    document.getElementById('preview').src = `/static/img/${nomeFoto}`; // Atualiza a pré-visualização

  
    const preview = document.getElementById('preview');
    preview.src = caminhoBase + nomeFoto;

    fecharModal();
  }

let currentIndex = 0;

document.getElementById('btnEsquerda').addEventListener('click', (event) => {
    event.preventDefault(); // Impede o comportamento padrão
    event.stopPropagation(); // Impede a propagação do evento
    moverCarrossel(-1);
});

document.getElementById('btnDireita').addEventListener('click', (event) => {
    event.preventDefault(); // Impede o comportamento padrão
    event.stopPropagation(); // Impede a propagação do evento
    moverCarrossel(1);
});

function moverCarrossel(direcao) {
    const carouselInner = document.getElementById('carouselInner');
    const totalImagens = carouselInner.children.length;
    const larguraImagem = 100; // Largura da imagem + margem (80px + 20px)

    // Calcula o novo índice
    currentIndex += direcao;

    // Impede que o índice saia dos limites
    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex > totalImagens - 4) { // Mostra até 4 imagens por vez
        currentIndex = totalImagens - 4;
    }

    // Move o carrossel
    const deslocamento = -(currentIndex * larguraImagem);
    carouselInner.style.transform = `translateX(${deslocamento}px)`;
}
document.getElementById('form_contato').addEventListener('submit', function(event) {
    const foto = document.getElementById('foto').value;
    if (!foto) {
        document.getElementById('foto').value = "icon_user.png"; // Define valor padrão
    }
});