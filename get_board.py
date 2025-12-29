import chess
import random

# Helper functions

# Check if a knight at knight_square attacks target_square
def knight_attacks(knight_square, target_square):
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    knight_file = chess.square_file(knight_square)
    knight_rank = chess.square_rank(knight_square)
    target_file = chess.square_file(target_square)
    target_rank = chess.square_rank(target_square)

    for df, dr in knight_moves:
        if (knight_file + df == target_file) and (knight_rank + dr == target_rank):
            return True
    return False

# Scenario 1: King vs King and Pawn
def scenario_king_vs_king_and_pawn():
    board = chess.Board()
    board.clear_board()

    while True:

        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))

        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Pawn (not on 1st or 8th rank, not same as either king)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn_square = random.choice(possible_pawn_squares)

        # Check that pawn isn’t attacking the black king (so not illegal “check”)
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        # A white pawn attacks diagonally forward
        if chess.square_rank(white_pawn_square) < 7:
            file = chess.square_file(white_pawn_square)
            rank = chess.square_rank(white_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank + 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank + 1))

        if black_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_pawn_square, chess.Piece(chess.PAWN, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

# Scenario 2: King and Rook vs King
def scenario_king_and_rook_vs_king():
    board = chess.Board()
    board.clear_board()

    while True:

        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))

        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Rook (not same as either king)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)

        # Check that rook isn’t attacking the black king (so not illegal “check”)
        if chess.square_file(white_rook_square) == chess.square_file(black_king_square) or chess.square_rank(white_rook_square) == chess.square_rank(black_king_square):
            continue  # illegal — rook attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

# Sceario 3: King and Queen vs King
def scenario_king_and_queen_vs_king():
    board = chess.Board()
    board.clear_board()

    while True:

        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))

        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)

        # Check that queen isn’t attacking the black king (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square))):
            continue  # illegal — queen attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))

        # Success: found a valid simple position
        break

    return board


# Scenario 4: King, Queeen and Rook vs King
def scenario_king_queen_rook_vs_king():
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place White Rook (not same as either king or queen)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)

        # Check that queen and rook aren’t attacking the black king (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square)):
            continue  # illegal — queen or rook attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))

        # Success: found a valid simple position
        break  

    return board

# Scenario 5: King and Two Rooks vs King
def scenario_king_and_two_rooks_vs_king():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Rook 1 (not same as either king)
        possible_rook1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook1_square = random.choice(possible_rook1_squares)
        # Place White Rook 2 (not same as either king or rook 1)
        possible_rook2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook1_square]
        ]
        white_rook2_square = random.choice(possible_rook2_squares)

        # Check that rooks aren’t attacking the black king (so not illegal “check”)
        if (chess.square_file(white_rook1_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook1_square) == chess.square_rank(black_king_square) or
            chess.square_file(white_rook2_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook2_square) == chess.square_rank(black_king_square)):
            continue  # illegal — rook attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook1_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(white_rook2_square, chess.Piece(chess.ROOK, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

