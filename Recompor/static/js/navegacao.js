
let show = true;
const navbar = document.querySelector(".navbar")
const menuToggle = navbar.querySelector(".menu-toggle")
menuToggle.addEventListener("click", () => {
    document.body.style.overflow = show ? "hidden" : "initial"
    navbar.classList.toggle("on",show)
    show = !show;
})

// const Naologado = document.querySelector("#conteudo-direita-hearder")
// const logado = document.querySelector("#conteudo-direita-hearder_login")

const login = document.querySelector('#login')
const cadastro = document.querySelector("#cadastro")

login.addEventListener("click", () => {
    Naologado.style.display="none"
    logado.style.display="block"
    document.body.style.overflow = show ? "hidden" : "initial"
})
