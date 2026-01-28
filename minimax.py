import copy
from typing import List, Optional, Tuple

winningIndexes = [
    # horizontals
    [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
    # verticals
    [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
    # diagonals
    [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
]

def current_player(board: List[List[str]]):
    xCount = sum(1 for row in board for move in row if move == "X")
    oCount = sum(1 for row in board for move in row if move == "O")
    return "X" if xCount <= oCount else "O"

def get_winner(board: List[List[str]]) -> Optional[str]:
    """Returns the winner ('X' or 'O') or None if no winner"""
    for indexes in winningIndexes:
        p1, p2, p3 = indexes
        if (board[p1[0]][p1[1]] != '' and
            board[p1[0]][p1[1]] == board[p2[0]][p2[1]] == board[p3[0]][p3[1]]):
            return board[p1[0]][p1[1]]
    return None

def is_board_full(board: List[List[str]]) -> bool:
    return all(cell != "" for row in board for cell in row)

def minimax(board: List[List[str]], maximizing_player: str, stats: dict) -> Tuple[int, Optional[List[List[str]]]]:
    """
    Returns (score, best_move) where best_move is only set at the top level
    """

    stats['iterations'] += 1

    winner = get_winner(board)
    if winner:
        return (10 if winner == maximizing_player else -10, None)

    if is_board_full(board):
        return (0, None)

    player = current_player(board)
    is_maximizing = (player == maximizing_player)

    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = player

                score, _ = minimax(board, maximizing_player, stats)

                board[row][col] = ""

                if is_maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = copy.deepcopy(board)
                        best_move[row][col] = player
                else:
                    if score < best_score:
                        best_score = score
                        best_move = copy.deepcopy(board)
                        best_move[row][col] = player

    return (best_score, best_move)