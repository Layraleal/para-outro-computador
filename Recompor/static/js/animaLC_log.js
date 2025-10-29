
var btnSignin = document.querySelector("#signin");
var btnSignup = document.querySelector("#signup");

var body = document.querySelector("body");


btnSignin.addEventListener("click", function () {
   body.className = "sign-in-js"; 
});

btnSignup.addEventListener("click", function () {
    body.className = "sign-up-js";
})

/*Elemento de troca de foto*/
'use strict'

let photo = document.getElementById('imgPhoto');
let file = document.getElementById('flImage');

photo.addEventListener('click', () => {
    file.click();
});

file.addEventListener('change', () => {

    if (file.files.length <= 0) {
        return;
    }

    let reader = new FileReader();

    reader.onload = () => {
        photo.src = reader.result;
    }

    reader.readAsDataURL(file.files[0]);
});


//Caixa de mensagem para nome e email- para o usúario digitar um valor válido.
$(function(){
	$('#form_contato').submit(function(){
		var er = new RegExp(/^[A-Za-z0-9_\-\.]+@[A-Za-z0-9_\-\.]{2,}\.[A-Za-z0-9]{2,}(\.[A-Za-z0-9])?/);
		var nome = $('#txt_nome').val();
		var email = $('#txt_email').val();

		if( nome == '' ) { alert('Preencha o campo nome'); return false; }
		if( email == '' || !er.test(email) ) { alert('Preencha o campo email corretamente'); return false; }

		// Se passou por essas validações exibe um alert
		alert( 'formulário enviado com sucesso!' );
	});
});




//Para o usuario digitar uma senha de acordo- até 6 digitos 
//esta no html essa parte, pois por algum motivo não estava funcionando aqui no  jS arquivo por isso foi passado
// para o arquivo CL

//olhinho da senha para mostrar senha e ocultar senha-Cadastro 
 function mostraSenha(){
    var inputPass = document.getElementById('senha')
    var btnShowPass = document.getElementById('btn-senha')

    if(inputPass.type === 'password'){
        inputPass.setAttribute('type','text')
    btnShowPass.classList.replace('bi-eye','bi-eye-slash')
 }else{inputPass.setAttribute('type','password')
 btnShowPass.classList.replace('bi-eye-slash','bi-eye')

 }
 }
//olhinho da senha para mostrar senha e ocultar senha-Cadastro 

 function mostraSenhaCadastro(){
    var inputPass = document.getElementById('password')
    var btnShowPass = document.getElementById('btn-senha-C')

    if(inputPass.type === 'password'){
        inputPass.setAttribute('type','text')
    btnShowPass.classList.replace('bi-eye','bi-eye-slash')
 }else{inputPass.setAttribute('type','password')
 btnShowPass.classList.replace('bi-eye-slash','bi-eye')

 }
 }


 //olhinho da senha para mostrar senha e ocultar senha-Cadastro 
 /*var btn = document.getElementById('signup');
var container = document.querySelector('.imageContainer');
btn.addEventListener('click', function() {
    
  if(container.style.display === 'block') {
      container.style.display = 'none';
  } else {
      container.style.display = 'block';
  }
});
/*var senha = document.formulario.senha;
var regex = /^(?=(?:.*?[A-Z]){1})(?=(?:.*?[0-9]){2})(?=(?:.*?[!@#$%*()_+^&}{:;?.]){1})(?!.*\s)[0-9a-zA-Z!@#$%;*(){}_+^&]*$/; 

if(senha.length < 8)
{
    alert("A senha deve conter no minímo 8 digitos!");
    document.formulario.senha.focus();
    return false;
}
else if(!regex.exec(senha))
{
    alert("A senha deve conter no mínimo 1 caracteres em maiúsculo, 2 números e 1 caractere especial!");
    document.formulario.senha.focus();
    return false;
}
return true;*/