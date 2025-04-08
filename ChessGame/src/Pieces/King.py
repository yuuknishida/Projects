from typing import List

from .Piece import Piece
from .Rook import Rook

class King(Piece):
    """Represents a king piece."""
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.hasTheKingMoved = False
        
    def getPossibleMoves(self, board) -> List[tuple]:
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
                        (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            col = self.col + dx 
            row = self.row + dy
            
            if not board.isPositionWithinBoard(col, row):
                continue

            target_piece = board.getPieceAtPosition((col, row))
            if target_piece is None or target_piece.color != self.color:
                moves.append((col, row))
        
        # Castling
        if not self.hasTheKingMoved:
            # Check for kingside castling
            if self.canCastleKingSide(board):
                moves.append((self.col + 2, self.row))    # Kingside castling

            # Check for queenside castling
            if self.canCastleQueenSide(board):
                moves.append((self.col - 2, self.row))    # Queenside castling

        # for move in moves:
        #     print(f"King Moves: ({move[0]}, {move[1]})")
        # print("Number of moves: ", len(moves))
        # print("\n")

        return moves

    def canCastleKingSide(self, board):
        if self.hasTheKingMoved:
            return False
        # Check if the rook has moved
        rook_position = (7, self.row)    # Rook is 3 squares away
        rook = board.getPieceAtPosition(rook_position)

        if rook is None or not isinstance(rook, Rook) or rook.hasRookMoved:
            return False
        
        # Check squares between king and rook
        for col in range(self.col + 1, 7):
            if board.getPieceAtPosition((col, self.row)) is not None:
                return False
            
        return True
    def canCastleQueenSide(self, board):
        if self.hasTheKingMoved:
            return False
        # Check if the rook has moved
        rook_position = (0, self.row)    # Rook is 4 squares away
        rook = board.getPieceAtPosition(rook_position)
        if rook is None or not isinstance(rook, Rook) or rook.hasRookMoved:
            return False
        
        # Check squares between king and rook
        for col in range(1, self.col):
            if board.getPieceAtPosition((col, self.row)) is not None:
                return False
        
        return True
