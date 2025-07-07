import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# Konfigurasi akun FaucetPay dan 2Captcha API
FAUCET_URL = "https://onlyfaucet.com/faucet/currency/pepe"  # Ganti dengan URL asli faucet
WALLET_ADDRESS = "yusdialbayck92@gmail.com"
CAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"  # Opsional, jika ingin integrasi

# Konfigurasi browser
def start_browser():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = uc.Chrome(options=options)
    return browser

# Fungsi auto claim
def claim_faucet(browser):
    browser.get(FAUCET_URL)
    time.sleep(5)  # Tunggu halaman selesai loading

    # Isi wallet
    wallet_input = browser.find_element(By.NAME, 'wallet')
    wallet_input.clear()
    wallet_input.send_keys(WALLET_ADDRESS)

    # CAPTCHA HARUS DISELESAIKAN (manual atau otomatis dengan 2Captcha jika tersedia)
    print("Silakan selesaikan captcha secara manual atau gunakan 2Captcha.")

    # Tunggu sampai captcha selesai secara manual (atau integrasi otomatis)
    input("Tekan Enter setelah captcha selesai dan Anda ingin melanjutkan...")

    # Klik tombol klaim
    claim_button = browser.find_element(By.ID, 'claim-button')  # Ganti sesuai ID tombol
    claim_button.click()

    print("Claim done.")
    time.sleep(5)

# Main loop
def main():
    browser = start_browser()
    try:
        while True:
            claim_faucet(browser)
            print("Menunggu 5 detik untuk claim berikutnya...")
            time.sleep(5)
    except KeyboardInterrupt:
        browser.quit()
        print("Bot dihentikan.")

if __name__ == '__main__':
    main()
