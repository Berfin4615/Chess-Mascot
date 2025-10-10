import os

def save_latest_game(pgn_text):
    os.makedirs("games", exist_ok=True)
    with open("games/latest_game.pgn", "w") as f:
        f.write(pgn_text)