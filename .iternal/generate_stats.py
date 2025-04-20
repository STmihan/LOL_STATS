import csv
import os

STATS_FOLDER = 'stats'
OUTPUT_FILE = '../Pick Statistics $%.md'
COLUMNS_TO_KEEP = ['Champion', 'Picks', 'Bans', 'PrioScore', 'Wins', 'Losses', 'Winrate']

def sanitize_champion_name(name):
    return name.replace("'", "").replace(".", "").replace(" ", "")

def normalize_name(name: str) -> str:
    parts = name.split()
    if len(parts) % 2 == 0 and parts[:len(parts)//2] == parts[len(parts)//2:]:
        return ' '.join(parts[:len(parts)//2])
    return name

def read_stat(file: str) -> list:
    with open(file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        rows = []

        for row in reader:
            if row['Picks'].isdigit() and row['Bans'].isdigit():
                if int(row['Picks']) == 0 and int(row['Bans']) == 0:
                    continue

                champion = normalize_name(row['Champion'])
                icon_url = f"https://gol.gg/_img/champions_icon/{sanitize_champion_name(champion)}.png"
                filtered = {
                    **{key: row[key] for key in COLUMNS_TO_KEEP}
                }
                # filtered['Champion'] = f'![]({icon_url})({row["Champion"]})'
                filtered['Champion'] = f'<div align="center"><img src="{icon_url}" width="48"/><br>{normalize_name(row["Champion"])}</div>'

                rows.append(filtered)
        return rows

def generate_markdown(stats: list, name: str):
    filename = OUTPUT_FILE.replace('$%', name)
    headers = COLUMNS_TO_KEEP
    with open(filename, 'w', encoding='utf-8') as out:
        out.write("---\n")
        out.write("cssclasses:\n")
        out.write(" - pick_statistics\n")
        out.write("---\n")
        out.write('| ' + ' | '.join(headers) + ' |\n')
        out.write('| ' + ' | '.join([':---:'] * len(headers)) + ' |\n')

        for row in stats:
            out.write('| ' + ' | '.join(row[col] for col in headers) + ' |\n')


def main():
    stats_list = os.listdir(STATS_FOLDER)
    for stat_file in stats_list:
        if not stat_file.endswith('.csv'):
            continue

        stat_path = os.path.join(STATS_FOLDER, stat_file)
        stats = read_stat(stat_path)

        if not stats:
            print(f"[!] No valid rows found in {stat_path}.")
            continue

        name = stat_file.split('.')[0]
        generate_markdown(stats, name)
        print(f"[✓] Markdown saved: {OUTPUT_FILE.replace('$%', name)}")

if __name__ == '__main__':
    main()
