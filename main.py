from typing import List

from fastapi import Body, FastAPI

# Import from your minimax module
from minimax import current_player, get_winner, is_board_full, minimax

app = FastAPI()

@app.post("/move")
def get_optimal_move(board: List[List[str]] = Body(..., example=[["X", "O", "X"],["O", "X", "O"],["", "", ""]])):
    """
    Takes a tic-tac-toe board and returns the optimal next move using minimax algorithm.
    """
    # Check if game is already over
    winner = get_winner(board)
    if winner:
        return {
            "error": f"Game is already over. Winner: {winner}",
            "board": board
        }

    if is_board_full(board):
        return {
            "error": "Game is already over. It's a draw.",
            "board": board
        }

    # Get current player
    player = current_player(board)

    # Run minimax
    stats = {'iterations': 0}
    score, best_move = minimax(board, player, stats)

    return {
        "player": player,
        "optimal_move": best_move,
        "score": score,
        "iterations": stats['iterations']
    }

if __name__ == "__main__":
    import os

    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)