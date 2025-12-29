import chess
import torch
import torch.nn as nn
import torch.nn.functional as F

piece_values = {
    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
}

def material_score(board):
    score = 0
    for piece_type, value in piece_values.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def pretty_print_board(fen) -> None:
    fen = fen[0]
    if isinstance(fen, str):
        board = chess.Board(fen)
        board_str = str(board)
        for row in board_str.split("\n"):
            print(row.replace(" ", ""))
    else:
        print(fen)


def board_to_tensor(board):
    tensor = torch.zeros(8, 8, 12, dtype=torch.float32)
    
    piece_idx = {
        chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
        chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
    }
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            rank, file = divmod(square, 8)
           
            channel = piece_idx[piece.piece_type] + (0 if piece.color == chess.WHITE else 6)
            tensor[rank, file, channel] = 1.0
    
    
    return tensor.flatten()

    