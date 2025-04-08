from typing import List

from .Piece import Piece

class Bishop(Piece):
    """Represents a bishop piece."""
    def __init__(self, col, row, color):
        super().__init__(col, row, color)

    def getPossibleMoves(self, board) -> List[tuple]:
        moves = []
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            col = self.col
            row = self.row
            while True:
                col += dx
                row += dy
                if not board.isPositionWithinBoard(col, row):
                    break
                if board.getPieceAtPosition((col, row)) is None:
                    moves.append((col, row))
                elif board.getPieceAtPosition((col, row)).color != self.color:
                    moves.append((col, row))
                    break
                else:
                    break
        # for move in moves:
        #     print(f"Bishop Moves: ({move[0]}, {move[1]})")
        # print("Number of moves: ", len(moves))
        # print("\n")

        return moves