import os
from pathlib import Path
import hashlib

def calculate_file_hash(file_path, chunk_size=8192):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(chunk_size), b''):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, OSError):
        return None

def analyze_folder():
    path_str = input("\nUnesite apsolutnu ili relativnu putanju do foldera za analizu: ").strip()
    folder = Path(path_str)

    if not folder.exists() or not folder.is_dir():
        print("[-] Greska: Uneta putanja ne postoji ili nije direktorijum")
        return

    print(f"\n[+] Analiziram folder: {folder.resolve()}... Molimo sacekajte.\n")

    total_files = 0
    total_folders = 0
    total_size_bytes = 0
    extension_stats = {}
    file_list = []

    for item in folder.rglob("*"):
        # Opcionalno preskakanje teških sistemskih foldera (poput node_modules, .git, venv)
        if any(part in item.parts for part in ['node_modules', '.git', 'venv', '__pycache__']):
            continue

        if item.is_dir():
            total_folders += 1
        elif item.is_file():
            total_files += 1
            try:
                file_size = item.stat().st_size
                total_size_bytes += file_size
                file_list.append((item, file_size))

                ext = item.suffix.lower() if item.suffix else "[bez ekstenzije]"
                if ext not in extension_stats:
                    extension_stats[ext] = {"count": 0, "size": 0}
                extension_stats[ext]["count"] += 1
                extension_stats[ext]["size"] += file_size
            except (PermissionError, OSError):
                continue

    total_size_mb = total_size_bytes / 1024 / 1024

    print("=" * 40)
    print("Opsta statistika foldera")
    print("=" * 40)
    print(f"Ukupno foldera: {total_folders}")
    print(f"Ukupno fajlova: {total_files}")
    print(f"Ukupna veličina: {total_size_mb:.2f} MB")

    print("\n" + "=" * 40)
    print("STATISTIKA PO EKSTENZIJAMA")
    print("=" * 40)
    for ext, stats in sorted(extension_stats.items(), key=lambda x: x[1]["size"], reverse=True):
        size_mb = stats["size"] / (1024 * 1024)
        print(f"• {ext:<15} | Broj: {stats['count']:<5} | Veličina: {size_mb:.2f} MB")

    print("\n" + "=" * 40)
    print("TOP 5 NAJVEĆIH FAJLOVA")
    print("=" * 40)
    sorted_files = sorted(file_list, key=lambda x: x[1], reverse=True)
    for i, (f_path, f_size) in enumerate(sorted_files[:5], 1):
        size_mb = f_size / (1024 * 1024)
        print(f"{i}. {f_path.name} ({size_mb:.2f} MB)\n   Putanja: {f_path}")

    print("\n" + "=" * 40)
    print("PROVERA DUPLIKATA (PREKO SHA-256)")
    print("=" * 40)

    hash_dict = {}
    for f_path, _ in file_list:
        file_hash = calculate_file_hash(f_path)
        if file_hash:
            if file_hash in hash_dict:
                hash_dict[file_hash].append(f_path)
            else:
                hash_dict[file_hash] = [f_path]

    duplicates_found = False
    for file_hash, paths in hash_dict.items():
        if len(paths) > 1:
            duplicates_found = True
            print(f"\n[!] Pronađeni identični fajlovi (Duplikati):")
            for p in paths:
                print(f"    - {p}")

    if not duplicates_found:
        print("[o] Nisu pronađeni duplikati u ovom folderu.")
    print("\n" + "=" * 40)

def run():
    """Glavna funkcija koju poziva glavni meni aplikacije."""
    analyze_folder()

if __name__ == "__main__":
    run()