import chess
import chess.pgn
from stockfish import Stockfish
from mascot.mascot import get_comment

stockfish = Stockfish(path="/usr/games/stockfish") 

def analyze_game(pgn_path):
    with open(pgn_path) as f:
        game = chess.pgn.read_game(f)

    board = game.board()
    analysis = []

    for move in game.mainline_moves():
        board.push(move)
        stockfish.set_fen_position(board.fen())
        eval_data = stockfish.get_evaluation()
        analysis.append({
            "move": board.san(move),
            "eval": eval_data,
            "comment": get_comment(eval_data)
        })

    return analysis
