import os
from pathlib import Path
import shutil

EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.odt', '.md'],
    'Code_Archives': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.json', '.xml', '.zip', '.rar', '.tar', '.gz', '.7z'],
    'Media': ['.mp3', '.mp4', '.wav', '.avi', '.mkv', '.flac', '.mov']
}

def get_category(ext):
    ext = ext.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return "Others"

def organize_folder():
    path_str = input("\nUnesite putanju do foldera koji želite da organizujete: ").strip()
    folder = Path(path_str)

    if not folder.exists() or not folder.is_dir():
        print("[-] Greška: Uneta putanja ne postoji ili nije direktorijum.")
        return

    print(f"\n[+] Organizujem folder: {folder.resolve()} ... Molimo sačekajte.\n")

    moved_count = 0
    error_count = 0

    for item in folder.iterdir():
        if item.is_file():
            if item.name.startswith('.'):
                continue

            ext = item.suffix.lower()
            category = get_category(ext)

            target_folder = folder / category
            target_folder.mkdir(exist_ok=True)

            target_path = target_folder / item.name

            if target_path.exists():
                base_name = item.stem
                suffix = item.suffix
                counter = 1
                while target_path.exists():
                    target_path = target_folder / f"{base_name}_{counter}{suffix}"
                    counter += 1

            try:
                # Ispravljeno: prosleđuje se puna ciljna putanja sa imenom fajla
                shutil.move(str(item), str(target_path))
                print(f"Premestio: {item.name} -> {category}/")
                moved_count += 1
            except Exception as e:
                print(f"Greška pri premeštanju {item.name}: {e}")
                error_count += 1

    print("\n" + "=" * 40)
    print("✅ ORGANIZACIJA JE USPEŠNO ZAVRŠENA")
    print("=" * 40)
    print(f"Ukupno premeštenih fajlova: {moved_count}")
    if error_count > 0:
        print(f"Broj grešaka: {error_count}")
    print("=" * 40)

def run():
    """Glavna funkcija koju poziva glavni meni aplikacije."""
    organize_folder()

if __name__ == "__main__":
    run()