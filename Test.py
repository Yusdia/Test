import requests
import time

API_KEY = 'API_2CAPTCHA_ANDA'
FAUCET_URL = 'https://example-faucet.com/claim'
CAPTCHA_SITEKEY = 'SITEKEY_CAPTCHA_DI_HALAMAN'
PAGE_URL = 'https://example-faucet.com/claim'

def solve_captcha(api_key, sitekey, url):
    # Kirim permintaan ke 2Captcha
    captcha_id = requests.post("http://2captcha.com/in.php", data={
        'key': api_key,
        'method': 'userrecaptcha',
        'googlekey': sitekey,
        'pageurl': url,
        'json': 1
    }).json()['request']

    # Tunggu hasilnya
    for i in range(20):
        time.sleep(5)
        response = requests.get("http://2captcha.com/res.php", params={
            'key': api_key,
            'action': 'get',
            'id': captcha_id,
            'json': 1
        }).json()
        if response['status'] == 1:
            return response['request']
    return None

def auto_claim():
    token = solve_captcha(API_KEY, CAPTCHA_SITEKEY, PAGE_URL)
    if not token:
        print("Gagal menyelesaikan captcha.")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'g-recaptcha-response': token,
        # Parameter lain tergantung situsnya
    }

    response = requests.post(FAUCET_URL, data=data, headers=headers)
    print("Status klaim:", response.text)

# Eksekusi
auto_claim()
          
