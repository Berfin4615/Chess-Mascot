from chess_engine.stockfish_engine import analyze_game_detailed
import json

data = analyze_game_detailed("games/latest_game.pgn")
print(json.dumps(data, indent=2)[:500])