#Scenario 6: King and two Bishops vs King
def scenario_king_and_two_bishops_vs_king():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Bishop 1 (not same as either king)
        possible_bishop1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_bishop1_square = random.choice(possible_bishop1_squares)
        # Place White Bishop 2 (not same as either king or bishop 1)
        possible_bishop2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_bishop1_square]
        ]
        white_bishop2_square = random.choice(possible_bishop2_squares)

        # Check that bishops aren’t attacking the black king (so not illegal “check”)
        if (abs(chess.square_file(white_bishop1_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_bishop1_square) - chess.square_rank(black_king_square)) or
            abs(chess.square_file(white_bishop2_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_bishop2_square) - chess.square_rank(black_king_square))):
            continue  # illegal — bishop attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_bishop1_square, chess.Piece(chess.BISHOP, chess.WHITE))
        board.set_piece_at(white_bishop2_square, chess.Piece(chess.BISHOP, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

# Scenario 7: King, Knight and Bishop vs King
def scenario_king_knight_bishop_vs_king():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Knight (not same as either king)
        possible_knight_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_knight_square = random.choice(possible_knight_squares)
        # Place White Bishop (not same as either king or knight)
        possible_bishop_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_knight_square]
        ]
        white_bishop_square = random.choice(possible_bishop_squares)

        # Check that knight and bishop aren’t attacking the black king (so not illegal “check”)
        if (knight_attacks(white_knight_square, black_king_square) or
            abs(chess.square_file(white_bishop_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_bishop_square) - chess.square_rank(black_king_square))):
            continue  # illegal — knight or bishop attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_knight_square, chess.Piece(chess.KNIGHT, chess.WHITE))
        board.set_piece_at(white_bishop_square, chess.Piece(chess.BISHOP, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

# Scenario 8: King and Queen vs King and Bishop
def scenario_king_queen_vs_king_bishop():
    
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Bishop (not same as either king or queen)
        possible_bishop_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_bishop_square = random.choice(possible_bishop_squares)

        # Check that queen and bishop aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            abs(chess.square_file(black_bishop_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop_square) - chess.square_rank(white_king_square))):
            continue  # illegal — queen or bishop attacking king

        # check that the black bishop is not attacking the white king
        if (abs(chess.square_file(black_bishop_square) - chess.square_file(white_king_square)) == 
            abs(chess.square_rank(black_bishop_square) - chess.square_rank(white_king_square))):
            continue  # illegal — bishop attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at( black_bishop_square, chess.Piece(chess.BISHOP, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 9: King and Queen Vs King and Knight
def scenario_king_queen_vs_king_knight():
    
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Knight (not same as either king or queen)
        possible_knight_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_knight_square = random.choice(possible_knight_squares)

        # Check that queen and knight aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            knight_attacks(black_knight_square, white_king_square)):
            continue  # illegal — queen or knight attacking king

        # Check that the black knight is not attacking the white king
        if knight_attacks(black_knight_square, white_king_square):
            continue  # illegal — knight attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at( black_knight_square, chess.Piece(chess.KNIGHT, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 10: King and Queen vs King and Rook
def scenario_king_queen_vs_king_rook():
    
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Rook (not same as either king or queen)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_rook_square = random.choice(possible_rook_squares)

        # Check that queen and rook aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            chess.square_file(black_rook_square) == chess.square_file(white_king_square) or
            chess.square_rank(black_rook_square) == chess.square_rank(white_king_square)):
            continue  # illegal — queen or rook attacking king

        # Check that the black rook is not attacking the white king
        if (chess.square_file(black_rook_square) == chess.square_file(white_king_square) or
            chess.square_rank(black_rook_square) == chess.square_rank(white_king_square)):
            continue  # illegal — rook attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at( black_rook_square, chess.Piece(chess.ROOK, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 11: King and Queen vs King, Knight and Bishop
def scenario_king_queen_vs_king_knight_bishop():
    
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Knight (not same as either king or queen)
        possible_knight_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_knight_square = random.choice(possible_knight_squares)
        # Place Black Bishop (not same as either king, queen or knight)
        possible_bishop_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square, black_knight_square]
        ]
        black_bishop_square = random.choice(possible_bishop_squares)

        # Check that queen, knight and bishop aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            knight_attacks(black_knight_square, white_king_square) or
            abs(chess.square_file(black_bishop_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop_square) - chess.square_rank(white_king_square))):
            continue  # illegal — queen, knight or bishop attacking king
        
        # Check that the black knight and bishop are not attacking the white king
        if (knight_attacks(black_knight_square, white_king_square) or
            abs(chess.square_file(black_bishop_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop_square) - chess.square_rank(white_king_square))):
            continue  # illegal — knight or bishop attacking king   

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at( black_knight_square, chess.Piece(chess.KNIGHT, chess.BLACK))
        board.set_piece_at( black_bishop_square, chess.Piece(chess.BISHOP, chess.BLACK))

        # Success: found a valid simple position
        break   

    return board

