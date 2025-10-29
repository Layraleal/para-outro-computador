// Função para abrir a barra de configurações da esquerda
function abrirBarra() {
	document.querySelector('.config-bar').style.display = 'block';
	document.querySelector('.config-bar').style.transform = 'translateX(0)';
}
				
// Função para fechar a barra de configurações
function fecharBarra() {
	document.querySelector('.config-bar').style.transform = 'translateX(100%)';
	setTimeout(() => {
		document.querySelector('.config-bar').style.display = 'none';
	    }, 300); // Espera o tempo da animação para esconder a barra
}
				
				
// Adiciona o evento de clique no ícone de configurações
document.querySelector('.config-icon').addEventListener('click', function() {
	abrirBarra();
});		


// Função para abrir os submenu

function toggleSubmenu(id, button) {

    const submenu = document.getElementById(id);
	const icon = button.querySelector('i.rotatable'); // ícone rotativo (chevron)

	// Alternar visibilidade do submenu
	const isVisible = submenu.style.display === "block";
	submenu.style.display = isVisible ? "none" : "block";

	// Rotacionar o ícone
	if (icon) {
		icon.classList.toggle("rotated", !isVisible);
		}
	}