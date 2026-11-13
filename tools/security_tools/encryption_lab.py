import base64
import binascii
import hashlib


def sha256_hash(text):
    """Vraća SHA-256 hash teksta kao hex string (64 znaka)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_hash(text, expected_hash):
    """True ako SHA-256 hash teksta odgovara očekivanom hashu."""
    return sha256_hash(text) == expected_hash.strip().lower()


def base64_encode(text):
    """Pretvara običan tekst u Base64."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def base64_decode(encoded):
    """Pretvara Base64 nazad u tekst. Baca ValueError ako unos nije ispravan."""
    try:
        raw = base64.b64decode(encoded.strip(), validate=True)
        return raw.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as e:
        raise ValueError("Neispravan Base64 unos.") from e



def _action_hash():
    text = input("Unesi tekst: ")
    print(f"\nSHA-256: {sha256_hash(text)}")


def _action_verify():
    text = input("Unesi tekst: ")
    expected = input("Unesi hash za poređenje: ")
    if verify_hash(text, expected):
        print("\nHash se poklapa.")
    else:
        print("\nHash se NE poklapa.")


def _action_encode():
    text = input("Unesi tekst: ")
    print(f"\nBase64: {base64_encode(text)}")


def _action_decode():
    encoded = input("Unesi Base64 string: ")
    try:
        print(f"\nTekst: {base64_decode(encoded)}")
    except ValueError as e:
        print(f"Greška: {e}")



def run():
    actions = {
        "1": _action_hash,
        "2": _action_verify,
        "3": _action_encode,
        "4": _action_decode,
    }
    while True:
        print("\n=== Encryption Lab ===")
        print("[1] SHA-256 hash teksta")
        print("[2] Proveri hash")
        print("[3] Base64 encode")
        print("[4] Base64 decode")
        print("[0] Nazad")
        choice = input("Select > ").strip()

        if choice == "0":
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Nepoznata opcija.")


if __name__ == "__main__":
    run()