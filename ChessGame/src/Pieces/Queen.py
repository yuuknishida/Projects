from .Piece import Piece
from typing import List

class Queen(Piece):
    """Represents a queen piece."""
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        
    def getPossibleMoves(self, board) -> List[tuple]:
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            col = self.col
            row = self.row
            while True:
                col += dx
                row += dy
                if not board.isPositionWithinBoard(col, row):
                    break

                target_piece = board.getPieceAtPosition((col, row))
                if target_piece is None:
                    moves.append((col, row))
                elif target_piece.color != self.color:
                    moves.append((col, row))
                    break
                else:
                    break
        # for move in moves:
        #     print(f"Queen Moves: ({move[0], move[1]})")
        # print("Number of moves: ", len(moves))
        # print("\n")
        return moves
