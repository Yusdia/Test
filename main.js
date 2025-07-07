const axios = require('axios');
const cheerio = require('cheerio');

const URL = 'https://onlyfaucet.com/faucet/currency/pepe';
const WALLET = 'yusdialbayck92@gmail.com';
const CAPTCHA_API_KEY = '7fa9fe01d6e280530733092087f3d2bd';
const COOLDOWN = 60 * 60 * 1000; // 1 jam

const headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Termux)'
};

async function solveCaptcha(sitekey, pageurl) {
  try {
    const res = await axios.post('http://2captcha.com/in.php', null, {
      params: {
        key: CAPTCHA_API_KEY,
        method: 'hcaptcha',
        sitekey: sitekey,
        pageurl: pageurl,
        json: 1
      }
    });

    if (res.data.status !== 1) throw new Error('Gagal submit captcha');

    const requestId = res.data.request;
    console.log('[⏳] Menunggu captcha...');

    for (let i = 0; i < 40; i++) {
      await new Promise(resolve => setTimeout(resolve, 5000));
      const result = await axios.get('http://2captcha.com/res.php', {
        params: {
          key: CAPTCHA_API_KEY,
          action: 'get',
          id: requestId,
          json: 1
        }
      });

      if (result.data.status === 1) {
        console.log('[✅] Captcha berhasil diselesaikan.');
        return result.data.request;
      }
    }

    throw new Error('Captcha timeout');
  } catch (err) {
    throw new Error('[❌] Captcha error: ' + err.message);
  }
}

async function claimFaucet() {
  try {
    const session = axios.create({ headers });

    // Step 1: Load page
    const response = await session.get(URL);
    const $ = cheerio.load(response.data);

    if ($('body').text().toLowerCase().includes('already claimed')) {
      console.log('[🕒] Faucet masih cooldown. Tunggu 1 jam.');
      return false;
    }

    const sitekey = $('.h-captcha').attr('data-sitekey');
    if (!sitekey) {
      console.log('[❌] Sitekey tidak ditemukan!');
      return false;
    }

    const csrf = $('input[name="csrf_token"]').val() || '';

    const captchaToken = await solveCaptcha(sitekey, URL);

    const formData = new URLSearchParams();
    formData.append('wallet_address', WALLET);
    formData.append('h-captcha-response', captchaToken);
    formData.append('csrf_token', csrf);

    const result = await session.post(URL, formData.toString(), {
      headers: {
        ...headers,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    if (result.data.toLowerCase().includes('success')) {
      console.log('[🎉] Berhasil klaim faucet!');
      return true;
    } else {
      console.log('[⚠️] Klaim gagal atau captcha salah.');
      return false;
    }

  } catch (err) {
    console.error('[💥] ERROR:', err.message);
    return false;
  }
}

(async () => {
  while (true) {
    const result = await claimFaucet();

    if (result) {
      console.log(`[🕓] Menunggu ${COOLDOWN / 60000} menit (cooldown faucet)...`);
      await new Promise(resolve => setTimeout(resolve, COOLDOWN));
    } else {
      console.log('[🔁] Coba lagi dalam 10 menit...');
      await new Promise(resolve => setTimeout(resolve, 600000));
    }
  }
})();
