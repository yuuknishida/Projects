
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem, QMainWindow, QDialog)
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, pyqtSignal

from Pieces.Piece import Piece
from Pieces.Pawn import Pawn
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Queen import Queen

import os
from dataclasses import dataclass
from typing import Any, Optional, List, Dict, Tuple

@dataclass
class SquareData:
    position: Tuple[int, int]
    piece: Any

class ChessBoardManager(QWidget):
    "Manages chess board gui and logic"
    def __init__(self, squareSize = 80):
        super().__init__()
        self.boardGridLayout = QGridLayout()
        self.boardGridLayout.setSpacing(0)
        self.boardGridLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.boardGridLayout)

        self.board: Dict[Tuple[int, int], Optional[Piece]] = {} # internal board matrix
        self.squares = {}   # Visual of individual squares on the board
        self.squareData = []
        self.squareSize = squareSize
        self.whiteKingPosition = (4, 7)
        self.blackKingPosition = (4, 0)
        self.gameHistory = []
        self.movesList = []
        self.isWhiteTurn = True
        self.attackingPieces = set()
        self.attackingPaths = []
        self.lastMove = None
        self.numOfTurns = 0
        self.selectedPiece = None
        self.selectedSquare = None
        self.initialPiecePositions()
    
    def initBoard(self):
        for row in range(8):
            for column in range(8):
                position = (column, row)
                square = self.addSquare(column, row)
                self.boardGridLayout.addWidget(square, row, column)
                self.squares[position] = square

    def update(self):
        for position, square in self.squares.items():
            piece = self.getPieceAtPosition(position)
            square.clear()
            square.piece = piece

            if piece:
                pieceImagePath = f"resources/{piece.getImageName()}"
                if os.path.exists(pieceImagePath):
                    pixmap = QPixmap(pieceImagePath)
                    scaledPixmap = pixmap.scaled(square.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    square.setPixmap(scaledPixmap)
                else:
                    print(f"Error: {pieceImagePath} does not exist.")

    def initialPiecePositions(self):
        initialPiecePositions = [
            (Rook, 0, 0, "Black"), (Knight, 1, 0, "Black"), (Bishop, 2, 0, "Black"), (Queen, 3, 0, "Black"), (King, 4, 0, "Black"), (Bishop, 5, 0, "Black"), (Knight, 6, 0, "Black"), (Rook, 7, 0,"Black"),

            (Rook, 0, 7, "White"), (Knight, 1, 7, "White"), (Bishop, 2, 7, "White"), (Queen, 3, 7, "White"), (King, 4, 7, "White"), (Bishop, 5, 7, "White"), (Knight, 6, 7, "White"), (Rook, 7, 7, "White"),
        ]

        for col in range(7, -1, -1):
            initialPiecePositions.append((Pawn, col, 1, "Black"))
            initialPiecePositions.append((Pawn, col, 6, "White"))

        for pieceClass, col, row, color in initialPiecePositions:
            piece = pieceClass(col, row, color)
            self.board[(col, row)] = piece

        for row in range(2, 6):
            for col in range(8):
                self.board[(col, row)] = None
    
    def initPieces(self):
        for position, piece in self.board.items():
            if piece:
                pieceImagePath = f"resources/{piece.getImageName()}"
                if os.path.exists(pieceImagePath):
                    pixmap = QPixmap(pieceImagePath)
                    scaledPixmap = pixmap.scaled(self.squares[position].size(), Qt.AspectRatioMode.KeepAspectRatio)
                    self.squares[position].setPixmap(scaledPixmap)
                    self.board[position] = piece
                else:
                    print(f"Error: {pieceImagePath} does not exist.")

    def addSquare(self, column, row):
        square = QLabel()
        square.setFixedSize(self.squareSize, self.squareSize)
        square.setFrameShape(QFrame.Shape.Box)

        self.updateSquareBackground(square, position=(column, row))
        square.mousePressEvent = lambda event: self.getBoardSquare(column, row)
        return square
    
    def updateSquareBackground(self, square, position, highlight=None):
        """highlight styles: selected, possible move, capture, check, and last move"""

        highlightStyles = {
            "selected": ("rgba(255, 255, 0, 0.5)", "yellow"),
            "possible move": ("rgba(0, 255, 0, 0.3)", "green"),
            "capture": ("rgba(255, 165, 0, 0.5)", "orange"),
            "check": ("rgba(255, 0, 0, 0.5)", "red"),
            "last move": ("rgba(102, 178, 255, 0.5)", "light blue")
        }

        if highlight in highlightStyles:
            bg_color, border_color = highlightStyles[highlight]
            style = f"""
            QLabel{{
                background-color: {bg_color};
                border: 2px solid {border_color};
            }}
            """
        else:
            bg_color = "#F0D9B5" if (position[0] + position[1]) % 2 == 0 else "#B58863"
            style = f"""
            QLabel{{
                background-color: {bg_color};
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            QLabel:hover {{
                border: 2px solid rgba(100, 100, 100, 0.5);
            }}
            """

        square.setStyleSheet(style)

    def getBoardSquare(self, column, row):
        """This function gets the square when the player selects the piece that's on a square"""
        pass

    def printBoard(self):
        print("\n    Board")
        print("===========")
        for row in range(8):
            rowState = []
            for column in range(8):
                position = (column, row)
                piece = self.board.get(position)
                rowState.append(" ")
                if piece:
                    if piece.color == "Black":
                        if isinstance(piece, Knight):
                            rowState.append(f"{piece.__class__.__name__.lower()[1]}{piece.color[0]}")
                        else:
                            rowState.append(f"{piece.__class__.__name__.lower()[0]}{piece.color[0]}")
                    else:
                        if isinstance(piece, Knight):
                            rowState.append(f"{piece.__class__.__name__.lower()[1]}{piece.color[0]}")
                        else:
                            rowState.append(f"{piece.__class__.__name__.lower()[0]}{piece.color[0]}")
                else:
                    rowState.append("--")
            print(" ".join(rowState))

    def getPieceAtPosition(self, position):
        return self.board.get(position)

    def setPieceAtPosition(self, position: tuple, piece: Optional[Piece]):
        if piece is None:
            self.board[position] = None
        else:
            self.board[position] = piece

    def clearHighlights(self):
        color = "White" if self.isWhiteTurn else "Black"
        isInCheck = self.isKingInCheck(color)
        kingPosition = self.whiteKingPosition if color == "White" else self.blackKingPosition

        for position, square in self.squares.items():
            self.updateSquareBackground(square, position)
        
        if isInCheck:
            self.updateSquareBackground(self.squares[kingPosition], kingPosition, "check")

    def isKingInCheck(self, color):
        self.attackingPaths.clear()
        self.attackingPieces.clear()

        kingPosition = self.whiteKingPosition if color == "White" else self.blackKingPosition
        
        self.checkRookAttacks(kingPosition, color)
        self.checkBishopAttacks(kingPosition, color)
        self.checkKnightAttacks(kingPosition, color)
        self.checkPawnAttacks(kingPosition, color)

        return len(self.attackingPieces) > 0

    def filterOutIllegalMoves(self, piece, position):
        self.movesList.clear()
        if not piece or (piece.color == "White") != self.isWhiteTurn:
            return []

        listOfPotentialMoves = piece.getPossibleMoves(self)
        validMoves = []

        for move in listOfPotentialMoves:
            if not self.isPositionWithinBoard(*move):
                continue

            targetPiece = self.board.get(move)
            if targetPiece and targetPiece.color == piece.color:
                continue

            # Make temporary move
            capturedPiece = self.getPieceAtPosition(move)
            originalPosition = piece.getPosition()

            # Temporarily update board
            self.setPieceAtPosition(position, None)
            self.setPieceAtPosition(move, piece)
            piece.col, piece.row = move

            # Update king position if king moved
            if isinstance(piece, King):
                if piece.color == "White":
                    self.whiteKingPosition = move
                else:
                    self.blackKingPosition = move

            # Check if the move leaves the king in check
            in_check = self.isKingInCheck(piece.color)

            # Revert the move
            self.setPieceAtPosition(position, piece)
            self.setPieceAtPosition(move, capturedPiece)
            piece.col, piece.row = originalPosition

            # Restore king position if king moved
            if isinstance(piece, King):
                if piece.color == "White":
                    self.whiteKingPosition = originalPosition
                else:
                    self.blackKingPosition = originalPosition

            if not in_check:
                validMoves.append(move)

        self.movesList = validMoves
        return validMoves

    def isPositionWithinBoard(self, column: int, row: int):
        return 0 <= column < 8 and 0 <= row < 8

    def movePieceTo(self, fromPosition, toPosition):
        piece = self.getPieceAtPosition(fromPosition)
        if not self.isMoveValid(piece, fromPosition, toPosition):
            return False
        if isinstance(piece, King):
            self.handleKingMoves(piece, fromPosition, toPosition)
        if isinstance(piece, Pawn):
            self.handlePawnMoves(piece, fromPosition, toPosition)
        if isinstance(piece, Rook):
            piece.hasRookMoved = True

        capturePiece = self.getPieceAtPosition(toPosition)
        self.setPieceAtPosition(fromPosition, None)
        self.setPieceAtPosition(toPosition, piece)
        piece.col, piece.row = toPosition[0], toPosition[1]

        self.lastMove = (fromPosition, toPosition, capturePiece is not None)
        FENFormat = self.FENConverter(self.lastMove[0], self.lastMove[1])
        self.gameHistory.append(FENFormat)
        return True

    def isMoveValid(self, piece, fromPosition, toPosition):
        """Check if a move is valid for the selected piece"""
        if not self.isPositionWithinBoard(toPosition[0], toPosition[1]):
            return False
        
        if not self.movesList:
            self.filterOutIllegalMoves(piece, fromPosition)

        return toPosition in self.movesList

    def handleKingMoves(self, piece, fromPosition, toPosition):
        if not isinstance(piece, King):
            return
        if abs(toPosition[0] - fromPosition[0]) == 2:
            canCastle = self.isCastlePossible(piece, fromPosition, toPosition)
            if canCastle:
                rookCol = 7 if toPosition[0] > fromPosition[0] else 0
                newRookCol = 5 if toPosition[0] > fromPosition[0] else 3
                rook = self.getPieceAtPosition((rookCol, fromPosition[1]))
                if rook:
                    self.setPieceAtPosition((rookCol, fromPosition[1]), None)
                    self.setPieceAtPosition((newRookCol, fromPosition[1]), rook)
                    rook.col = newRookCol
        piece.hasTheKingMoved = True
        if piece.color == "White":
            self.whiteKingPosition = toPosition
        else:
            self.blackKingPosition = toPosition

    def isCastlePossible(self, king: King, fromPosition: tuple, toPosition: tuple):
        if king.hasTheKingMoved:
            return False
        
        # Determine the rook's position based on castling direction
        rookCol = 7 if toPosition[0] > fromPosition[0] else 0
        rook = self.getPieceAtPosition((rookCol, fromPosition[1]))

        if rook is None or not isinstance(rook, Rook) or rook.hasRookMoved:
            return False
        
        # check if squares between king and rook are empty
        step = 1 if rookCol > fromPosition[0] else -1
        for col in range(fromPosition[0] + step, rookCol, step):
            if self.getPieceAtPosition((col, fromPosition[1])) is not None:
                return False
            
        # Ensure the king is not in check before, during, or after castling
        if self.isKingInCheck(king.color):
            return False
        
        kingRow = fromPosition[1]
        
        # Simulate the king's move to each square it crosses
        for col in range(fromPosition[0] + step, toPosition[0] + step, step):
            originalKingPosition = self.whiteKingPosition if king.color == "White" else self.blackKingPosition
            if king.color == "White":
                self.whiteKingPosition = (col, kingRow)
            else:
                self.blackKingPosition = (col, kingRow)
            
            isSquareUnderAttack = self.isKingInCheck(king.color)

            if king.color == "White":
                self.whiteKingPosition = originalKingPosition
            else:
                self.blackKingPosition = originalKingPosition

            if isSquareUnderAttack:
                return False
        
        return True

    def canMakeLegalMoves(self, enemy):
        """
        Determines if the current player has any legal moves available.

        This method iterates over all pieces of the current player and checks
        if there is at least one move that does not leave the player's king in check.
        It temporarily simulates each potential move to verify its legality.

        Returns:
            bool: True if at least one legal move exists, False otherwise.
        """

        # Check all pieces of the current player
        for col in range(8):
            for row in range(8):
                piece = self.board.get((col, row))
                if piece and piece.color == enemy:
                    # Get all potential moves for this piece
                    position = (col, row)
                    listOfPotentialMoves = piece.getPossibleMoves(self)

                    # Test each move
                    for move in listOfPotentialMoves:
                        if not self.isPositionWithinBoard(*move):
                            continue

                        # Save the current board
                        originalPosition = (piece.col, piece.row)
                        capturedPiece = self.getPieceAtPosition(move)
                        originalKingPosition = self.whiteKingPosition if enemy == "White" else self.blackKingPosition
                        
                        # temporarily make the move
                        self.setPieceAtPosition(position, None)
                        self.setPieceAtPosition(move, piece)
                        piece.col, piece.row = move

                        # Modify king position t
                        if isinstance(piece, King):
                            if piece.color == "White":
                                self.whiteKingPosition = move
                            else:
                                self.blackKingPosition = move

                        # Check if this move puts king in check
                        in_check = self.isKingInCheck(enemy)

                        # restore the board state
                        self.setPieceAtPosition(position, piece)
                        self.setPieceAtPosition(move, capturedPiece)
                        piece.col, piece.row = originalPosition

                        # Revert the king to its original position
                        if isinstance(piece, King):
                            if piece.color == "White":
                                self.whiteKingPosition = originalKingPosition
                            else:
                                self.blackKingPosition = originalKingPosition
                        
                        if not in_check:
                            return True
                        
        return False

    def handlePawnMoves(self, pawn, fromPosition, toPosition):
        """
        Handles the movement of a pawn, including en passant capture and double move flagging.

        Args:
            pawn (Pawn): The pawn piece being moved.
            fromPosition (tuple): The starting position of the pawn (column, row).
            toPosition (tuple): The square the pawn is moving to. (column, row).

        Returns:
            bool: True if an en passant capture occurred, False otherwise.

        The method checks for en passant conditions and updates the board state
        accordingly. It also flags the pawn if it makes a double move.
        """
        for pos, piece in self.board.items():
            if isinstance(piece, Pawn) and piece.color == pawn.color:
                piece.hasDoubleMoved = False
                piece.enpassantVulnerable = False

        if abs(toPosition[0] - fromPosition[0]) == 1 and abs(toPosition[1] - fromPosition[1]) == 1:
            targetPiece = self.board.get(toPosition)
            if targetPiece is None:
            
                # Verify the conditions for en passant:
                captured_position = (toPosition[0], fromPosition[1])
                capturedPiece = self.board.get(captured_position)

                if isinstance(capturedPiece, Pawn) and capturedPiece.enpassantVulnerable and capturedPiece.getColor() != pawn.color:
                    self.setPieceAtPosition(captured_position, None)
                    return True
            
        # Handle double move    
        if abs(toPosition[1] - fromPosition[1]) == 2:
            pawn.hasDoubleMoved = True
            pawn.enpassantVulnerable = True
        
        return False    

    def FENConverter(self, fromPosition: tuple, toPosition: tuple):
        if 0 <= fromPosition[0] <= 7 and 0 <= fromPosition[1] <= 7:
            from_rank = chr(97 + fromPosition[0])  # a-h
            from_file = str(8 - fromPosition[1])   # 1-8
        
        if 0 <= toPosition[0] <= 7 and 0 <= toPosition[1] <= 7:
            to_rank = chr(97 + toPosition[0])
            to_file = str(8 - toPosition[1])
        fen_format = from_rank + from_file + to_rank + to_file
        return fen_format

    def checkRookAttacks(self, kingPosition, color):
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            col, row = kingPosition[0] + dx, kingPosition[1] + dy
            current_path = []

            while self.isPositionWithinBoard(col, row):
                current_path.append((col, row))
                piece = self.getPieceAtPosition((col, row))

                if piece:
                    if piece.color != color and isinstance(piece, (Rook, Queen)):
                        self.attackingPieces.add(piece)
                        self.attackingPaths.append(current_path)
                    break

                col += dx
                row += dy

    def checkBishopAttacks(self, kingPosition, color):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            col, row = kingPosition[0] + dx, kingPosition[1] + dy
            current_path = []

            while self.isPositionWithinBoard(col, row):
                current_path.append((col, row))
                piece = self.getPieceAtPosition((col, row))

                if piece:
                    if piece.color != color and isinstance(piece, (Bishop, Queen)):
                        self.attackingPieces.add(piece)
                        self.attackingPaths.append(current_path)
                    break

                col += dx
                row += dy

    def checkKnightAttacks(self, kingPosition, color):
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)] 
                        
        for move in knight_moves:
            col = kingPosition[0] + move[0]
            row = kingPosition[1] + move[1]
            if self.isPositionWithinBoard(col, row):
                piece = self.getPieceAtPosition((col, row))
                if piece and piece.color != color and isinstance(piece, Knight):
                    self.attackingPaths.append([(col, row)])
                    self.attackingPieces.add(piece)

    def checkPawnAttacks(self, kingPosition, color):
        pawn_moves = [(-1, -1), (1, -1)] if color == "White" else [(-1, 1), (1, 1)]
        for move in pawn_moves:
            col = kingPosition[0] + move[0]
            row = kingPosition[1] + move[1]
            if self.isPositionWithinBoard(col, row):
                piece = self.getPieceAtPosition((col, row))
                if piece and piece.color != color and isinstance(piece, Pawn):
                    self.attackingPaths.append([(col, row)])
                    self.attackingPieces.add(piece)

    def getBoardInFENPosition(self):
        pass






