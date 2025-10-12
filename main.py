# main.py
import requests, time
from chess_engine.pgn_utils import save_latest_game
from chess_engine.stockfish_engine import analyze_game_detailed
from ui.terminal_ui import show_analysis

username = "berfin4615"
headers = {"User-Agent": "Mozilla/5.0"}
last_game_count = 0

def get_latest_archive_url():
    res = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives", headers=headers)
    return res.json()["archives"][-1]

def get_games(archive_url):
    res = requests.get(archive_url, headers=headers)
    return res.json().get("games", [])

print("🎯 Chess-Mascot başlatıldı... Yeni oyun olduğunda analiz edeceğim!")

while True:
    try:
        archive_url = get_latest_archive_url()
        games = get_games(archive_url)
        current_count = len(games)

        if current_count > last_game_count:
            print(f"\n✅ Yeni oyun bulundu! ({current_count})\n")
            last_game = games[-1]
            save_latest_game(last_game["pgn"])

            detailed = analyze_game_detailed("games/latest_game.pgn")
            moves = detailed.get("moves", [])
            print("\n📊 Oyun Analizi:\n")
            show_analysis(moves)   # <-- SADECE LISTEYI GÖNDER

            last_game_count = current_count
        else:
            print(f"⏳ Henüz yeni oyun yok. ({current_count})")

        time.sleep(60)

    except Exception as e:
        print(f"❌ Hata: {e}")
        time.sleep(60)
