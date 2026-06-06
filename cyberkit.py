#!/usr/bin/env python3
import hashlib
import random
import string
import base64
import sys
import time
import os


# ── ANSI color helpers ────────────────────────────────────────────────────────
def c(text, code):
    return f"\033[{code}m{text}\033[0m"

def RED(t):     return c(t, "91")
def GREEN(t):   return c(t, "92")
def YELLOW(t):  return c(t, "93")
def CYAN(t):    return c(t, "96")
def BOLD(t):    return c(t, "1")
def DIM(t):     return c(t, "2")
def MAGENTA(t): return c(t, "95")


# ── Banner ────────────────────────────────────────────────────────────────────
BANNER = CYAN("""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗████████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██║╚══██╔══╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ██║   ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██║   ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║   ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝""")

SUBTITLE = DIM("    by Jaden  |  v1.0\n")

MENU = (
    "\n"
    f"  {BOLD('[ 1 ]')}  {YELLOW('Password Strength Analyzer')}\n"
    f"  {BOLD('[ 2 ]')}  {YELLOW('Secure Password Generator')}\n"
    f"  {BOLD('[ 3 ]')}  {YELLOW('Caesar Cipher  (encode / decode)')}\n"
    f"  {BOLD('[ 4 ]')}  {YELLOW('Base64  (encode / decode)')}\n"
    f"  {BOLD('[ 5 ]')}  {YELLOW('Hash Generator  (MD5 · SHA-1 · SHA-256 · SHA-512)')}\n"
    f"  {BOLD('[ 6 ]')}  {YELLOW('Hacker Typing Effect  🎬')}\n"
    f"  {BOLD('[ 0 ]')}  {DIM('Exit')}\n"
)


def separator(char="─", width=64, color=DIM):
    print(color(char * width))


def header(title):
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    print(SUBTITLE)
    separator()
    print(f"  {MAGENTA('▶')}  {BOLD(title)}")
    separator()
    print()


def press_enter():
    print()
    input(DIM("  Press Enter to return to menu..."))


# ── 1. Password Strength Analyzer ────────────────────────────────────────────
def analyze_password():
    header("Password Strength Analyzer")
    pwd = input(f"  {CYAN('Enter a password to analyze:')} ")
    print()

    checks = {
        "At least 8 characters":         len(pwd) >= 8,
        "At least 12 characters":        len(pwd) >= 12,
        "Contains lowercase letters":    any(ch.islower() for ch in pwd),
        "Contains uppercase letters":    any(ch.isupper() for ch in pwd),
        "Contains digits":               any(ch.isdigit() for ch in pwd),
        "Contains special characters":   any(ch in string.punctuation for ch in pwd),
        "No common patterns (123, abc)": not any(
            p in pwd.lower() for p in ["123", "abc", "qwerty", "password", "111", "000"]
        ),
    }

    score = sum(checks.values())
    total = len(checks)

    for label, passed in checks.items():
        icon  = GREEN("  ✔") if passed else RED("  ✘")
        text  = label if passed else DIM(label)
        print(f"{icon}  {text}")

    print()
    bar_filled = int((score / total) * 30)
    bar = GREEN("█" * bar_filled) + DIM("░" * (30 - bar_filled))
    print(f"  Strength  [{bar}]  {score}/{total}")
    print()

    if score >= 6:
        rating = GREEN("STRONG 🔒")
    elif score >= 4:
        rating = YELLOW("MODERATE ⚠️")
    else:
        rating = RED("WEAK 🚨")
    print(f"  Rating: {BOLD(rating)}")

    # Entropy estimate
    import math
    charset = 0
    if any(ch.islower() for ch in pwd):
        charset += 26
    if any(ch.isupper() for ch in pwd):
        charset += 26
    if any(ch.isdigit() for ch in pwd):
        charset += 10
    if any(ch in string.punctuation for ch in pwd):
        charset += 32
    if charset > 0:
        entropy = len(pwd) * math.log2(charset)
        print(f"  Entropy:  {CYAN(f'{entropy:.1f} bits')}")

    press_enter()


