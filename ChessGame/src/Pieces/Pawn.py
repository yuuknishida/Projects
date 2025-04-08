from typing import List

from .Piece import Piece

class Pawn(Piece):
    """Represents a pawn piece."""
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.hasDoubleMoved = False
        self.enpassantVulnerable = False

    def getPossibleMoves(self, board) -> List[tuple]:
        moves = []
        direction = 1 if self.color == "Black" else -1

        # Single and double move
        single_move = (self.col, self.row + direction)
        if board.isPositionWithinBoard(single_move[0], single_move[1]) and board.getPieceAtPosition(single_move) is None:
            moves.append(single_move)

            if (self.getColor() == "Black" and self.row == 1) or (self.getColor() == "White" and self.row == 6):
                double_move = (self.col, self.row + (direction * 2))
                piece = board.getPieceAtPosition(double_move)
                if not piece:
                    moves.append(double_move)

        # Capture Moves
        for dx in [-1, 1]:
            capture_position = (self.col + dx, self.row + direction)
            possible_capture = board.getPieceAtPosition(capture_position)
            if possible_capture is not None and possible_capture.color != self.color:
                moves.append(capture_position)

        # En Passant Move Code
        if ((self.color == "White" and self.row == 3) or (self.color == "Black" and self.row == 4)):
            for dx in [-1, 1]:
                enpassant_pos = (self.col + dx, self.row)
                if board.isPositionWithinBoard(enpassant_pos[0], enpassant_pos[1]):
                    enpassant_piece = board.getPieceAtPosition(enpassant_pos)
                    if (isinstance(enpassant_piece, Pawn) 
                        and enpassant_piece.color != self.color 
                        and enpassant_piece.enpassantVulnerable):
                        moves.append((enpassant_pos[0], self.row + direction))
        
        # for move in moves:
        #     print(f"Pawn Moves: ({move[0], move[1]})")
        # print("Number of moves: ", len(moves))
        # print("\n")

        return moves