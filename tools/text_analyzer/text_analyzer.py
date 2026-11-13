import re
from collections import Counter
from pathlib import Path

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def count_words(text):
    return len([word for word in text.split() if re.search(r"\w", word)])


def count_characters(text, include_spaces=True):
    if include_spaces:
        return len(text)
    return len(re.sub(r"\s", "", text))


def count_sentences(text):
    sentences = re.split(r"[.!?]+(?=\s|$)", text)
    return len([sentence for sentence in sentences if sentence.strip()])


def most_common_words(text, n=5):
    text_without_emails = EMAIL_PATTERN.sub(" ", text)
    words = re.findall(r"\w+", text_without_emails.lower())
    return Counter(words).most_common(n)


def find_emails(text):
    return list(dict.fromkeys(EMAIL_PATTERN.findall(text)))


def read_from_keyboard():
    print("Enter text (empty line to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def read_from_file():
    path = Path(input("File path > ").strip())
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("File not found.")
    except IsADirectoryError:
        print("That is a folder, not a file.")
    except UnicodeDecodeError:
        print("File is not a text file.")
    return None


def read_text():
    print("[1] Type text")
    print("[2] Load from file")
    choice = input("Select > ").strip()
    if choice == "1":
        return read_from_keyboard()
    if choice == "2":
        return read_from_file()
    print("Invalid choice.")
    return None


def print_report(text):
    print("\n--- REPORT ---")
    print(f"{'Words:':<30}{count_words(text)}")
    print(f"{'Characters (with spaces):':<30}{count_characters(text)}")
    print(f"{'Characters (without spaces):':<30}{count_characters(text, include_spaces=False)}")
    print(f"{'Sentences:':<30}{count_sentences(text)}")

    print("\nTop 5 words:")
    for word, count in most_common_words(text):
        print(f"  {word}: {count}")

    emails = find_emails(text)
    print(f"\nEmails found ({len(emails)}):")
    for email in emails:
        print(f"  {email}")


def run():
    while True:
        print("\n=== TEXT ANALYZER ===")
        text = read_text()
        if text and text.strip():
            print_report(text)
        else:
            print("No text to analyze.")

        again = input("\nAnalyze another text? (y/n) > ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    run()
