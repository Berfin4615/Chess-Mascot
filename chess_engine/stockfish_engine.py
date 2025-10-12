import chess
import chess.pgn
from stockfish import Stockfish
from mascot.mascot import get_comment

engine = Stockfish(path="/usr/games/stockfish") 

def analyze_game_detailed(pgn_path: str):
    with open(pgn_path) as f:
        game = chess.pgn.read_game(f)

    board = game.board()
    timeline = []  # [{san, fen_after, eval:{type,value}, comment}, ...]

    for move in game.mainline_moves():
        san = board.san(move)        # önce SAN
        board.push(move)             # sonra uygula
        engine.set_fen_position(board.fen())
        ev = engine.get_evaluation()
        timeline.append({
            "san": san,
            "fen_after": board.fen(),
            "eval": ev,
            "comment": get_comment(ev)
        })
    return {
        "initial_fen": chess.STARTING_FEN,
        "moves": timeline
    }