const botaoMensagem = document.getElementById('mostrar-mensagem-btn');
const divMensagem = document.getElementById('mensagem-js');

botaoMensagem.addEventListener('click', () => {
    // Limpa mensagens anteriores
    divMensagem.innerHTML = ''; 

    const novaMensagem = document.createElement('p');
    novaMensagem.textContent = 'Hello World! Bem-vindos ao meu Portfólio!';
    novaMensagem.classList.add('mensagem-animada'); // Adiciona a classe para animar

    divMensagem.appendChild(novaMensagem);

    // Opcional: Remover a mensagem após alguns segundos
    setTimeout(() => {
        novaMensagem.remove();
    }, 5000); 
});