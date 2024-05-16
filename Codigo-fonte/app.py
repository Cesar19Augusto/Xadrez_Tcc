from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def is_valid_move(piece, start_square, end_square, board):
    """
    Verifica se um movimento de uma peça é válido de acordo com as regras do xadrez.

    Args:
    - piece: A peça que está sendo movida.
    - start_square: O quadrado de onde a peça está sendo movida.
    - end_square: O quadrado para onde a peça está sendo movida.
    - board: O estado atual do tabuleiro.

    Returns:
    - True se o movimento for válido, False caso contrário.
    """

    # Verifica se a peça está no quadrado de início
    if board[start_square] != piece:
        return False

    # Obtém o tipo de peça
    piece_type = piece[0]

    # Implementa a lógica de movimento para cada tipo de peça
    if piece_type == 'P':  # Peão
        return is_valid_pawn_move(start_square, end_square, board)
    elif piece_type == 'R':  # Torre
        return is_valid_rook_move(start_square, end_square, board)
    elif piece_type == 'N':  # Cavalo
        return is_valid_knight_move(start_square, end_square, board)
    elif piece_type == 'B':  # Bispo
        return is_valid_bishop_move(start_square, end_square, board)
    elif piece_type == 'Q':  # Rainha
        return is_valid_queen_move(start_square, end_square, board)
    elif piece_type == 'K':  # Rei
        return is_valid_king_move(start_square, end_square, board)
    
    # Se a peça não for reconhecida, o movimento é inválido
    return False


# Lógica de Movimento para o Peão
def is_valid_pawn_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é um peão
    if board[start_square][0] != 'P':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se o peão está se movendo na direção correta (dependendo da cor)
    if board[start_square][1] == 'W':
        direction = -1  # Peão branco move-se para cima do tabuleiro
        start_row -= 1  # Atualiza a posição de início para a fileira correta
    else:
        direction = 1  # Peão preto move-se para baixo do tabuleiro
        start_row += 1  # Atualiza a posição de início para a fileira correta
    
    # Verifica se o movimento é um avanço de um quadrado
    if end_row == start_row + direction and end_col == start_col and board[end_square] == '.':
        return True
    
    # Verifica se o movimento é um avanço de dois quadrados a partir da posição inicial
    if (start_row == 6 and end_row == start_row + 2 * direction and end_col == start_col
            and board[start_square + direction * 8] == '.' and board[end_square] == '.'):
        return True
    
    # Verifica se o movimento é uma captura diagonal
    if abs(end_col - start_col) == 1 and end_row == start_row + direction:
        target_piece = board[end_square]
        if target_piece != '.' and target_piece[1] != board[start_square][1]:
            return True
    
    return False


# Lógica de Movimento para a Torre
def is_valid_rook_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é uma torre
    if board[start_square][0] != 'R':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se a torre está se movendo na mesma fileira ou coluna
    if start_row == end_row or start_col == end_col:
        return True
    
    return False


# Lógica de Movimento para o Cavalo
def is_valid_knight_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é um cavalo
    if board[start_square][0] != 'N':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se o movimento do cavalo é em forma de L
    delta_row = abs(start_row - end_row)
    delta_col = abs(start_col - end_col)
    if (delta_row == 1 and delta_col == 2) or (delta_row == 2 and delta_col == 1):
        return True
    
    return False


# Lógica de Movimento para o Bispo
def is_valid_bishop_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é um bispo
    if board[start_square][0] != 'B':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se o bispo está se movendo na diagonal
    if abs(start_row - end_row) == abs(start_col - end_col):
        return True
    
    return False


# Lógica de Movimento para a Rainha
def is_valid_queen_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é uma rainha
    if board[start_square][0] != 'Q':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se a rainha está se movendo na mesma fileira, coluna ou diagonal
    if (start_row == end_row or start_col == end_col or
            abs(start_row - end_row) == abs(start_col - end_col)):
        return True
    
    return False


# Lógica de Movimento para o Rei
def is_valid_king_move(start_square, end_square, board):
    # Verifica se a peça na posição de início é um rei
    if board[start_square][0] != 'K':
        return False
    
    # Obtém a fileira e a coluna da posição de início e de destino
    start_row, start_col = start_square // 8, start_square % 8
    end_row, end_col = end_square // 8, end_square % 8
    
    # Verifica se o rei está se movendo para uma casa adjacente
    delta_row = abs(start_row - end_row)
    delta_col = abs(start_col - end_col)
    if delta_row <= 1 and delta_col <= 1:
        return True
    
    return False


@app.route('/move', methods=['POST'])
def get_next_move():
    # Obtem a posição atual do tabuleiro enviada pelo front-end
    data = request.get_json()
    current_position = data.get('position')

    # Chama a função para obter o movimento sugerido do Stockfish
    next_move = get_stockfish_move(current_position)

    # Retorna o movimento sugerido ao front-end
    return jsonify({'move': next_move})

def get_stockfish_move(position):
    # Inicia o Stockfish como um processo subprocesso
    stockfish_process = subprocess.Popen(
        ['stockfish'],  # Path para o executável do Stockfish, ajuste conforme necessário
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # Envia a posição do tabuleiro para o Stockfish e obtém o movimento sugerido
    stockfish_process.stdin.write(f'position fen {position}\n')
    stockfish_process.stdin.write('go depth 1\n')
    stockfish_process.stdin.flush()
    output = stockfish_process.stdout.readline().strip()

    # Analisa a saída do Stockfish para obter o movimento sugerido
    if output.startswith('bestmove'):
        next_move = output.split(' ')[1]
        return next_move
    else:
        # Em caso de erro ou falha, retorna um movimento vazio
        return ''

if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask em modo de depuração
