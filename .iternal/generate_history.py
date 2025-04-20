import requests
import json
import os
import time

URL = "https://gol.gg/esports/ajax.home.php"
CACHE_FILE = "cached_games.json"
MD_FILE = "../Pro Games.md"
MAX_GAMES = 150


def fetch_last_games():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PHPSESSID=ahe7phs4o2eslcqgcp85q0npik; _ga=GA1.1.1819550386.1745156434; _ga_J1K08MER9S=GS1.1.1745156434.1.1.1745157798.0.0.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }
    games = []

    for start in range(0, MAX_GAMES, 10):
        data = {"start": str(start)}
        r = requests.post(URL, data=data, headers=headers)
        r.raise_for_status()
        games += r.json()
        print(f"[i] Found {len(games)} games.")
        time.sleep(4)

    return games


def cache_games(games):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)


def load_cached_games():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def generate_markdown(games):
    def champ_icon(name):
        url = f"https://gol.gg/_img/champions_icon/{name.replace(' ', '')}.png"
        return f'<div align="center"><img src="{url}" width="48"/><br>{name}</div>'

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("cssclasses:\n")
        f.write(" - pick_statistics\n")
        f.write("---\n")
        for game in games:
            f.write(f"##### {game['game_name']} ({game['game_date']}) — {game['tournament']}\n\n")
            f.write("| Top | Jungle | Mid | Bot | Support |\n")
            f.write("|:---:|:------:|:---:|:---:|:-------:|\n")
            f.write(f"|" +
                    f"{champ_icon(game['bluetop_name'])}| " +
                    f"{champ_icon(game['bluejgl_name'])}| " +
                    f"{champ_icon(game['bluemid_name'])}| " +
                    f"{champ_icon(game['bluebot_name'])}| " +
                    f"{champ_icon(game['bluesup_name'])}|\n")
            f.write(f"|" +
                    f"{champ_icon(game['redtop_name'])}| " +
                    f"{champ_icon(game['redjgl_name'])}| " +
                    f"{champ_icon(game['redmid_name'])}| " +
                    f"{champ_icon(game['redbot_name'])}| " +
                    f"{champ_icon(game['redsup_name'])}|\n\n")


def main():
    games = load_cached_games()
    
    if games is None:
        print("[i] No cache found. Fetching from server...")
        try:
            games = fetch_last_games()
            cache_games(games)
        except Exception as e:
            print(f"[!] Failed to fetch games: {e}")
            print("[✗] No data available.")
            return

    generate_markdown(games)
    print(f"[✓] Markdown saved: {MD_FILE}")


if __name__ == "__main__":
    main()
