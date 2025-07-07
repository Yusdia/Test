import requests
import time
from bs4 import BeautifulSoup

url = "https://onlyfaucet.com/faucet/currency/pepe"  # ganti dengan faucet URL yang valid
wallet_address = yusdialbayck92@gmail.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Termux)"
}

def auto_claim():
    session = requests.Session()
    
    # Kunjungi halaman awal faucet
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari token atau input hidden kalau ada (contoh)
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"] if soup.find("input", {"name": "csrf_token"}) else ""

    # Kirim klaim
    data = {
        "wallet": wallet_address,
        "csrf_token": csrf_token
    }

    claim = session.post(url, data=data, headers=headers)
    
    if "Success" in claim.text:
        print("✅ Berhasil klaim faucet!")
    else:
        print("⚠️ Gagal klaim atau butuh captcha")

while True:
    auto_claim()
    print("⏳ Menunggu 5 detik...")
    time.sleep(5)
