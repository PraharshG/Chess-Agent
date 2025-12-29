import chess
from helper import material_score


def reward_function(board: chess.Board, move: chess.Move | None, turn: bool) -> float:
    
    if move is None:
        return 0.0
    
    temp_board = board.copy()
    if move not in temp_board.legal_moves:
        return -10  
    
    temp_board.push(move)
    
    reward = 0.0

    if temp_board.is_check():
        reward += 2.0

    material_before = material_score(board)
    material_after = material_score(temp_board)
    material_change = material_after - material_before
    
    if turn == chess.WHITE:
        reward += material_change
    else:
        reward -= material_change
    

    if turn == chess.WHITE:
        black_king = temp_board.king(chess.BLACK)
        if black_king:
            file_dist = min(chess.square_file(black_king), 7 - chess.square_file(black_king))
            rank_dist = min(chess.square_rank(black_king), 7 - chess.square_rank(black_king))
            edge_closeness = (7 - file_dist - rank_dist)
            reward += edge_closeness * 0.1  
    else:
        white_king = temp_board.king(chess.WHITE)
        if white_king:
            file_dist = min(chess.square_file(white_king), 7 - chess.square_file(white_king))
            rank_dist = min(chess.square_rank(white_king), 7 - chess.square_rank(white_king))
            edge_closeness = (7 - file_dist - rank_dist)
            reward += edge_closeness * 0.1

    return reward
