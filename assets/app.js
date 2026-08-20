const SPREADS = {
  Mumbai: 0, Delhi: 12, Noida: 12, Bangalore: 8, Chennai: -6, Kolkata: 5,
  Hyderabad: 4, Ahmedabad: 10, Pune: 3, Jaipur: 7, Surat: 9,
};

function inr(n) {
  if (n == null || Number.isNaN(n)) return "—";
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(n);
}

function applySpread(gram, bps) {
  return Math.round(gram * 10 * (1 + bps / 10000) * 100) / 100;
}

async function loadRates() {
  const res = await fetch("rates.json", { cache: "no-store" });
  if (!res.ok) throw new Error("rates.json missing");
  return res.json();
}

function renderRates(data, citySel, out) {
  const city = citySel.value;
  const bps = SPREADS[city] ?? 0;
  const g24 = Number(data.price_gram_24k);
  const g22 = Number(data.price_gram_22k);
  const g18 = Number(data.price_gram_18k);
  out.innerHTML = `
    <p class="muted">${city} · as of ${data.as_of_ist || data.as_of || ""} IST · metal only, no making charges</p>
    <p>24K / 10 g: <span class="price">${inr(applySpread(g24, bps))}</span></p>
    <p>22K / 10 g: <span class="price">${inr(applySpread(g22, bps))}</span></p>
    <p>18K / 10 g: <span class="price">${inr(applySpread(g18, bps))}</span></p>
  `;
}

function fairValue(data, city, karat, grams) {
  const bps = SPREADS[city] ?? 0;
  const gram = karat === 24 ? data.price_gram_24k : karat === 18 ? data.price_gram_18k : data.price_gram_22k;
  const per10 = applySpread(Number(gram), bps);
  return (per10 / 10) * grams;
}

async function bootRates() {
  const citySel = document.querySelector("[name=city]");
  const out = document.querySelector("#rate-box");
  const fairOut = document.querySelector("#fair-box");
  const w = document.querySelector("[name=weight]");
  const k = document.querySelector("[name=karat]");
  if (!out) return;
  try {
    const data = await loadRates();
    const paint = () => {
      renderRates(data, citySel, out);
      if (fairOut && w && k) {
        const grams = Number(w.value);
        if (grams > 0) {
          const v = fairValue(data, citySel.value, Number(k.value), grams);
          fairOut.textContent = "Fair metal value: " + inr(v);
        } else fairOut.textContent = "";
      }
    };
    citySel.addEventListener("change", paint);
    w && w.addEventListener("input", paint);
    k && k.addEventListener("change", paint);
    paint();
  } catch (e) {
    out.innerHTML = "<p class='err'>Today's rate file is not on this host yet. Refresh after the daily job runs.</p>";
  }
}

function cfg() {
  return window.GOLDMEET || { supabaseUrl: "", supabaseAnon: "" };
}

async function sendOtp(phone) {
  const c = cfg();
  if (!c.supabaseUrl) throw new Error("Supabase URL not set. Use waitlist below.");
  const res = await fetch(c.supabaseUrl.replace(/\/$/, "") + "/functions/v1/send-otp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: c.supabaseAnon,
    },
    body: JSON.stringify({ phone }),
  });
  const body = await res.json();
  if (!res.ok || body.error) throw new Error(body.error || "OTP send failed");
  return body;
}

async function verifyOtp(phone, code) {
  const c = cfg();
  const res = await fetch(c.supabaseUrl.replace(/\/$/, "") + "/functions/v1/verify-otp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: c.supabaseAnon,
    },
    body: JSON.stringify({ phone, code }),
  });
  const body = await res.json();
  if (!res.ok || body.error) throw new Error(body.error || "OTP verify failed");
  return body;
}

function bootAuth() {
  const form = document.querySelector("#otp-form");
  if (!form) return;
  const status = document.querySelector("#otp-status");
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    status.textContent = "Sending…";
    try {
      const phone = form.phone.value.trim();
      const code = form.code.value.trim();
      if (!code) {
        const r = await sendOtp(phone);
        status.innerHTML = r.dev_code
          ? `<span class="ok">Dev OTP ${r.dev_code}</span>`
          : `<span class="ok">OTP sent to ${phone}</span>`;
      } else {
        await verifyOtp(phone, code);
        status.innerHTML = `<span class="ok">Phone verified. Welcome to GoldMeet.</span>`;
        localStorage.setItem("goldmeet_phone", phone);
      }
    } catch (e) {
      status.innerHTML = `<span class="err">${e.message}</span>`;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const city = new URLSearchParams(location.search).get("city");
  const q = new URLSearchParams(location.search);
  ["utm_source", "utm_campaign", "utm_medium"].forEach((k) => {
    const v = q.get(k);
    const el = document.querySelector(`[name="${k}"]`);
    if (v && el) el.value = v;
  });
  if (city) {
    document.querySelectorAll("select[name=city]").forEach((el) => {
      const hit = [...el.options].find((o) => o.value === city || o.text === city);
      if (hit) el.value = hit.value;
    });
  }
  bootRates();
  bootAuth();
});
