import logging
import os
from datetime import datetime
from typing import List

from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from minimax import (current_player, get_winner, is_board_full, minimax,
                     minimax_alpha_beta)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://tic-tac-toe-minimax-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def format_board(board: List[List[str]]) -> str:
    """Format board for logging"""
    lines = []
    for row in board:
        line = " | ".join([cell if cell else " " for cell in row])
        lines.append(line)
    return "\n" + "\n---------\n".join(lines)

def get_move_position(old_board: List[List[str]], new_board: List[List[str]]) -> str:
    """Find what move was made"""
    for i in range(3):
        for j in range(3):
            if old_board[i][j] != new_board[i][j]:
                return f"({i},{j})"
    return "unknown"

@app.get("/")
def read_root():
    logger.info("Health check endpoint hit")
    return {"message": "Tic-Tac-Toe API", "status": "running"}

@app.post("/move")
def get_optimal_move(request: Request, board: List[List[str]] = Body(...)):
    # Log incoming request
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"=== New Game Request (Standard Minimax) ===")
    logger.info(f"Client IP: {client_ip}")
    logger.info(f"Current board state:{format_board(board)}")

    winner = get_winner(board)
    if winner:
        logger.info(f"Game already over. Winner: {winner}")
        return {"error": f"Game over. Winner: {winner}", "board": board}

    if is_board_full(board):
        logger.info("Game already over. Board is full (draw)")
        return {"error": "Game over. Draw.", "board": board}

    player = current_player(board)
    logger.info(f"Current player: {player}")

    # Run minimax
    stats = {'iterations': 0}
    score, best_move = minimax(board, player, 0, stats)

    # Log the result
    move_position = get_move_position(board, best_move) if best_move else "none"
    logger.info(f"AI ({player}) chose position {move_position}")
    logger.info(f"Resulting board:{format_board(best_move) if best_move else ' (no move)'}")
    logger.info(f"Minimax score: {score}")
    logger.info(f"Iterations computed: {stats['iterations']}")
    logger.info(f"=== Request Complete ===\n")

    return {
        "player": player,
        "optimal_move": best_move,
        "score": score,
        "iterations": stats['iterations']
    }

@app.post("/move_alpha_beta")
def get_optimal_move_alpha_beta(request: Request, board: List[List[str]] = Body(...)):
    # Log incoming request
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"=== New Game Request (Alpha-Beta Pruning) ===")
    logger.info(f"Client IP: {client_ip}")
    logger.info(f"Current board state:{format_board(board)}")

    winner = get_winner(board)
    if winner:
        logger.info(f"Game already over. Winner: {winner}")
        return {"error": f"Game over. Winner: {winner}", "board": board}

    if is_board_full(board):
        logger.info("Game already over. Board is full (draw)")
        return {"error": "Game over. Draw.", "board": board}

    player = current_player(board)
    logger.info(f"Current player: {player}")

    # Run minimax with alpha-beta pruning
    stats = {'iterations': 0}
    score, best_move = minimax_alpha_beta(board, player, 0, stats)

    # Log the result
    move_position = get_move_position(board, best_move) if best_move else "none"
    logger.info(f"AI ({player}) chose position {move_position}")
    logger.info(f"Resulting board:{format_board(best_move) if best_move else ' (no move)'}")
    logger.info(f"Minimax score: {score}")
    logger.info(f"Iterations computed: {stats['iterations']}")
    logger.info(f"=== Request Complete ===\n")

    return {
        "player": player,
        "optimal_move": best_move,
        "score": score,
        "iterations": stats['iterations']
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
