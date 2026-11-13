import math
import secrets
import string

COMMON_PASSWORDS = {
    "123456", "12345678", "123456789", "password", "password1", "qwerty",
    "qwerty123", "abc123", "111111", "000000", "iloveyou", "admin",
    "letmein", "welcome", "lozinka", "sifra", "srbija",
}


def generate_password(length=16, use_upper=True, use_digits=True, use_symbols=True):

    pools = [string.ascii_lowercase]
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    if length < len(pools):
        raise ValueError(f"Dužina mora biti bar {len(pools)}.")


    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]

    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def check_strength(password):

    tips = []

    if not password:
        return "Prazna lozinka", 0.0, ["Unesi lozinku."]

    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    else:
        tips.append("Dodaj mala slova.")
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    else:
        tips.append("Dodaj velika slova.")
    if any(c in string.digits for c in password):
        pool_size += 10
    else:
        tips.append("Dodaj brojeve.")
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)
    else:
        tips.append("Dodaj simbole.")
    if len(password) < 12:
        tips.append("Koristi bar 12 karaktera.")


    entropy = len(password) * math.log2(pool_size) if pool_size else 0.0

    if password.lower() in COMMON_PASSWORDS:
        return "Veoma slaba", entropy, ["Ovo je jedna od najčešćih lozinki!"]

    if len(set(password)) == 1:
        tips.append("Lozinka ima samo jedan ponavljajući karakter.")
        return "Veoma slaba", entropy, tips

    if entropy < 36:
        label = "Veoma slaba"
    elif entropy < 60:
        label = "Slaba"
    elif entropy < 80:
        label = "Srednja"
    elif entropy < 100:
        label = "Jaka"
    else:
        label = "Veoma jaka"

    return label, entropy, tips


def generate_token(nbytes=16, urlsafe=True):
    if nbytes < 1:
        raise ValueError("Broj bajtova mora biti bar 1.")
    return secrets.token_urlsafe(nbytes) if urlsafe else secrets.token_hex(nbytes)



def _ask_int(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("Neispravan broj, koristim podrazumevanu vrednost.")
        return default


def _ask_yes_no(prompt, default=True):
    hint = "D/n" if default else "d/N"
    raw = input(f"{prompt} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("d", "da", "y", "yes")



def _action_generate():
    length = _ask_int("Dužina lozinke", 16)
    upper = _ask_yes_no("Velika slova?")
    digits = _ask_yes_no("Brojevi?")
    symbols = _ask_yes_no("Simboli?")
    try:
        password = generate_password(length, upper, digits, symbols)
    except ValueError as e:
        print(f"Greška: {e}")
        return
    print(f"\nLozinka: {password}")
    label, entropy, _ = check_strength(password)
    print(f"Jačina: {label} ({entropy:.0f} bita entropije)")


def _action_check():
    password = input("Unesi lozinku za proveru: ")
    label, entropy, tips = check_strength(password)
    print(f"\nJačina: {label} ({entropy:.0f} bita entropije)")
    for tip in tips:
        print(f"  - {tip}")


def _action_token():
    nbytes = _ask_int("Broj bajtova", 16)
    urlsafe = _ask_yes_no("URL-safe format? (ne = hex)")
    try:
        print(f"\nToken: {generate_token(nbytes, urlsafe)}")
    except ValueError as e:
        print(f"Greška: {e}")




def run():
    actions = {
        "1": _action_generate,
        "2": _action_check,
        "3": _action_token,
    }
    while True:
        print("\n=== Password Generator ===")
        print("[1] Generiši lozinku")
        print("[2] Proveri jačinu lozinke")
        print("[3] Generiši random token")
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