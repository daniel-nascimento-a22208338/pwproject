// Função para obter a data formatada
function obterDataFormatada() {
    const agora = new Date();
    const opcoes = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    return agora.toLocaleDateString('pt-BR', opcoes);
}

// Função para obter o tempo formatado
function obterTempoFormatado() {
    const agora = new Date();
    const opcoes = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    };
    return agora.toLocaleTimeString('pt-BR', opcoes);
}

// Função para atualizar a data e a hora no DOM
function atualizarDataHora() {
    const dataFormatada = obterDataFormatada();
    const tempoFormatado = obterTempoFormatado();
    document.getElementById('data').textContent = dataFormatada;
    document.getElementById('relogio').textContent = tempoFormatado;
}

// Atualiza a data e a hora imediatamente
atualizarDataHora();

// Atualiza a data e a hora a cada segundo
setInterval(atualizarDataHora, 1000);

// Funções e lógica do Tic-Tac-Toe

const cells = document.querySelectorAll('[data-cell]');
const board = document.querySelector('.board');
const restartButton = document.getElementById('restartButton');
const X_CLASS = 'x';
const O_CLASS = 'o';
let oTurn;

// Função para iniciar o jogo
function startGame() {
    oTurn = false;
    cells.forEach(cell => {
        cell.classList.remove(X_CLASS);
        cell.classList.remove(O_CLASS);
        cell.removeEventListener('click', handleClick);
        cell.addEventListener('click', handleClick, { once: true });
    });
    setBoardHoverClass();
}

// Função para tratar o clique na célula
function handleClick(e) {
    const cell = e.target;
    const currentClass = oTurn ? O_CLASS : X_CLASS;
    placeMark(cell, currentClass);
    if (checkWin(currentClass)) {
        endGame(false);
    } else if (isDraw()) {
        endGame(true);
    } else {
        swapTurns();
        setBoardHoverClass();
    }
}

// Função para terminar o jogo
function endGame(draw) {
    if (draw) {
        alert('Empate!');
    } else {
        alert(`${oTurn ? "O's" : "X's"} Venceu!`);
    }
    startGame();
}

// Função para verificar empate
function isDraw() {
    return [...cells].every(cell => {
        return cell.classList.contains(X_CLASS) || cell.classList.contains(O_CLASS);
    });
}

// Função para colocar a marca (X ou O)
function placeMark(cell, currentClass) {
    cell.classList.add(currentClass);
}

// Função para trocar turnos
function swapTurns() {
    oTurn = !oTurn;
}

// Função para definir a classe de hover do tabuleiro
function setBoardHoverClass() {
    board.classList.remove(X_CLASS);
    board.classList.remove(O_CLASS);
    if (oTurn) {
        board.classList.add(O_CLASS);
    } else {
        board.classList.add(X_CLASS);
    }
}

// Função para verificar vitória
function checkWin(currentClass) {
    const WINNING_COMBINATIONS = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];
    return WINNING_COMBINATIONS.some(combination => {
        return combination.every(index => {
            return cells[index].classList.contains(currentClass);
        });
    });
}

// Evento para reiniciar o jogo
restartButton.addEventListener('click', startGame);

// Iniciar o jogo quando a página carregar
window.onload = startGame;