#Scenario 12: King and Queen vs King and two knights
def scenario_king_queen_vs_king_two_knights(): 

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Knight 1 (not same as either king or queen)
        possible_knight1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_knight1_square = random.choice(possible_knight1_squares)
        # Place Black Knight 2 (not same as either king, queen or knight 1)
        possible_knight2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square, black_knight1_square]
        ]
        black_knight2_square = random.choice(possible_knight2_squares)

        # Check that queen and knights aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            knight_attacks(black_knight1_square, white_king_square) or
            knight_attacks(black_knight2_square, white_king_square)):
            continue  # illegal — queen or knight attacking king

        # Check that the black knights are not attacking the white king
        if (knight_attacks(black_knight1_square, white_king_square) or
            knight_attacks(black_knight2_square, white_king_square)):
            continue  # illegal — knight attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at(black_knight1_square, chess.Piece(chess.KNIGHT, chess.BLACK))
        board.set_piece_at(black_knight2_square, chess.Piece(chess.KNIGHT, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 13: King and Queen vs King and two bishops
def scenario_king_queen_vs_king_two_bishops():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Bishop 1 (not same as either king or queen)
        possible_bishop1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_bishop1_square = random.choice(possible_bishop1_squares)
        # Place Black Bishop 2 (not same as either king, queen or bishop 1)
        possible_bishop2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square, black_bishop1_square]
        ]
        black_bishop2_square = random.choice(possible_bishop2_squares)

        # Check that queen and bishops aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            abs(chess.square_file(black_bishop1_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop1_square) - chess.square_rank(white_king_square)) or
            abs(chess.square_file(black_bishop2_square) - chess.square_file(white_king_square)) == 
            abs(chess.square_rank(black_bishop2_square) - chess.square_rank(white_king_square))):
            continue  # illegal — queen or bishop attacking king

        # Check that the black bishops are not attacking the white king
        if (abs(chess.square_file(black_bishop1_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop1_square) - chess.square_rank(white_king_square)) or
            abs(chess.square_file(black_bishop2_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop2_square) - chess.square_rank(white_king_square))):
            continue  # illegal — bishop attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at(black_bishop1_square, chess.Piece(chess.BISHOP, chess.BLACK))
        board.set_piece_at(black_bishop2_square, chess.Piece(chess.BISHOP, chess.BLACK))    

        # Success: found a valid simple position
        break   

    return board

# Scenario 14: King and two pawns vs King
def scenario_king_and_two_pawns_vs_king():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Pawn 1 (not on 1st or 8th rank, not same as either king)
        possible_pawn1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn1_square = random.choice(possible_pawn1_squares)
        # Place White Pawn 2 (not on 1st or 8th rank, not same as either king or pawn 1)
        possible_pawn2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_pawn1_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn2_square = random.choice(possible_pawn2_squares)

        # Check that pawns aren’t attacking the black king (so not illegal “check”)
        pawn1_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        pawn2_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        # A white pawn attacks diagonally forward
        for pawn_square, attack_squares in [(white_pawn1_square, pawn1_attack_squares), (white_pawn2_square, pawn2_attack_squares)]:
            if chess.square_rank(pawn_square) < 7:
                file = chess.square_file(pawn_square)
                rank = chess.square_rank(pawn_square)
                if file > 0:
                    attack_squares.append(chess.square(file - 1, rank + 1))
                if file < 7:
                    attack_squares.append(chess.square(file + 1, rank + 1))

        if black_king_square in pawn1_attack_squares or black_king_square in pawn2_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_pawn1_square, chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(white_pawn2_square, chess.Piece(chess.PAWN, chess.WHITE))    

        # Success: found a valid simple position
        break   

    return board

#Scenario 15: King and Bishop vs King and Pawn
def scenario_king_bishop_vs_king_pawn():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)

        # Place White Bishop (not same as either king)
        possible_bishop_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_bishop_square = random.choice(possible_bishop_squares)
        # Place Black Pawn (not on 1st or 8th rank, not same as either king or bishop)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_bishop_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn_square = random.choice(possible_pawn_squares)

        # Check that bishop and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (abs(chess.square_file(white_bishop_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_bishop_square) - chess.square_rank(black_king_square))):
            continue  # illegal — bishop attacking king

        # A black pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(black_pawn_square) > 0:
            file = chess.square_file(black_pawn_square)
            rank = chess.square_rank(black_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank - 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank - 1))

        if white_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_bishop_square, chess.Piece(chess.BISHOP, chess.WHITE))
        board.set_piece_at(black_pawn_square, chess.Piece(chess.PAWN, chess.BLACK)) 

        # Success: found a valid simple position
        break   

    return board

