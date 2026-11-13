import csv
import json
import statistics
from pathlib import Path


def validate_json(text):
    try:
        json.loads(text)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"{e.msg} (line {e.lineno}, column {e.colno})"


def format_json(text, indent=4):
    data = json.loads(text)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def to_number(value):
    try:
        return float(value.strip().replace(",", "."))
    except (ValueError, AttributeError):
        return None


def detect_delimiter(sample):
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
    except csv.Error:
        return ","


def csv_stats(path):
    content = Path(path).read_text(encoding="utf-8-sig")
    delimiter = detect_delimiter(content[:2048])
    rows = list(csv.DictReader(content.splitlines(), delimiter=delimiter))
    columns = list(rows[0].keys()) if rows else []

    column_stats = {}
    for column in columns:
        values = [(row[column] or "").strip() for row in rows]
        filled = [value for value in values if value]
        numbers = [to_number(value) for value in filled]

        stats = {"empty": len(values) - len(filled)}
        if filled and all(number is not None for number in numbers):
            stats["type"] = "number"
            stats["min"] = min(numbers)
            stats["max"] = max(numbers)
            stats["avg"] = round(statistics.mean(numbers), 2)
        else:
            stats["type"] = "text"
            stats["unique"] = len(set(filled))
        column_stats[column] = stats

    return {
        "rows": len(rows),
        "columns": columns,
        "delimiter": delimiter,
        "stats": column_stats,
    }


def read_from_keyboard():
    print("Paste JSON (empty line to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def read_file(prompt):
    path = Path(input(prompt).strip())
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print("File not found.")
    except IsADirectoryError:
        print("That is a folder, not a file.")
    except PermissionError:
        print("No permission to read this file.")
    except UnicodeDecodeError:
        print("File is not a text file.")
    return None


def read_json_input():
    print("[1] Paste JSON")
    print("[2] Load from file")
    choice = input("Select > ").strip()
    if choice == "1":
        return read_from_keyboard()
    if choice == "2":
        return read_file("JSON file path > ")
    print("Invalid choice.")
    return None


def json_validator():
    text = read_json_input()
    if not text or not text.strip():
        print("No JSON to check.")
        return
    valid, error = validate_json(text)
    if valid:
        print("\nJSON is valid.")
    else:
        print(f"\nJSON is NOT valid: {error}")


def json_formatter():
    text = read_json_input()
    if not text or not text.strip():
        print("No JSON to format.")
        return
    valid, error = validate_json(text)
    if not valid:
        print(f"\nCannot format, JSON is NOT valid: {error}")
        return
    print("\n" + format_json(text))


def csv_statistics():
    path = input("CSV file path > ").strip()
    try:
        result = csv_stats(path)
    except FileNotFoundError:
        print("File not found.")
        return
    except IsADirectoryError:
        print("That is a folder, not a file.")
        return
    except PermissionError:
        print("No permission to read this file.")
        return
    except UnicodeDecodeError:
        print("File is not a text file.")
        return

    if not result["columns"]:
        print("CSV file is empty.")
        return

    delimiter_name = {",": "comma", ";": "semicolon", "\t": "tab"}[result["delimiter"]]
    print("\n--- CSV STATISTICS ---")
    print(f"{'Rows:':<15}{result['rows']}")
    print(f"{'Columns:':<15}{len(result['columns'])}")
    print(f"{'Separator:':<15}{delimiter_name}")

    for column, stats in result["stats"].items():
        print(f"\n{column} ({stats['type']})")
        if stats["type"] == "number":
            print(f"  min: {stats['min']}, max: {stats['max']}, avg: {stats['avg']}")
        else:
            print(f"  unique values: {stats['unique']}")
        print(f"  empty cells: {stats['empty']}")


def run():
    while True:
        print("\n=== DEVELOPER UTILITIES ===")
        print("[1] JSON validator")
        print("[2] JSON formatter")
        print("[3] CSV statistics")
        print("[0] Back")
        choice = input("Select > ").strip()

        if choice == "1":
            json_validator()
        elif choice == "2":
            json_formatter()
        elif choice == "3":
            csv_statistics()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()
