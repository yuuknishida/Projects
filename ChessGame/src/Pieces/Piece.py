from abc import abstractmethod
from typing import List

class Piece:
    def __init__(self, col: int, row: int, color: str):
        self.col = col
        self.row = row
        self.color = color

    def getColor(self) -> str:
        return self.color
    
    def getPosition(self) -> tuple:
        return (self.col, self.row)
    
    def setPosition(self, col, row):
        self.col = col
        self.row = row
    
    def getImageName(self) -> str:
        """Returns the image file name for the piece"""
        color_map = {"White": "W", "Black": "B"}
        color = color_map.get(self.color, "U")
        class_name = self.__class__.__name__
        return f"{class_name}{color}.png"
    
    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"

    @abstractmethod
    def getPossibleMoves(self, board) -> List[tuple]:
        return [] 