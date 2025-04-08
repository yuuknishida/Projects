from typing import Tuple
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QSpacerItem, QSizePolicy, QFrame, QScrollArea, QLabel, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor

import sys

from chessBoardManager import ChessBoardManager
from chessEngine import StockfishEngine

class EvaluationBar(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.frame = QFrame()
        self.score = 0
        self.bar = QProgressBar()
        self.frame.setFrameStyle(QFrame.Shape.Box)
        self.setMinimumWidth(30)
        self.setContentsMargins(0,0,0,0)

    def setScore(self, score):
        self.score = max(min(score / 1000, 1), -1) / 2 + 0.5
        self.update()

    def paintEvent(self, event):
        """Handle score display painting"""
        painter = QPainter(self)
        height = self.height()
        width = self.width()
        
        # Draw background
        painter.fillRect(0, 0, width, height, QColor(200, 200, 200))
        
        # Draw evaluation bar
        bar_height = int(self.score * height)
        painter.fillRect(0, height - bar_height, width, bar_height, QColor(0, 0, 0))

class GameHistory(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setMinimumWidth(300)
        self.setFrameStyle(QFrame.Shape.Box)

        self.moves = []

        layout = QVBoxLayout(self)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scrollArea.setWidget(self.scrollWidget)
        layout.addWidget(self.scrollArea)
    
    def addMove(self, move):
        if not self.moves or self.moves[-1][2]:
            self.moves.append([len(self.moves) + 1, move, ""])
        else:
            self.moves[-1][2] = move
        self.updateHistory()

    def updateHistory(self):
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()

        moveTexts = []
        for roundTurn, whiteTurn, blackTurn in self.moves:
            turnNum = f"{roundTurn}.".ljust(8)
            white = whiteTurn.ljust(10)
            move = turnNum + white + blackTurn
            moveTexts.append(move)
        

        moveHistoryLabel = QLabel("\n".join(moveTexts))
        moveHistoryLabel.setStyleSheet("font-family: monospace; font-size: 12pt;")

        self.scrollLayout.addWidget(moveHistoryLabel)

class Window(QMainWindow):
    def __init__(self, chessEngine, chessBoard, parent=None):
        super().__init__(parent)
        self.chessEngine = chessEngine
        self.chessBoardManager = chessBoard
        self.evaluationBar = EvaluationBar()
        self.gameHistoryList = GameHistory()
        self.gameState = "PLAYING" # PLAYING, STALEMATE, CHECKMATE


        self.initUI()
        self.show()
    
    def initUI(self):
        self.setWindowTitle("Chess Game")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)

        # Game layout
        gameLayout = QHBoxLayout()

        centerLayout = QHBoxLayout()
        centerLayout.setContentsMargins(0,0,0,0)
        centerLayout.addWidget(self.evaluationBar)  # Evaluation Bar
        spacer = QSpacerItem(50, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        centerLayout.addSpacerItem(spacer)
        centerLayout.addWidget(self.chessBoardManager)  # Chess Board
        centerLayout.addSpacerItem(spacer)
        centerLayout.addWidget(self.gameHistoryList)

        centerWidget = QWidget()
        centerWidget.setLayout(centerLayout)
        gameLayout.addWidget(centerWidget, alignment=Qt.AlignmentFlag.AlignCenter)

        gameWidget = QWidget()
        gameWidget.setLayout(gameLayout)
        mainLayout.addWidget(gameWidget)
    
    def showGameEndDialog(self, message: str):
        QMessageBox.information(self, "Game Over", message)