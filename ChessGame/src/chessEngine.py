from stockfish import Stockfish
from typing import List

class StockfishEngine:
    def __init__(self, path = "C:\\Senior Design Project\\stockfish\\stockfish-windows-x86-64-avx2.exe"):
        self.engine = Stockfish(path=path)
        self.currentFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.difficulty = self.setDifficulty("Medium")
        self.movesList = []
        self.initEngine()

    def initEngine(self):
        self.engine.update_engine_parameters(
            {
            "Threads": 1,
            "Hash": 2048,
            "UCI_Chess960": "false",
            "Minimum Thinking Time": 20
            })
        self.engine.set_fen_position(self.currentFEN)
    
    def sendBoardToEngine(self, board, fromPosition, toPosition):
        fenFormat = self.FENConverter(fromPosition, toPosition)

        try:
            if not self.engine.is_move_correct(fenFormat):
                raise Exception(f"Invalid move received: {fenFormat}")

            previousFEN = self.currentFEN
            previousMoves = self.movesList.copy()

            self.movesList.append(fenFormat)

            self.engine.set_fen_position(previousFEN)
            self.engine.make_moves_from_current_position([fenFormat])

            newFEN = self.engine.get_fen_position()
            if newFEN == previousFEN:
                raise Exception("Move did not change board state")
            
            self.currentFEN = newFEN
            return True
        
        except Exception as e:
            self.movesList = previousMoves
            if 'previousFEN' in locals():
                self.engine.set_fen_position(previousFEN)
                self.currentFEN = previousFEN
            raise Exception(f"{e}")
        
    def generateMove(self):
        try:
            if " w " in self.currentFEN:
                self.currentFEN = self.currentFEN.replace(" w ", " b ")
            
            # generate the best move possible for black
            bestMove = self.engine.get_best_move(wtime=None, btime=2000)

            # check if move is correct
            if not bestMove or not self.engine.is_move_correct(bestMove):
                raise Exception("No valid move found")
            
            previousFEN = self.currentFEN
            
            self.movesList.append(bestMove)

            self.engine.set_fen_position(previousFEN)
            self.engine.make_moves_from_current_position([bestMove])
            
            self.currentFEN = self.engine.get_fen_position()
            
            return bestMove

        except Exception as e:
            raise Exception(f"Error generating move: {e} in file C:\\Senior Design Project\\src\\chessEngine.py")
            

    def setDifficulty(self, difficulty: str):
        if difficulty == "EASY":
            self. engine.update_engine_parameters({
                "UCI_Elo": 800
            })
            self.difficulty = difficulty

        elif difficulty == "MEDIUM":
            self.engine.update_engine_parameters({
                "UCI_Elo": 1500
            })
            self.difficulty = difficulty
        else:
            self.engine.update_engine_parameters({
                "UCI_Elo": 2500
            })
            self.difficulty = difficulty

    def FENConverter(self, fromPosition: tuple, toPosition: tuple=None):
        if 0 <= fromPosition[0] <= 7 and 0 <= fromPosition[1] <= 7:
            from_rank = chr(97 + fromPosition[0])  # a-h
            from_file = str(8 - fromPosition[1])   # 1-8
        
        if toPosition is not None and 0 <= toPosition[0] <= 7 and 0 <= toPosition[1] <= 7:
            to_rank = chr(97 + toPosition[0])
            to_file = str(8 - toPosition[1])

        fen_format = from_rank + from_file + to_rank + to_file
        return fen_format
    
    def convertToNumeric(self, position: str):
        fromFile, fromRank, toFile, toRank = position[:4]
        fileToCol = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        
        fromCol = fileToCol[fromFile]
        fromRow = 8 - int(fromRank)
        toCol = fileToCol[toFile]
        toRow = 8 - int(toRank)

        fromPosition = (fromCol, fromRow)
        toPosition = (toCol, toRow)

        return fromPosition, toPosition