import os
from typing import List

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from minimax import current_player, get_winner, is_board_full, minimax

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        # "https://your-react-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Tic-Tac-Toe API", "status": "running"}

@app.post("/move")
def get_optimal_move(board: List[List[str]] = Body(...)):
    winner = get_winner(board)
    if winner:
        return {"error": f"Game over. Winner: {winner}", "board": board}

    if is_board_full(board):
        return {"error": "Game over. Draw.", "board": board}

    player = current_player(board)
    stats = {'iterations': 0}
    score, best_move = minimax(board, player, stats)

    return {
        "player": player,
        "optimal_move": best_move,
        "score": score,
        "iterations": stats['iterations']
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)