# ── 2. Password Generator ─────────────────────────────────────────────────────
def generate_password():
    header("Secure Password Generator")
    try:
        length = int(input(f"  {CYAN('Password length')} {DIM('[default: 16]')}: ") or "16")
        length = max(8, min(length, 128))
    except ValueError:
        length = 16

    print()
    use_upper  = input(f"  Include {YELLOW('uppercase')} letters? {DIM('[Y/n]')} ").strip().lower() != "n"
    use_digits = input(f"  Include {YELLOW('digits')}?           {DIM('[Y/n]')} ").strip().lower() != "n"
    use_syms   = input(f"  Include {YELLOW('symbols')}?          {DIM('[Y/n]')} ").strip().lower() != "n"
    print()

    pool = string.ascii_lowercase
    guaranteed = [random.choice(string.ascii_lowercase)]
    if use_upper:
        pool += string.ascii_uppercase
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_digits:
        pool += string.digits
        guaranteed.append(random.choice(string.digits))
    if use_syms:
        pool += string.punctuation
        guaranteed.append(random.choice(string.punctuation))

    remaining = [random.choice(pool) for _ in range(length - len(guaranteed))]
    pwd_list  = guaranteed + remaining
    random.shuffle(pwd_list)
    pwd = "".join(pwd_list)

    print(f"  {DIM('Generating...')} ", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(DIM("."), end="", flush=True)
    print()
    print()
    separator("─", 64)
    print(f"  {BOLD(GREEN(pwd))}")
    separator("─", 64)
    print(f"  Length: {CYAN(str(length))} characters")
    print(f"  Strength tip: {DIM('Store this in a password manager!')}")

    press_enter()


# ── 3. Caesar Cipher ──────────────────────────────────────────────────────────
def caesar_cipher():
    header("Caesar Cipher")
    print(f"  {DIM('The classic substitution cipher, shifting letters by a fixed amount.')}")
    print()
    mode  = input(f"  {CYAN('[E]ncode')} or {YELLOW('[D]ecode')}? ").strip().lower()
    text  = input("  Enter text: ")
    try:
        shift = int(input(f"  Shift amount {DIM('[1-25, default: 13]')}: ") or "13") % 26
    except ValueError:
        shift = 13

    if mode == "d":
        shift = (26 - shift) % 26

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    result = "".join(result)

    print()
    label = "Decoded" if mode == "d" else "Encoded"
    separator()
    print(f"  Original : {DIM(text)}")
    print(f"  {label:8}: {GREEN(result)}  {DIM(f'(shift={shift})')}")
    separator()

    press_enter()


# ── 4. Base64 ─────────────────────────────────────────────────────────────────
def base64_tool():
    header("Base64 Encoder / Decoder")
    print(f"  {DIM('Base64 encodes binary data as ASCII — used everywhere in web & security.')}")
    print()
    mode = input(f"  {CYAN('[E]ncode')} or {YELLOW('[D]ecode')}? ").strip().lower()
    text = input("  Enter text: ")
    print()

    try:
        if mode == "d":
            result = base64.b64decode(text.encode()).decode(errors="replace")
            label  = "Decoded"
        else:
            result = base64.b64encode(text.encode()).decode()
            label  = "Encoded"
        separator()
        print(f"  Original : {DIM(text)}")
        print(f"  {label:8}: {GREEN(result)}")
        separator()
    except Exception as e:
        print(RED(f"  Error: {e}"))

    press_enter()


# ── 5. Hash Generator ─────────────────────────────────────────────────────────
def hash_generator():
    header("Hash Generator")
    print(f"  {DIM('Hashes are one-way fingerprints — used in passwords, file verification & more.')}")
    print()
    text = input(f"  {CYAN('Enter text to hash:')} ")
    print()

    algos = [
        ("MD5    ", hashlib.md5,    RED("(weak — avoid for security)")),
        ("SHA-1  ", hashlib.sha1,   YELLOW("(deprecated)")),
        ("SHA-256", hashlib.sha256, GREEN("(recommended)")),
        ("SHA-512", hashlib.sha512, GREEN("(strongest)")),
    ]

    separator()
    for name, fn, note in algos:
        digest = fn(text.encode()).hexdigest()
        print(f"  {BOLD(name)}  {note}")
        print(f"  {CYAN(digest)}")
        print()
    separator()

    press_enter()


# ── 6. Hacker Typing Effect ───────────────────────────────────────────────────
HACKER_SCRIPT = (
    "[*] Initializing CyberKit v1.0...\n"
    "[*] Scanning network interfaces...\n"
    "[+] Found interface: eth0  (192.168.1.42)\n"
    "[*] Loading encryption modules... OK\n"
    "[*] Checking firewall rules...\n"
    "[+] iptables: 17 active rules detected\n"
    "[*] Running port sweep on localhost...\n"
    "[+]  22/tcp  OPEN  OpenSSH 9.2\n"
    "[+]  80/tcp  OPEN  Apache/2.4.57\n"
    "[+] 443/tcp  OPEN  nginx/1.24\n"
    "[*] Enumerating users...\n"
    "[+] Found: root, daemon, jaden\n"
    "[*] Checking password hashes...\n"
    "[+] SHA-256 integrity verified ✔\n"
    "[*] Generating 4096-bit RSA key pair...\n"
    "[+] Private key saved → ~/.ssh/id_rsa\n"
    "[+] Public  key saved → ~/.ssh/id_rsa.pub\n"
    "[*] All systems nominal. Stay safe out there. 🔐\n"
)


def hacker_effect():
    header("Hacker Typing Effect  🎬")
    print(f"  {DIM('Simulated terminal output — 100% harmless, 100% impressive.')}")
    print()
    input(f"  {CYAN('Press Enter to start the show...')}")
    print()

    for line in HACKER_SCRIPT.strip().splitlines():
        if line.startswith("[+]"):
            print(GREEN(line))
        elif line.startswith("[*]"):
            print(CYAN(line))
        else:
            print(line)
        time.sleep(random.uniform(0.08, 0.35))

    press_enter()


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    actions = {
        "1": analyze_password,
        "2": generate_password,
        "3": caesar_cipher,
        "4": base64_tool,
        "5": hash_generator,
        "6": hacker_effect,
    }

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        print(SUBTITLE)
        separator()
        print(MENU)
        separator()
        choice = input(f"\n  {CYAN('Select an option:')} ").strip()

        if choice == "0":
            print()
            print(CYAN("  Stay safe. Stay curious. Goodbye! 👾"))
            print()
            sys.exit(0)
        elif choice in actions:
            actions[choice]()
        else:
            print(RED("\n  Invalid option. Try again."))
            time.sleep(1)


if __name__ == "__main__":
    main()