# Scenario 16: King and Knight vs King and Pawn
def scenario_king_knight_vs_king_pawn():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)   
        # Place White Knight (not same as either king)
        possible_knight_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_knight_square = random.choice(possible_knight_squares)
        # Place Black Pawn (not on 1st or 8th rank, not same as either king or knight)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_knight_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn_square = random.choice(possible_pawn_squares)

        # Check that knight and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (knight_attacks(white_knight_square, black_king_square)):
            continue  # illegal — knight attacking king

        # A black pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(black_pawn_square) > 0:    
            file = chess.square_file(black_pawn_square)
            rank = chess.square_rank(black_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank - 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank - 1))
            
        if white_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_knight_square, chess.Piece(chess.KNIGHT, chess.WHITE))
        board.set_piece_at(black_pawn_square, chess.Piece(chess.PAWN, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

#Scenario 17: King and Rook vs King and Pawn
def scenario_king_rook_vs_king_pawn():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)
        # Place Black Pawn (not on 1st or 8th rank, not same as either king or rook)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn_square = random.choice(possible_pawn_squares)

        # Check that rook and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square)):
            continue  # illegal — rook attacking king

        # A black pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(black_pawn_square) > 0:    
            file = chess.square_file(black_pawn_square)
            rank = chess.square_rank(black_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank - 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank - 1))

        if white_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king   

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_pawn_square, chess.Piece(chess.PAWN, chess.BLACK))

        # Success: found a valid simple position
        break   

    return board

