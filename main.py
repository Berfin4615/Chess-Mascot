import requests
import time

username = "berfin4615"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# En son bilinen oyun ID (basit olarak oyun sayısı da olabilir)
last_game_count = 0

def get_latest_archive_url():
    res = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives", headers=headers)
    data = res.json()
    return data["archives"][-1]  # En güncel ay

def get_game_count(archive_url):
    res = requests.get(archive_url, headers=headers)
    data = res.json()
    return len(data.get("games", []))

print("⏳ Takip başlatıldı. Yeni oyun oynandığında haber vereceğim...")

while True:
    try:
        latest_archive = get_latest_archive_url()
        current_count = get_game_count(latest_archive)

        if current_count > last_game_count:
            print(f"✅ Yeni bir oyun oynadın! 🎉 Toplam oyun sayısı: {current_count}")
            last_game_count = current_count
        else:
            print(f"🔁 Henüz yeni bir oyun yok. (Toplam: {current_count})")

        time.sleep(60)  # Her 60 saniyede bir kontrol et
    except Exception as e:
        print(f"❌ Hata: {e}")
        time.sleep(60)
