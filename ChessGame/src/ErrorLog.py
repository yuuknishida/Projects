from typing import Any, Dict, Optional
import pandas as pd # type: ignore
import datetime
import os

class ErrorLog:
    log_file_path = "error_logs.xlsx"
    def __init__(self):
        self._initalize_log_file()
        

    def _initalize_log_file(self):
        if not os.path.exists(self.log_file_path):
            df = pd.DataFrame(columns=[
                'timestamp',
                'error_type',
                'error_message',
                'source_file',
                'function_name',
                'Selected Piece',
                'Selected Square',
                'Move To',
                'Number of Turns',
                'Player Turn'
            ])
            df.to_excel(self.log_file_path, index=False)

    def log_error_to_excel(self, 
                           error_type: str,
                           error_message: str,
                           source_file: str,
                           function_name: str,
                           selectedPiece,
                           selectedSquare,
                           moveTo,
                           numofTurns,
                           playerTurn):
        """
            error_type(str) : Type of error ("InvalidMove, Engine Error)
            error_message(str): The error message
            source_file(str): The file where the error occurred 
            function_name(str): The function where the error occurred 
            additional_info(str): The Additional information about the error context
        """
        try:
            if os.path.exists(self.log_file_path):
                df = pd.read_excel(self.log_file_path)
            else:
                df = pd.DataFrame(column=[
                    'timestamp',
                    'error_type',
                    'error_message',
                    'source_file',
                    'function_name',
                    'Selected Piece',
                    'Selected Square',
                    'Move To',
                    'Number of Turns',
                    'Player Turn'
                ])
            new_entry = {
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'error_type': error_type,
                'error_message': error_message,
                'source_file': source_file,
                'function_name': function_name,
                'Selected Piece': selectedPiece,
                'Selected Square': selectedSquare,
                'Move To': moveTo,
                'Number of Turns': numofTurns,
                'Player Turn': playerTurn
            }
            

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_excel(self.log_file_path, index=False)

        except Exception as e:
            print(f"Error while logging to Excel: {e}")
            print(f"original error: {error_type} - in {error_message} in {source_file}::{function_name}")
