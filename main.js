const axios = require('axios');
const cheerio = require('cheerio');

const URL = 'https://onlyfaucet.com/faucet/currency/pepe';
const WALLET = 'yusdialbayck92@gmail.com'; // ganti dengan wallet kamu
const CAPTCHA_API_KEY = '7fa9fe01d6e280530733092087f3d2bd'; // API Key kamu
const COOLDOWN = 60 * 60 * 1000;

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/x-www-form-urlencoded'
};

async function solveCaptcha(sitekey, pageurl) {
  const res = await axios.post('http://2captcha.com/in.php', null, {
    params: {
      key: CAPTCHA_API_KEY,
      method: 'hcaptcha',
      sitekey,
      pageurl,
      json: 1
    }
  });

  if (res.data.status !== 1) throw new Error('Submit captcha gagal');

  const requestId = res.data.request;
  console.log('[⏳] Menunggu hasil captcha...');

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
}

async function claimFaucet() {
  try {
    const session = axios.create({ headers, withCredentials: true });

    // GET halaman utama, simpan cookie & CSRF
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

    const csrf = $('input[name="csrf_token"]').val();
    if (!csrf) {
      console.log('[❌] CSRF token tidak ditemukan!');
      return false;
    }

    const captchaToken = await solveCaptcha(sitekey, URL);

    const formData = new URLSearchParams();
    formData.append('wallet_address', WALLET);
    formData.append('h-captcha-response', captchaToken);
    formData.append('csrf_token', csrf);

    // Kirim POST dengan header & cookie
    const claim = await session.post(URL, formData.toString(), {
      headers: {
        ...headers,
        'Referer': URL,
        'Origin': 'https://onlyfaucet.com'
      }
    });

    if (claim.data.toLowerCase().includes('success')) {
      console.log('[🎉] Klaim berhasil!');
      return true;
    } else {
      console.log('[⚠️] Klaim ditolak. Periksa token captcha / CSRF.');
      return false;
    }

  } catch (err) {
    console.error('[💥] ERROR:', err.message);
    if (err.response) {
      console.error('→ Status:', err.response.status);
      console.error('→ Body:', err.response.data?.slice(0, 300));
    }
    return false;
  }
}

(async () => {
  while (true) {
    const result = await claimFaucet();

    if (result) {
      console.log(`[🕓] Menunggu ${COOLDOWN / 60000} menit...`);
      await new Promise(resolve => setTimeout(resolve, COOLDOWN));
    } else {
      console.log('[🔁] Coba lagi dalam 10 menit...');
      await new Promise(resolve => setTimeout(resolve, 600000));
    }
  }
})();