# Scenario 18: King and Queen Vs King and Pawn
def scenario_king_queen_vs_king_pawn():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Queen (not same as either king)
        possible_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_queen_squares)
        # Place Black Pawn (not on 1st or 8th rank, not same as either king or queen)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn_square = random.choice(possible_pawn_squares)

        # Check that queen and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square))):
            continue  # illegal — queen attacking king

        # A black pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(black_pawn_square) > 0:    
            file = chess.square_file(black_pawn_square)
            rank = chess.square_rank(black_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank - 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank - 1))

        if white_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at(black_pawn_square, chess.Piece(chess.PAWN, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 19: King, Queen and Pawn vs King and Queen
def scenario_king_queen_pawn_vs_king_queen():
    
    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Queen (not same as either king)
        possible_white_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_queen_square = random.choice(possible_white_queen_squares)
        # Place Black Queen (not same as either king or white queen)
        possible_black_queen_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square]
        ]
        black_queen_square = random.choice(possible_black_queen_squares)
        # Place White Pawn (not on 1st or 8th rank, not same as either king or either queen)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_queen_square, black_queen_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn_square = random.choice(possible_pawn_squares)

        # Check that queens and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_queen_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_queen_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(white_queen_square) - chess.square_file(black_king_square)) ==
            abs(chess.square_rank(white_queen_square) - chess.square_rank(black_king_square)) or
            chess.square_file(black_queen_square) == chess.square_file(white_king_square) or
            chess.square_rank(black_queen_square) == chess.square_rank(white_king_square) or
            abs(chess.square_file(black_queen_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_queen_square) - chess.square_rank(white_king_square))):
            continue  # illegal — queen attacking king

        # A white pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(white_pawn_square) < 7:    
            file = chess.square_file(white_pawn_square)
            rank = chess.square_rank(white_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank + 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank + 1))

        if black_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_queen_square, chess.Piece(chess.QUEEN, chess.WHITE))
        board.set_piece_at(black_queen_square, chess.Piece(chess.QUEEN, chess.BLACK))
        board.set_piece_at(white_pawn_square, chess.Piece(chess.PAWN, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

# Scenario 20: King and two pawns vs King and pawn
def scenario_king_two_pawns_vs_king_pawn():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Pawn 1 (not on 1st or 8th rank, not same as either king)
        possible_white_pawn1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn1_square = random.choice(possible_white_pawn1_squares)
        # Place White Pawn 2 (not on 1st or 8th rank, not same as either king or white pawn 1)
        possible_white_pawn2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_pawn1_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn2_square = random.choice(possible_white_pawn2_squares)
        # Place Black Pawn (not on 1st or 8th rank, not same as either king or either white pawn)
        possible_black_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_pawn1_square, white_pawn2_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn_square = random.choice(possible_black_pawn_squares)

        # Check that pawns aren’t attacking the opposing kings (so not illegal “check”)
        white_pawn1_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        white_pawn2_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        # A white pawn attacks diagonally forward
        for pawn_square, attack_squares in [(white_pawn1_square, white_pawn1_attack_squares), (white_pawn2_square, white_pawn2_attack_squares)]:
            if chess.square_rank(pawn_square) < 7:
                file = chess.square_file(pawn_square)
                rank = chess.square_rank(pawn_square)
                if file > 0:
                    attack_squares.append(chess.square(file - 1, rank + 1))
                if file < 7:
                    attack_squares.append(chess.square(file + 1, rank + 1))
        if black_king_square in white_pawn1_attack_squares or black_king_square in white_pawn2_attack_squares:
            continue  # illegal — white pawn attacking black king

        # A black pawn attacks diagonally forward
        black_pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(black_pawn_square) > 0:    
            file = chess.square_file(black_pawn_square)
            rank = chess.square_rank(black_pawn_square)
            if file > 0:
                black_pawn_attack_squares.append(chess.square(file - 1, rank - 1))
            if file < 7:
                black_pawn_attack_squares.append(chess.square(file + 1, rank - 1))
        if white_king_square in black_pawn_attack_squares:
            continue  # illegal — black pawn attacking white king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_pawn1_square, chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(white_pawn2_square, chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(black_pawn_square, chess.Piece(chess.PAWN, chess.BLACK)) 

        # Success: found a valid simple position
        break

    return board

# Scenario 21: King, Pawn and Rook vs King and Rook
def scenario_king_pawn_rook_vs_king_rook():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_white_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_white_rook_squares)
        # Place Black Rook (not same as either king or white rook)
        possible_black_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
        ]
        black_rook_square = random.choice(possible_black_rook_squares)
        # Place White Pawn (not on 1st or 8th rank, not same as either king or either rook)
        possible_pawn_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square, black_rook_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn_square = random.choice(possible_pawn_squares)

        # Check that rooks and pawn aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square) or
            chess.square_file(black_rook_square) == chess.square_file(white_king_square) or
            chess.square_rank(black_rook_square) == chess.square_rank(white_king_square)):
            continue  # illegal — rook attacking king

        # A white pawn attacks diagonally forward
        pawn_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        if chess.square_rank(white_pawn_square) < 7:    
            file = chess.square_file(white_pawn_square)
            rank = chess.square_rank(white_pawn_square)
            if file > 0:
                pawn_attack_squares.append(chess.square(file - 1, rank + 1))
            if file < 7:
                pawn_attack_squares.append(chess.square(file + 1, rank + 1))
        if black_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Check that black pawn is not attacking white king
        if white_king_square in pawn_attack_squares:
            continue  # illegal — pawn attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_rook_square, chess.Piece(chess.ROOK, chess.BLACK))
        board.set_piece_at(white_pawn_square, chess.Piece(chess.PAWN, chess.WHITE))

        # Success: found a valid simple position
        break

    return board    

