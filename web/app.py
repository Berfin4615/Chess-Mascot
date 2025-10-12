from flask import Flask, render_template, jsonify
from pathlib import Path
import sys, os

# Proje kökünü import yoluna ekle
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from chess_engine.stockfish_engine import analyze_game_detailed

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analysis")
def api_analysis():
    pgn_path = ROOT / "games" / "latest_game.pgn"
    if not pgn_path.exists():
        return jsonify({"error": "latest_game.pgn bulunamadı. Önce bir oyun oyna/çek."}), 404
    data = analyze_game_detailed(str(pgn_path))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
