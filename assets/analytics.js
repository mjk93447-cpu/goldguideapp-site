/* Keep algorithms in sync with web/lib/analytics.ts */
(function () {
  var STORAGE = "goldmeet-analytics-v1";
  var EXPERIMENT = "home_cta";
  var CRAWLER =
    /googlebot|bingbot|gptbot|chatgpt-user|oai-searchbot|perplexitybot|claudebot|claude-web|applebot|bytespider|ccbot|anthropic|cohere-ai|facebookbot|slurp|duckduckbot|yandexbot|baiduspider|amazonbot|meta-externalagent|google-extended|petalbot/i;

  function fnv1a(input) {
    var h = 2166136261;
    for (var i = 0; i < input.length; i++) {
      h ^= input.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }

  function assignVariant(vid) {
    return fnv1a(EXPERIMENT + ":" + vid) % 2 === 0 ? "A" : "B";
  }

  function isCrawler() {
    return CRAWLER.test(navigator.userAgent || "");
  }

  function rid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "g" + Math.random().toString(36).slice(2) + Date.now().toString(36);
  }

  function load() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE) || "") || empty();
    } catch (e) {
      return empty();
    }
  }

  function empty() {
    return { consent: "unknown", vid: "", sessionId: "", events: [], visits: [] };
  }

  function save(s) {
    localStorage.setItem(STORAGE, JSON.stringify(s));
  }

  function path() {
    var p = location.pathname || "/";
    if (p.endsWith("/index.html") || p === "/index.html") return "/";
    return p;
  }

  function utm() {
    var q = new URLSearchParams(location.search);
    var o = {};
    if (q.get("utm_source")) o.source = q.get("utm_source");
    if (q.get("utm_medium")) o.medium = q.get("utm_medium");
    if (q.get("utm_campaign")) o.campaign = q.get("utm_campaign");
    return o;
  }

  function shouldRecord(s) {
    return s.consent === "analytics" && !isCrawler();
  }

  function track(name, meta) {
    var s = load();
    if (!shouldRecord(s)) return;
    if (!s.vid) s.vid = rid();
    if (!s.sessionId) s.sessionId = rid();
    var ev = {
      ts: Date.now(),
      name: name,
      path: path(),
      vid: s.vid,
      sessionId: s.sessionId,
      experiment: EXPERIMENT,
      variant: assignVariant(s.vid),
      referrer: document.referrer || undefined,
      utm: utm(),
      meta: meta,
    };
    s.events = (s.events || []).concat([ev]).slice(-500);
    if (name === "page_view") {
      s.visits = [{ ts: ev.ts, path: ev.path, referrer: ev.referrer || "" }].concat(s.visits || []).slice(0, 20);
    }
    save(s);
    var cfg = window.GOLDMEET || {};
    if (cfg.collectUrl && navigator.sendBeacon) {
      try {
        navigator.sendBeacon(cfg.collectUrl, new Blob([JSON.stringify({ events: [ev] })], { type: "application/json" }));
      } catch (e) {}
    }
  }

  function applyAb(s) {
    if (isCrawler()) return;
    if (s.consent !== "analytics" || !s.vid) return;
    var v = assignVariant(s.vid);
    document.querySelectorAll("[data-ab=home_cta]").forEach(function (el) {
      var copy = el.getAttribute(v === "B" ? "data-ab-b" : "data-ab-a");
      if (copy) el.textContent = copy;
    });
  }

  function banner(s) {
    if (s.consent !== "unknown" || isCrawler()) return;
    var bar = document.createElement("div");
    bar.className = "consent-bar";
    bar.innerHTML =
      "<p>GoldMeet can store a first-party cookie and this device’s visit log to measure search and join conversion. No ads. No sale of data.</p>" +
      '<div class="consent-actions"><button type="button" class="btn ghost" data-c="denied">Necessary only</button>' +
      '<button type="button" class="btn" data-c="analytics">Accept measurement</button></div>';
    document.body.appendChild(bar);
    bar.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t || !t.getAttribute) return;
      var c = t.getAttribute("data-c");
      if (!c) return;
      var next = load();
      next.consent = c;
      if (c === "analytics") {
        next.vid = next.vid || rid();
        next.sessionId = next.sessionId || rid();
      } else {
        next.events = [];
        next.visits = [];
      }
      save(next);
      bar.remove();
      if (c === "analytics") {
        applyAb(next);
        track("page_view");
      }
    });
  }

  function bind() {
    document.querySelectorAll("[data-track=cta]").forEach(function (el) {
      el.addEventListener("click", function () {
        track("cta_click");
      });
    });
    document.querySelectorAll("form[data-track=join]").forEach(function (form) {
      form.addEventListener("submit", function () {
        track("join_submit");
      });
    });
  }

  window.GoldMeetAnalytics = {
    exportJson: function () {
      return localStorage.getItem(STORAGE) || "";
    },
  };

  document.addEventListener("DOMContentLoaded", function () {
    var s = load();
    banner(s);
    applyAb(s);
    bind();
    if (shouldRecord(s)) track("page_view");
  });
})();
