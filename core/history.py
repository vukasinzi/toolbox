import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("history.json")


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def add_entry(tool_name):
    history = load_history()
    history.append({
        "tool": tool_name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )