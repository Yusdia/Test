import requests
import time
from bs4 import BeautifulSoup

# Konfigurasi
URL = "https://onlyfaucet.com/faucet/currency/pepe"  # Ganti dengan URL faucet asli
WALLET = "yusdialbayck92@gmail.com"
CAPTCHA_API_KEY = "ISI_DENGAN_API_KEY_2CAPTCHA"
CAPTCHA_TYPE = "hcaptcha"  # ganti "hcaptcha" jika pakai hCaptcha

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Termux)"
}

def solve_captcha(sitekey, url):
    print("[🔄] Mengirim captcha ke 2Captcha...")
    if CAPTCHA_TYPE == "recaptcha":
        captcha_type = "userrecaptcha"
    else:
        captcha_type = "hcaptcha"

    payload = {
        'key': CAPTCHA_API_KEY,
        'method': captcha_type,
        'googlekey': sitekey,
        'pageurl': url,
        'json': 1
    }

    r = requests.post('http://2captcha.com/in.php', data=payload)
    request_id = r.json()["request"]
    print("[⏳] Menunggu hasil captcha...")

    for _ in range(30):
        time.sleep(5)
        res = requests.get(f"http://2captcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={request_id}&json=1")
        if res.json()["status"] == 1:
            print("[✅] Captcha berhasil dipecahkan.")
            return res.json()["request"]
    raise Exception("Captcha gagal diselesaikan.")

def claim_faucet():
    session = requests.Session()
    r = session.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Ambil sitekey dari reCAPTCHA/hCaptcha
    if CAPTCHA_TYPE == "hcaptcha":
        sitekey_tag = soup.find("div", {"class": "g-recaptcha"})
    else:
        sitekey_tag = soup.find("div", {"class": "h-captcha"})

    sitekey = sitekey_tag["data-sitekey"]
    print(f"[🔑] Sitekey ditemukan: {sitekey}")

    captcha_token = solve_captcha(sitekey, URL)

    # Ambil CSRF token jika ada
    csrf = soup.find("input", {"name": "csrf_token"})
    csrf_token = csrf["value"] if csrf else ""

    # Kirim form klaim
    data = {
        "wallet": WALLET,
        "g-recaptcha-response" if CAPTCHA_TYPE == "recaptcha" else "h-captcha-response": captcha_token,
        "csrf_token": csrf_token
    }

    claim = session.post(URL, data=data, headers=headers)
    if "Success" in claim.text or "claimed" in claim.text:
        print("[🎉] Klaim berhasil!")
    else:
        print("[⚠️] Gagal klaim atau captcha salah!")

while True:
    try:
        claim_faucet()
        print("⏳ Menunggu 5 detik sebelum klaim ulang...")
        time.sleep(5)
    except Exception as e:
        print(f"[❌] Error: {e}")
        break