# Scenario 22: King, Two Pawns and Rook vs King and Rook
def scenario_king_two_pawns_rook_vs_king_rook():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_white_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_white_rook_squares)
        # Place Black Rook (not same as either king or white rook)
        possible_black_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
        ]
        black_rook_square = random.choice(possible_black_rook_squares)
        # Place White Pawn 1 (not on 1st or 8th rank, not same as either king or either rook)
        possible_white_pawn1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square, black_rook_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn1_square = random.choice(possible_white_pawn1_squares)
        # Place White Pawn 2 (not on 1st or 8th rank, not same as either king, either rook or white pawn 1)
        possible_white_pawn2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square, black_rook_square, white_pawn1_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        white_pawn2_square = random.choice(possible_white_pawn2_squares)

        # Check that rooks and pawns aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square) or
            chess.square_file(black_rook_square) == chess.square_file(white_king_square) or
            chess.square_rank(black_rook_square) == chess.square_rank(white_king_square)):
            continue  # illegal — rook attacking king

        white_pawn1_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        white_pawn2_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        # A white pawn attacks diagonally forward
        for pawn_square, attack_squares in [(white_pawn1_square, white_pawn1_attack_squares), (white_pawn2_square, white_pawn2_attack_squares)]:
            if chess.square_rank(pawn_square) < 7:
                file = chess.square_file(pawn_square)
                rank = chess.square_rank(pawn_square)
                if file > 0:
                    attack_squares.append(chess.square(file - 1, rank + 1))
                if file < 7:
                    attack_squares.append(chess.square(file + 1, rank + 1))
        if black_king_square in white_pawn1_attack_squares or black_king_square in white_pawn2_attack_squares:
            continue  # illegal — white pawn attacking black king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_rook_square, chess.Piece(chess.ROOK, chess.BLACK))
        board.set_piece_at(white_pawn1_square, chess.Piece(chess.PAWN, chess.WHITE))
        board.set_piece_at(white_pawn2_square, chess.Piece(chess.PAWN, chess.WHITE))

        # Success: found a valid simple position
        break

    return board

#Scenario 23: King and Rook vs King and Bishop
def scenario_king_rook_vs_king_bishop():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)
        # Place Black Bishop (not same as either king or rook)
        possible_bishop_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
        ]
        black_bishop_square = random.choice(possible_bishop_squares)

        # Check that rook and bishop aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square) or
            abs(chess.square_file(black_bishop_square) - chess.square_file(white_king_square)) ==
            abs(chess.square_rank(black_bishop_square) - chess.square_rank(white_king_square))):
            continue  # illegal — rook or bishop attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_bishop_square, chess.Piece(chess.BISHOP, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

# Scenario 24: King and Rook Vs King and knight
def scenario_king_rook_vs_king_knight():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)
        # Place Black Knight (not same as either king or rook)
        possible_knight_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
        ]
        black_knight_square = random.choice(possible_knight_squares)

        # Check that rook and knight aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square) or
            knight_attacks(black_knight_square, white_king_square)):
            continue  # illegal — rook or knight attacking king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_knight_square, chess.Piece(chess.KNIGHT, chess.BLACK))

        # Success: found a valid simple position
        break

    return board

