import tkinter as tk
from tkinter import font, messagebox

# Players
HUMAN = "O"
COMPUTER = "X"
current_turn = COMPUTER

# Scoring system for minimax
points = {
    "X": 1,
    "O": -1,
    "Tie": 0    
}

# Game Board and control variables
board_state = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
end_game = False
button_grid = [[None for j in range(3)] for i in range(3)]

# Set up the GUI
def initialize_game():
    window = tk.Tk()
    window.title("Tic Tac Toe")

    for row in range(3):
        for col in range(3):
            btn = tk.Button(window, text="",
                            font=font.Font(size=36, weight="bold"),
                            width=5, height=2,
                            command=lambda r=row, c=col: player_turn(r, c))
            btn.grid(row=row, column=col)
            button_grid[row][col] = btn

    if current_turn == COMPUTER:
        computer_turn()

    window.mainloop()

# Player's turn
def player_turn(row, col):
    global current_turn
    if board_state[row][col] == '' and not end_game and current_turn == HUMAN:
            board_state[row][col] = HUMAN
            button_grid[row][col].config(text=HUMAN)
            result = check_winner()
            if result:
                display_result(result)
            else:
                current_turn = COMPUTER
                computer_turn()

# Computer's turn
def computer_turn():
    global current_turn
    best_Score = float('-inf')
    best_move = None

    # Finding the best move for the computer
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == '':
                board_state[i][j] = COMPUTER
                score = minimax(board_state, 0, False)
                board_state[i][j] = ''
                if score > best_Score:
                    best_Score = score
                    best_move = (i,j)
    if best_move:
        board_state[best_move[0]][best_move[1]] = COMPUTER
        button_grid[best_move[0]][best_move[1]].config(text=COMPUTER)
        result = check_winner()
        if result:
            display_result(result)
        else:
            current_turn = HUMAN

# Check for a winner
def display_result(winner):
    global end_game
    message = "Tie!" if winner == "Tie" else f"Winner is {winner}"
    messagebox.showinfo("Game Over", message)
    end_game = True
    restart_game()

# Restart the game
def restart_game():
    global board_state
    global end_game
    global current_turn
    board_state = [["", "", ""], ["", "", ""], ["", "", ""]]
    for i in range(3):
        for j in range(3):
            button_grid[i][j].config(text='')
    current_turn = COMPUTER
    end_game = False
    if current_turn == COMPUTER:
        computer_turn()

# Minimax algorithm
def minimax(state, depth, is_maximizing):
    """
    Minimax algorithm
    Parameters:
    board(list): the current state of the board as a list of 9 elements (0 for empty, 1 for X, -1 for O)
    depth(int): the current depth of the recursion
    maximizing_player(bool): True if it's the maximizing player's turn, False for the minimizing player's turn
    is_game_over(bool): True if the game is over, False otherwise
    
    Returns:
    int: the score of the best move (-1, 0, or 1)
    """
    result = check_winner()
    if result is not None:
        return points[result]

    if is_maximizing: 
        max_Score = float('-inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':  
                    state[i][j] = COMPUTER  
                    score = minimax(state, depth + 1, False)  
                    state[i][j] = ''  
                    max_Score = max(score, max_Score)
        return max_Score
    else:
        min_Score = float('inf')
        for i in range(3):
            for j in range(3):
                if state[i][j] == '':  
                    state[i][j] = HUMAN  
                    score = minimax(state, depth + 1, True)  
                    state[i][j] = ''  
                    min_Score = min(score, min_Score)
        return min_Score

# Check for a winner
def check_winner():
    """
    Returns:
    int: the winner of the game (0 for no winner, 1 for X, -1 for O, or 'Tie' if the game is a tie)
    """
    # Check rows and columns
    for i in range(3):
        if board_state[0][i] == board_state[1][i] == board_state[2][i] != '':
            return board_state[0][i]
        if board_state[i][0] == board_state[i][1] == board_state[i][2] != '':
            return board_state[i][0]
    
    # Check diagonal
    if board_state[0][0] == board_state[1][1] == board_state[2][2] != '':
        return board_state[0][0]
    if board_state[2][0] == board_state[1][1] == board_state[0][2] != '':
        return board_state[2][0]
    
    if all(cell != '' for row in board_state for cell in row):
        return 'Tie'
    return None

def main():
    initialize_game()

if __name__ == "__main__":
    main()