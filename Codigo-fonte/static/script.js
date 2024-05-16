document.addEventListener("DOMContentLoaded", function() {
    const board = document.querySelector('.board');
    let selectedPiece = null;

    // Adiciona as casas do tabuleiro
    for (let i = 0; i < 64; i++) {
        const square = document.createElement('div');
        square.classList.add('square');
        square.dataset.index = i;
        square.addEventListener('click', handleSquareClick);
        board.appendChild(square);
    }

    // Adiciona as imagens das peças aos quadrados
    const pieceImages = [
        "Torree_Preto.png", "Cavalo_Preto.png", "Bispo_Preto.png", "Rainha_Preto.png", "Rei_Preto.png", "Bispo_Preto.png", "Cavalo_Preto.png", "Torree_Preto.png",
        "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png", "Peão_Preto.png",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png", "Peão_Branco.png",
        "Torre_Branco.png", "Cavalo_Branco.png", "Bispo_Branco.png", "Rainha_Branco.png", "Rei_Branco.png", "Bispo_Branco.png", "Cavalo_Branco.png", "Torre_Branco.png"
    ];

    for (let i = 0; i < pieceImages.length; i++) {
        if (pieceImages[i] !== "") {
            const pieceImage = document.createElement('img');
            pieceImage.classList.add('piece');
            pieceImage.src = "../img/" + pieceImages[i];
            board.children[i].appendChild(pieceImage);
        }
    }

    // Define a função para lidar com o clique em uma casa do tabuleiro
    function handleSquareClick() {
        const selectedIndex = parseInt(this.dataset.index);
        console.log('Casa selecionada:', selectedIndex);
        
        // Verifica se já há uma peça selecionada
        if (selectedPiece !== null) {
            // Move a peça para a casa selecionada
            const selectedSquare = board.querySelector(`.square[data-index="${selectedIndex}"]`);
            selectedSquare.appendChild(selectedPiece);
            selectedPiece = null; // Reseta a peça selecionada para null
        } else {
            // Se não houver peça selecionada, seleciona a peça da casa clicada
            const piece = this.querySelector('.piece');
            if (piece !== null) {
                selectedPiece = piece;
            }
        }
    }

    // Função para enviar a posição atual do tabuleiro para o Flask e receber o próximo movimento sugerido
    async function getNextMoveFromBackend(currentPosition) {
        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ position: currentPosition })
            });
            const data = await response.json();
            return data.move; // Retorna o próximo movimento sugerido
        } catch (error) {
            console.error('Erro ao obter próximo movimento do back-end:', error);
            return null;
        }
    }

    // Função para processar o próximo movimento sugerido pela IA
    async function processNextMove() {
        // Aqui você precisa implementar a lógica para obter a posição atual do tabuleiro
        // e convertê-la em um formato que possa ser enviado para o back-end (por exemplo, uma string FEN)
        const currentPosition = '...'; // Defina a posição atual do tabuleiro
        
        // Chama a função para obter o próximo movimento sugerido do back-end Flask
        const nextMove = await getNextMoveFromBackend(currentPosition);
        
        // Aqui você precisa implementar a lógica para processar o próximo movimento sugerido
        // e atualizar o tabuleiro de acordo
        console.log('Próximo movimento sugerido:', nextMove);
    }

    // Chama a função para processar o próximo movimento ao carregar a página
    document.addEventListener('DOMContentLoaded', processNextMove);
});