#Scenario 25: King and Rook vs King and pawn
def scenario_king_rook_vs_king_two_pawns():

    board = chess.Board()
    board.clear_board()

    while True:
        board.clear_board()
        # Place White King
        white_king_square = random.choice(list(chess.SQUARES))
        # Place Black King (not same and not adjacent)
        possible_black_squares = [
            sq for sq in chess.SQUARES
            if sq != white_king_square and chess.square_distance(sq, white_king_square) > 1
        ]
        black_king_square = random.choice(possible_black_squares)
        # Place White Rook (not same as either king)
        possible_rook_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square]
        ]
        white_rook_square = random.choice(possible_rook_squares)
        # Place Black Pawn 1 (not on 1st or 8th rank, not same as either king or rook)
        possible_pawn1_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn1_square = random.choice(possible_pawn1_squares)
        # Place Black Pawn 2 (not on 1st or 8th rank, not same as either king, rook or black pawn 1)
        possible_pawn2_squares = [
            sq for sq in chess.SQUARES
            if sq not in [white_king_square, black_king_square, white_rook_square, black_pawn1_square]
            and 0 < chess.square_rank(sq) < 7
        ]
        black_pawn2_square = random.choice(possible_pawn2_squares)

        # Check that rook and pawns aren’t attacking the opposing kings (so not illegal “check”)
        if (chess.square_file(white_rook_square) == chess.square_file(black_king_square) or
            chess.square_rank(white_rook_square) == chess.square_rank(black_king_square)):
            continue  # illegal — rook attacking king

        black_pawn1_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        black_pawn2_attack_squares = list(chess.SquareSet(chess.BB_EMPTY))
        # A black pawn attacks diagonally forward
        for pawn_square, attack_squares in [(black_pawn1_square, black_pawn1_attack_squares), (black_pawn2_square, black_pawn2_attack_squares)]:
            if chess.square_rank(pawn_square) > 0:
                file = chess.square_file(pawn_square)
                rank = chess.square_rank(pawn_square)
                if file > 0:
                    attack_squares.append(chess.square(file - 1, rank - 1))
                if file < 7:
                    attack_squares.append(chess.square(file + 1, rank - 1))
        if white_king_square in black_pawn1_attack_squares or white_king_square in black_pawn2_attack_squares:
            continue  # illegal — black pawn attacking white king

        # Construct board
        board.clear_board()
        board.set_piece_at(white_king_square, chess.Piece(chess.KING, chess.WHITE))
        board.set_piece_at(black_king_square, chess.Piece(chess.KING, chess.BLACK))
        board.set_piece_at(white_rook_square, chess.Piece(chess.ROOK, chess.WHITE))
        board.set_piece_at(black_pawn1_square, chess.Piece(chess.PAWN, chess.BLACK))
        board.set_piece_at(black_pawn2_square, chess.Piece(chess.PAWN, chess.BLACK))

        # Success: found a valid simple position
        break

    return board


SCENARIO_MAP = {
    1: scenario_king_vs_king_and_pawn,
    2: scenario_king_and_rook_vs_king,
    3: scenario_king_and_queen_vs_king,
    4: scenario_king_queen_rook_vs_king,
    5: scenario_king_and_two_rooks_vs_king,
    6: scenario_king_and_two_bishops_vs_king,
    7: scenario_king_knight_bishop_vs_king,
    8: scenario_king_queen_vs_king_bishop,
    9: scenario_king_queen_vs_king_knight,
    10: scenario_king_queen_vs_king_rook,
    11: scenario_king_queen_vs_king_knight_bishop,
    12: scenario_king_queen_vs_king_two_knights,
    13: scenario_king_queen_vs_king_two_bishops,
    14: scenario_king_and_two_pawns_vs_king,
    15: scenario_king_bishop_vs_king_pawn,
    16: scenario_king_knight_vs_king_pawn,
    17: scenario_king_rook_vs_king_pawn,
    18: scenario_king_queen_vs_king_pawn,
    19: scenario_king_queen_pawn_vs_king_queen,
    20: scenario_king_two_pawns_vs_king_pawn,
    21: scenario_king_pawn_rook_vs_king_rook,
    22: scenario_king_two_pawns_rook_vs_king_rook,
    23: scenario_king_rook_vs_king_bishop,
    24: scenario_king_rook_vs_king_knight,
    25: scenario_king_rook_vs_king_two_pawns,
}
# Scenario Dispatcher
def get_scenario_board(scenario_number, n):

    selected_scenario = SCENARIO_MAP.get(scenario_number)
    selected_scenario_name = selected_scenario.__name__ 

    unique_boards = set()
    boards = []

    attempts = 0
    max_attempts = n * 100

    while len(boards) < n and attempts < max_attempts:
        board = selected_scenario()
        board_fen = board.fen()
        if board_fen not in unique_boards:
            unique_boards.add(board_fen)
            boards.append(board)
        attempts += 1

    if len(boards) < n:
        print(f"Warning: Only generated {len(boards)} unique boards out of requested {n} for scenario {scenario_number} ({selected_scenario_name}).")

    return boards

def get_boards():

    all_boards = []
    for i in range(1, 26):
        boards = get_scenario_board(i, 100)
        all_boards.extend(boards)

    return all_boards