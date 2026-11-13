from tools.random_challenge import run as random_challenge
from tools.text_analyzer import run as text_analyzer

def coming_soon():
    print("Ovaj alat još nije povezan.")

TOOLS = {
    "1": ("Password Generator", coming_soon),
    "2": ("File Analyzer", coming_soon),
    "3": ("Text Analyzer", text_analyzer),
    "4": ("QR Code Generator", coming_soon),
    "5": ("System Monitor", coming_soon),
    "6": ("File Organizer", coming_soon),
    "7": ("URL & IP Tools", coming_soon),
    "8": ("Encryption Lab", coming_soon),
    "9": ("Random Challenge", random_challenge),
    "10": ("Developer Utilities", coming_soon),
}