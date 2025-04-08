from typing import List

from .Piece import Piece

class Knight(Piece):
    """Represents a knight piece."""
    def __init__(self, col, row, color):
        super().__init__(col, row, color)

    def getPossibleMoves(self, board) -> List[tuple]:
        moves = []
        directions = [(2, 1), (2, -1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)]

        for dx, dy in directions:
            col = self.col + dx
            row = self.row + dy
            
            if not board.isPositionWithinBoard(col, row):    # if position is outside of board break
                continue
            target_piece = board.getPieceAtPosition((col,row))
            if target_piece is None or target_piece.color != self.color:
                moves.append((col, row))

        return moves