import trace
from typing import Any, Dict, Tuple
import traceback
from PyQt5.QtWidgets import QApplication # type: ignore
from PyQt5.QtCore import QTimer # type: ignore
import sys
from window import Window
from chessEngine import StockfishEngine
from chessBoardManager import ChessBoardManager
from ErrorLog import ErrorLog

class App:
    def __init__(self):
        self.errorLog = ErrorLog()
        self.chessEngine = StockfishEngine()
        self.chessBoardManager = ChessBoardManager() 
        self.window = Window(self.chessEngine, self.chessBoardManager)
        self.gameState = "PLAYING"
        self.selectedPiece = None
        self.selectedSquare = None
        self.enableAi = False
        self._info = {}

        self.aiTimer = QTimer()
        self.aiTimer.setSingleShot(True)
        self.aiTimer.timeout.connect(self.aiTurn)

        self.setupGame()
    
    def setupGame(self):
        self.chessBoardManager.initBoard()
        self.chessBoardManager.initPieces()
        self.chessBoardManager.getBoardSquare = self.handleSquareClick

    def handleSquareClick(self, column: int, row: int):
        """This method is meant to test the chess code via clicking on a square on the board. """
        if self.gameState != "PLAYING":
            return False
        
        position = (column, row)
        piece = self.chessBoardManager.getPieceAtPosition(position)
        self._info.clear()

        if self.selectedSquare:
            if position == self.selectedSquare:
                self.chessBoardManager.clearHighlights()
                self.selectedPiece = None
                self.selectedSquare = None
                self._info.clear()
            else:
                validMoves = self.chessBoardManager.filterOutIllegalMoves(self.selectedPiece, self.selectedSquare)
                if position in validMoves:
                    self.tryMove(self.selectedSquare, position)
                    self.processTurn()
                    self.chessBoardManager.numOfTurns += 1                    
        else:
            piece = self.chessBoardManager.getPieceAtPosition(position)
            if piece and piece.color == ("White" if self.chessBoardManager.isWhiteTurn else "Black"):
                self.pieceSelection(piece, position)

    def tryMove(self, fromPosition, toPosition):
        self.chessBoardManager.movePieceTo(fromPosition, toPosition)

        fenNotation = self.chessBoardManager.FENConverter(self.chessBoardManager.lastMove[0], self.chessBoardManager.lastMove[1])
        self.window.gameHistoryList.addMove(fenNotation)

        return True
        
    def processTurn(self):
        self.clearSelection()

        checkEnemy = "Black" if self.chessBoardManager.isWhiteTurn else "White"
        isInCheck = self.chessBoardManager.isKingInCheck(checkEnemy)
        hasLegalMoves = self.chessBoardManager.canMakeLegalMoves(checkEnemy)

        if isInCheck and not hasLegalMoves:
            self.gameState = "CHECKMATE"
            winner = "Black" if self.chessBoardManager.isWhiteTurn else "White"
            # self.showGameEndDialog(f"Checkmate! {winner} wins!")
        elif not hasLegalMoves:
            self.gameState = "STALEMATE"
            # self.showGameEndDialog(f"Stalemate!")

        try:
            evaluation = self.chessEngine.engine.get_evaluation()
            if evaluation.get('type') == 'cp':
                score = evaluation.get('value')
                self.window.evaluationBar.setScore(score)
        except Exception as e:
            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            function_name = tb.name
            file_name = tb.filename

            self._info['Number of Turns'] = self.chessBoardManager.numOfTurns
            self._info['Player Turn'] = "White" if self.chessBoardManager.isWhiteTurn else "Black"
            
            print(f"Error updating evaluation: {e} in C:\\Senior Project Electronic Chessboard\\src\\App.py")
            self.errorLog.log_error_to_excel("GUI Error", f"Evaluation Score bar updated incorrectly {e}", file_name, function_name, f"{evaluation}", self.chessBoardManager.selectedPiece, self.chessBoardManager.selectedSquare, moveTo="", numofTurns=self.chessBoardManager.numOfTurns, playerTurn="White" if self.chessBoardManager.isWhiteTurn else "Black")
            self.debugLog("GUI had an error evaluation bar gave an error")

        self.chessBoardManager.update()
        self.chessBoardManager.isWhiteTurn = not self.chessBoardManager.isWhiteTurn

        self.chessBoardManager.clearHighlights()

        if self.enableAi and self.chessBoardManager.isWhiteTurn == False:
            try:
                fromPosition, toPosition = self.chessEngine.convertToNumeric(self.chessBoardManager.gameHistory[-1])
                self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[fromPosition], fromPosition, "last move")
                self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[toPosition], toPosition, "last move")
                self.chessEngine.sendBoardToEngine(self.chessBoardManager, fromPosition, toPosition)
                self.aiTimer.start(1000)
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])[-1]
                function_name = tb.name
                file_name = tb.filename
                self._info['Number of Turns'] = self.chessBoardManager.numOfTurns
                self._info['Player Turn'] = "White" if self.chessBoardManager.isWhiteTurn else "Black"
                print(f"Error setting up AI turn: {e} in file C:\\Senior Project Electronic Chessboard\\src\\App.py")
                self.errorLog.log_error_to_excel("Engine Error", f"Error occurred in {tb} - {e}", file_name, function_name, self.chessBoardManager.selectedPiece, self.chessBoardManager.selectedSquare, moveTo="", numofTurns=self.chessBoardManager.numOfTurns, playerTurn="White" if self.chessBoardManager.isWhiteTurn else "Black")
                self.debugLog()
        else:
            try:
                fromPosition, toPosition = self.chessEngine.convertToNumeric(self.chessBoardManager.gameHistory[-1])
                self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[fromPosition], fromPosition, "last move")
                self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[toPosition], toPosition, "last move")
                self.chessEngine.sendBoardToEngine(self.chessBoardManager, fromPosition, toPosition)
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])[-1]
                function_name = tb.name
                file_name = tb.filename
                self._info['Number of Turns'] = self.chessBoardManager.numOfTurns
                self._info['Player Turn'] = "White" if self.chessBoardManager.isWhiteTurn else "Black"
                self.errorLog.log_error_to_excel("Engine Error", f"Error occurred in {tb} - {e}", file_name, function_name, self.chessBoardManager.selectedPiece, self.chessBoardManager.selectedSquare, moveTo="", numofTurns=self.chessBoardManager.numOfTurns, playerTurn="White" if self.chessBoardManager.isWhiteTurn else "Black")

                print(f"Error highlighting last move: {e}")
                self.debugLog()

    def aiTurn(self):
        try:
            aiMove = self.chessEngine.generateMove()
            self._info['Generated Move'] = aiMove
            if aiMove is None:
                return
            aiFrom, aiTo = self.chessEngine.convertToNumeric(aiMove)
            piece = self.chessBoardManager.getPieceAtPosition(aiFrom)

            self.pieceSelection(piece, aiFrom)
            
            # Checks if the piece is properly selected
            if not self.chessBoardManager.selectedPiece:
                raise Exception(f"There's no piece at {aiFrom}")
            
            # Checks if the piece is black
            if self.chessBoardManager.selectedPiece.color != "Black":
                raise Exception(f"The selected piece is not black its a {self.chessBoardManager.board.get(aiFrom)}")
            
            # Get the moves for the piece
            listofMoves = self.chessBoardManager.filterOutIllegalMoves(self.chessBoardManager.selectedPiece, aiFrom)

            if aiTo not in listofMoves:
                raise Exception(f"Cannot move to target square {aiTo}. Not in list of moves")
            
            if self.chessBoardManager.movePieceTo(aiFrom, aiTo):
                self.chessBoardManager.update()
                self.processTurn()

                fenNotation = self.chessBoardManager.FENConverter(aiFrom, aiTo)
                self.window.gameHistoryList.addMove(fenNotation)
            else:
                raise Exception("Failed to make AI move")
            
            # Clear highlights and highlight last move squares
            self.chessBoardManager.clearHighlights()
            fromPosition, toPosition = self.chessEngine.convertToNumeric(self.chessBoardManager.gameHistory[-1])
            self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[fromPosition], fromPosition, "last move")
            self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[toPosition], toPosition, "last move")
        except Exception as e:
            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            function_name = tb.name
            file_name = tb.filename
            self._info['Number of Turns'] = self.chessBoardManager.numOfTurns
            self._info['Player Turn'] = "White" if self.chessBoardManager.isWhiteTurn else "Black"
            self._info['Selected Piece'] = self.chessBoardManager.selectedPiece
            self._info['Selected Square'] = self.chessBoardManager.selectedSquare
            self.errorLog.log_error_to_excel("Engine Error", f"Error occurred in {tb} - {e}", file_name, function_name, self.chessBoardManager.selectedPiece, self.chessBoardManager.selectedSquare, moveTo=None, numofTurns=self.chessBoardManager.numOfTurns, playerTurn="Wite" if self.chessBoardManager.isWhiteTurn else "Black")
            self.debugLog(message=str(e))

    def pieceSelection(self, piece, position: Tuple[int, int]):
        # Set selected piece and square
        self.chessBoardManager.selectedPiece = piece
        self.chessBoardManager.selectedSquare = position
        self.selectedPiece = piece
        self.selectedSquare = position

        self.chessBoardManager.clearHighlights()
        self.chessBoardManager.updateSquareBackground(
            self.chessBoardManager.squares[position],
            position,
            "selected"
        )

        # Load info for error log
        self._info['Selected Piece'] = self.selectedPiece
        self._info['Selected Square'] = self.selectedSquare

        # Show the moves available for the piece
        validMoves = self.chessBoardManager.filterOutIllegalMoves(self.chessBoardManager.selectedPiece, self.chessBoardManager.selectedSquare)
        
        for move in validMoves:
            highlightType = "capture" if self.chessBoardManager.getPieceAtPosition(move) else "possible move"
            self.chessBoardManager.updateSquareBackground(self.chessBoardManager.squares[move], move, highlightType)

    def clearSelection(self):
        self.chessBoardManager.clearHighlights()
        self.chessBoardManager.selectedPiece = None
        self.chessBoardManager.selectedSquare = None
        self.selectedSquare = None
        self.selectedPiece = None

    def debugLog(self, message = None):
        print("\t Debug Log")
        print("="*40)
        print(f"Error Message: {message}")
        print(f"Selected Piece: {self.chessBoardManager.selectedPiece}")
        print(f"Selected Square: {self.chessBoardManager.selectedSquare}")
        print(f"Moves List: {self.chessBoardManager.gameHistory}")
        print("\n Tracking Board...")
        print("="*40)
        self.chessBoardManager.printBoard()
        print("\n Tracking Engine's Board...")
        print("="*40)
        print(self.chessEngine.engine.get_board_visual())
        print(f"Current FEN: {self.chessEngine.currentFEN}")
        print(f"Current Score: {self.window.evaluationBar.score}")



if __name__ == "__main__":
    ChessApp = QApplication(sys.argv)
    app = App()
    sys.exit(ChessApp.exec_())
