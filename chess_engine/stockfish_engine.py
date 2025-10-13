import chess
import chess.pgn
from stockfish import Stockfish
from mascot.mascot import get_comment
import shutil, re, io

# Stockfish yolu
stockfish_path = shutil.which("stockfish")
if not stockfish_path:
    raise FileNotFoundError("⚠️ Stockfish bulunamadı (sudo apt install stockfish).")
stockfish = Stockfish(path=stockfish_path)

def analyze_game_detailed(pgn_path: str):
    """PGN dosyasını okur, her hamleyi analiz edip JSON döner."""
    # 🧹 1. PGN dosyasını oku ve yorumları temizle
    with open(pgn_path, "r", encoding="utf-8") as f:
        raw = f.read()
    clean_pgn = re.sub(r"\{[^}]*\}", "", raw)  # yorumları sil
    pgn_io = io.StringIO(clean_pgn)

    # 🧩 2. Oyunu oku
    game = chess.pgn.read_game(pgn_io)
    if not game:
        print("❌ PGN okunamadı.")
        return {"initial_fen": chess.STARTING_FEN, "moves": []}

    # 🧠 3. Hamleleri analiz et
    board = game.board()
    timeline = []

    for move in game.mainline_moves():
        san = board.san(move)
        board.push(move)
        stockfish.set_fen_position(board.fen())
        eval_data = stockfish.get_evaluation()
        timeline.append({
            "san": san,
            "fen_after": board.fen(),
            "eval": eval_data,
            "comment": get_comment(eval_data)
        })

    return {
        "initial_fen": chess.STARTING_FEN,
        "moves": timeline
    }
