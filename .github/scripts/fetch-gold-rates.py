"""Write an India jewellery-board gold snapshot.

Primary source is IBJA (per 10 g, excluding GST and making charges).
GoldAPI XAU/INR is international spot, not the Indian board; it is only used
as a fallback after applying the May 2026 15% import duty.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo

    IST = ZoneInfo("Asia/Kolkata")
except Exception:  # pragma: no cover - Windows without tzdata
    IST = None

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "rates.json")
KEY = os.environ.get("GOLDAPI_KEY", "").strip()
IBJA_URL = "https://ibjarates.com/"
CONTENTS_URL = "https://api.github.com/repos/mjk93447-cpu/goldguideapp-site/contents/rates.json?ref=main"
RAW_URL = os.environ.get(
    "GOLD_RATE_SYNC_URL",
    "https://raw.githubusercontent.com/mjk93447-cpu/goldguideapp-site/main/rates.json",
)

# Effective BCD + AIDC on bullion from 13 May 2026. IBJA prints rates without GST.
INDIA_IMPORT_DUTY = 0.15

IBJA_ROW = re.compile(
    r'data-label="(?P<session>AM|PM)"><strong>(?P<date>\d{2}/\d{2}/\d{4})</strong></td>\s*'
    r'<td[^>]*data-label="Gold 999">\s*(?P<g999>[\d,]+|NA)\s*</td>\s*'
    r'<td[^>]*data-label="Gold 995">\s*(?P<g995>[\d,]+|NA)\s*</td>\s*'
    r'<td[^>]*data-label="Gold 916">\s*(?P<g916>[\d,]+|NA)\s*</td>\s*'
    r'<td[^>]*data-label="Gold 750">\s*(?P<g750>[\d,]+|NA)\s*</td>',
    re.IGNORECASE,
)

UA = {
    "User-Agent": "GoldMeet-rate-pipeline/1.0 (+https://goldguideapp.com)",
    "Accept": "text/html,application/json",
}


def _now_ist() -> datetime:
    fetched = datetime.now(timezone.utc)
    return fetched.astimezone(IST) if IST else fetched


def _parse_money(value: str) -> float | None:
    text = value.replace(",", "").strip()
    if not text or text.upper() == "NA":
        return None
    number = float(text)
    return number if number > 0 else None


def parse_ibja_html(html: str) -> dict:
    rows: list[tuple[datetime, int, dict]] = []
    for match in IBJA_ROW.finditer(html):
        per_24 = _parse_money(match.group("g999"))
        per_22 = _parse_money(match.group("g916"))
        per_18 = _parse_money(match.group("g750"))
        if not per_24 or not per_22 or not per_18:
            continue
        as_of = datetime.strptime(match.group("date"), "%d/%m/%Y")
        session = match.group("session").upper()
        pm_rank = 1 if session == "PM" else 0
        rows.append(
            (
                as_of,
                pm_rank,
                {
                    "as_of_ist": as_of.strftime("%Y-%m-%d"),
                    "session": session,
                    "per_10g_24k": round(per_24),
                    "per_10g_22k": round(per_22),
                    "per_10g_18k": round(per_18),
                },
            )
        )
    if not rows:
        raise ValueError("no IBJA gold rows in HTML")
    rows.sort(key=lambda item: (item[0], item[1]))
    return rows[-1][2]


def board_feed_from_ibja(row: dict, fetched_at_ist: str, timestamp: int) -> dict:
    return {
        "timestamp": timestamp,
        "metal": "XAU",
        "currency": "INR",
        "as_of_ist": row["as_of_ist"],
        "fetched_at_ist": fetched_at_ist,
        "session": row["session"],
        "per_10g_24k": row["per_10g_24k"],
        "per_10g_22k": row["per_10g_22k"],
        "per_10g_18k": row["per_10g_18k"],
        "price_gram_24k": round(row["per_10g_24k"] / 10, 4),
        "price_gram_22k": round(row["per_10g_22k"] / 10, 4),
        "price_gram_18k": round(row["per_10g_18k"] / 10, 4),
        "source": "ibja",
        "disclaimer": "IBJA metal rate per 10 g; excludes 3% GST and making charges",
    }


def india_board_from_spot(spot: dict, fetched_at_ist: str) -> dict:
    g24 = float(spot["price_gram_24k"]) * (1 + INDIA_IMPORT_DUTY)
    g22 = float(spot["price_gram_22k"]) * (1 + INDIA_IMPORT_DUTY)
    g18 = float(spot["price_gram_18k"]) * (1 + INDIA_IMPORT_DUTY)
    data = dict(spot)
    data.update(
        {
            "price_gram_24k": round(g24, 4),
            "price_gram_22k": round(g22, 4),
            "price_gram_18k": round(g18, 4),
            "per_10g_24k": round(g24 * 10),
            "per_10g_22k": round(g22 * 10),
            "per_10g_18k": round(g18 * 10),
            "fetched_at_ist": fetched_at_ist,
            "as_of_ist": fetched_at_ist[:10],
            "source": "goldapi_inr_plus_import_duty",
            "disclaimer": "International spot plus 15% India import duty; not IBJA",
        }
    )
    return data


def fetch_bytes(url: str, headers: dict[str, str] | None = None) -> bytes:
    req = urllib.request.Request(url, headers=headers or UA)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    return json.loads(fetch_bytes(url, headers).decode("utf-8"))


def unwrap_feed(data: dict) -> dict:
    if data.get("encoding") == "base64" and isinstance(data.get("content"), str):
        import base64

        return json.loads(base64.b64decode(data["content"]))
    return data


def from_ibja() -> dict:
    html = fetch_bytes(IBJA_URL).decode("utf-8", errors="replace")
    row = parse_ibja_html(html)
    ist = _now_ist()
    return board_feed_from_ibja(row, ist.isoformat(), int(ist.timestamp()))


def from_goldapi_landed(key: str) -> dict:
    spot = fetch_json(
        "https://www.goldapi.io/api/XAU/INR",
        {"x-access-token": key, "Content-Type": "application/json", **UA},
    )
    return india_board_from_spot(spot, _now_ist().isoformat())


def from_public_feed() -> dict:
    try:
        return unwrap_feed(
            fetch_json(
                CONTENTS_URL,
                {
                    "User-Agent": UA["User-Agent"],
                    "Accept": "application/vnd.github.raw+json",
                },
            )
        )
    except Exception:
        return fetch_json(RAW_URL, {"User-Agent": UA["User-Agent"]})


def main() -> None:
    errors: list[str] = []
    data = None
    try:
        data = from_ibja()
    except Exception as exc:
        errors.append(f"ibja: {exc}")
        if KEY:
            try:
                data = from_goldapi_landed(KEY)
            except Exception as goldapi_exc:
                errors.append(f"goldapi: {goldapi_exc}")
        if data is None:
            data = from_public_feed()
            if str(data.get("source", "")).startswith("goldapi_inr") and not str(data.get("source")).endswith(
                "import_duty"
            ):
                data = india_board_from_spot(data, _now_ist().isoformat())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT, data.get("price_gram_22k"), data.get("as_of_ist"), data.get("source"))
    if errors:
        print("fallbacks:", "; ".join(errors))


if __name__ == "__main__":
    main()
