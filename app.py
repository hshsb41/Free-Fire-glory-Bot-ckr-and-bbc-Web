import requests
from flask import Flask, Response, jsonify, render_template_string, request

app = Flask(__name__)

# ============================================================================
# CKRPRO AND BBC — Premium Glory Guild Dashboard (OB55 Info API)
# - Server-side proxy (no browser CORS issues)
# - Premium dark UI: depth via elevation/shadow only (no glow, no border lines)
# - 3D tilt cards, animated counters, skeleton loaders, toasts, Web Audio SFX
# ============================================================================

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>CKRPRO AND BBC | Glory Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root {
  --bg: #06060A;
  --bg-elevated: #0A0A10;
  --s1: rgba(255,255,255,0.045);
  --s2: rgba(255,255,255,0.07);
  --s3: rgba(255,255,255,0.09);
  --s-hover: rgba(255,255,255,0.11);
  --glass: rgba(18,18,24,0.55);
  --glass-2: rgba(24,24,32,0.62);
  --glass-3: rgba(30,30,40,0.7);
  --accent: #8B5CF6;
  --accent-2: #6D28D9;
  --accent-soft: rgba(139, 92, 246, 0.16);
  --gold: #F5A623;
  --gold-soft: rgba(245, 166, 35, 0.14);
  --success: #22C55E;
  --success-soft: rgba(34, 197, 94, 0.14);
  --danger: #EF4444;
  --danger-soft: rgba(239, 68, 68, 0.14);
  --text: #F4F4F6;
  --text-2: #A0A0AA;
  --text-3: #6E6E78;
  --e1: 0 2px 8px rgba(0,0,0,.35);
  --e2: 0 8px 24px rgba(0,0,0,.4);
  --e3: 0 16px 40px rgba(0,0,0,.45);
  --e-inset: inset 0 1px 0 rgba(255,255,255,.08);
  --blur: 18px;
  --blur-sm: 12px;
  --r-sm: 8px;
  --r-md: 12px;
  --r-lg: 16px;
  --ease: cubic-bezier(.4,0,.2,1);
  --spring: cubic-bezier(.34,1.56,.64,1);
}

* { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; border:none; outline:none; }
img { border:0; }
html { scroll-behavior:smooth; }
body {
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg);
  background-image:
    radial-gradient(ellipse 90% 60% at 15% -5%, rgba(139,92,246,.14), transparent 55%),
    radial-gradient(ellipse 70% 50% at 95% 5%, rgba(245,166,35,.08), transparent 50%),
    radial-gradient(ellipse 50% 40% at 50% 100%, rgba(109,40,217,.06), transparent 55%);
  background-attachment:fixed;
  color:var(--text);
  font-size:13px;
  line-height:1.45;
  min-height:100vh;
  display:flex;
  justify-content:center;
  padding-bottom:32px;
  -webkit-font-smoothing:antialiased;
  perspective:none;
}
::selection { background:var(--accent); color:#fff; }
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--s3); border-radius:8px; }


/* Glass surfaces — frosted, no hard border lines */
.glass {
  background: var(--glass);
  backdrop-filter: blur(var(--blur)) saturate(1.35);
  -webkit-backdrop-filter: blur(var(--blur)) saturate(1.35);
  box-shadow: var(--e2), var(--e-inset);
}
.glass-sm {
  background: var(--glass-2);
  backdrop-filter: blur(var(--blur-sm)) saturate(1.25);
  -webkit-backdrop-filter: blur(var(--blur-sm)) saturate(1.25);
  box-shadow: var(--e1), var(--e-inset);
}
.wrapper {
  width:100%;
  max-width:368px;
  padding:0 12px;
  display:flex;
  flex-direction:column;
  gap:9px;
}

/* Header */
.header {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:12px 0 2px;
}
.header-left { display:flex; align-items:center; gap:11px; }
.logo-wrap {
  position:relative;
  width:34px; height:34px;
  border-radius:9px;
  overflow:hidden;
  flex-shrink:0;
  background:var(--s2);
  box-shadow:var(--e1);
}
.logo-wrap img { width:100%; height:100%; object-fit:cover; display:block; }
.logo-fallback {
  width:100%; height:100%;
  align-items:center; justify-content:center;
  font-family:'Sora',sans-serif;
  font-size:14px; font-weight:800;
  color:var(--gold);
  background:var(--s3);
}
.title-group h1 {
  font-family:'Sora',sans-serif;
  font-size:15px;
  font-weight:800;
  letter-spacing:.2px;
  line-height:1.15;
  background:linear-gradient(100deg,#fff 0%,var(--gold) 28%,#fff 50%,var(--gold) 72%,#fff 100%);
  background-size:300% 100%;
  -webkit-background-clip:text;
  background-clip:text;
  color:transparent;
  animation:shimmer-title 7s linear infinite;
}
@keyframes shimmer-title {
  0% { background-position:0% 50%; }
  100% { background-position:-300% 50%; }
}
.title-group p {
  font-size:9px;
  font-weight:700;
  letter-spacing:.6px;
  text-transform:uppercase;
  color:var(--text-2);
  margin-top:2px;
}
.header-right { display:flex; align-items:center; gap:8px; }
.status-pill {
  display:flex; align-items:center; gap:5px;
  background:rgba(34,197,94,0.12);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  color:var(--success);
  font-size:9px; font-weight:800;
  letter-spacing:.4px; text-transform:uppercase;
  padding:5px 10px; border-radius:999px;
  box-shadow:var(--e1), var(--e-inset);
}
.status-dot {
  width:5px; height:5px; border-radius:50%;
  background:var(--success);
  animation:pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity:1; transform:scale(1); }
  50% { opacity:.45; transform:scale(.75); }
}
.sound-toggle {
  width:28px; height:28px; border-radius:9px;
  background:var(--glass-2);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  color:var(--text-2);
  display:flex; align-items:center; justify-content:center;
  cursor:pointer; font-size:11px;
  box-shadow:var(--e1), var(--e-inset);
  transition:background .2s var(--ease), color .2s var(--ease), transform .2s var(--spring);
}
.sound-toggle:hover { background:var(--s-hover); color:var(--text); transform:translateY(-1px); }
.sound-toggle.muted { color:var(--danger); }


/* Brand title — bold capital, small realistic, fully animated */
.brand-title {
  font-family:'Sora',system-ui,sans-serif;
  font-size:13px;
  font-weight:800;
  letter-spacing:1.15px;
  line-height:1.15;
  text-transform:uppercase;
  display:flex;
  align-items:baseline;
  flex-wrap:wrap;
}
.brand-ckr, .brand-bbc {
  background: linear-gradient(
    105deg,
    #FFFFFF 0%,
    #E8E8EC 18%,
    var(--gold) 38%,
    #FFFFFF 55%,
    var(--gold) 72%,
    #F5F5F7 100%
  );
  background-size: 280% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: brand-shine 5.5s linear infinite;
}
.brand-bbc {
  animation-delay: 0.35s;
}
.brand-x {
  color: var(--text-2);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.5px;
  padding: 0 1px;
  opacity: 0.9;
  animation: brand-x-pulse 2.8s ease-in-out infinite;
}
@keyframes brand-shine {
  0% { background-position: 0% 50%; }
  100% { background-position: -280% 50%; }
}
@keyframes brand-x-pulse {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.06); }
}
.brand-sub {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  color: var(--text-2);
  margin-top: 3px;
  animation: brand-sub-in 0.6s var(--ease) both;
}
@keyframes brand-sub-in {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Search */
.search-wrap { display:flex; flex-direction:column; gap:4px; }
.search-container {
  display:flex; align-items:center; gap:6px;
  background:var(--glass);
  backdrop-filter:blur(var(--blur)) saturate(1.3);
  -webkit-backdrop-filter:blur(var(--blur)) saturate(1.3);
  border-radius:var(--r-md);
  padding:3px 3px 3px 11px;
  box-shadow:var(--e2), var(--e-inset);
  transition:background .25s var(--ease), transform .25s var(--ease);
  transform-style:preserve-3d;
}
.search-container:focus-within {
  background:var(--glass-2);
  transform:translateY(-1px);
}
.search-container i.fa-hashtag { color:var(--text-3); font-size:11px; }
.search-container input {
  background:transparent; border:none; outline:none;
  color:var(--text); padding:9px 6px; flex:1;
  font-size:13px; font-weight:600; min-width:0;
}
.search-container input::placeholder { color:var(--text-3); font-weight:500; }
.input-error-msg {
  display:none; font-size:10px; font-weight:700;
  color:var(--danger); padding:2px 4px;
}
.input-error-msg.show { display:block; }
.btn-search {
  position:relative; overflow:hidden;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  color:#fff; border:none;
  padding:10px 16px; border-radius:9px;
  font-size:11px; font-weight:800;
  letter-spacing:.3px; text-transform:uppercase;
  cursor:pointer;
  box-shadow:var(--e1);
  transition:transform .2s var(--spring), filter .2s var(--ease);
  flex-shrink:0;
}
.btn-search:hover { filter:brightness(1.08); transform:translateY(-1px); }
.btn-search:active { transform:scale(.96); }
.btn-search .spinner-icon { display:none; }
.btn-search.loading .fa-magnifying-glass { display:none; }
.btn-search.loading .spinner-icon { display:inline-block; animation:spin .7s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }

/* Skeleton */
.skeleton-block { display:none; width:100%; flex-direction:column; gap:12px; }
.skeleton-block.show { display:flex; }
.skel {
  border-radius:var(--r-md);
  background:linear-gradient(100deg, rgba(255,255,255,.04) 30%, rgba(255,255,255,.09) 50%, rgba(255,255,255,.04) 70%);
  background-size:220% 100%;
  animation:shimmer 1.2s linear infinite;
  box-shadow:var(--e1);
  backdrop-filter:blur(8px);
}
@keyframes shimmer {
  0% { background-position:200% 0; }
  100% { background-position:-200% 0; }
}
.skel-banner { height:76px; border-radius:var(--r-lg); }
.skel-hero { height:88px; }
.skel-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.skel-card { height:70px; }

/* Banner */
.banner-card {
  background:var(--glass);
  backdrop-filter:blur(var(--blur)) saturate(1.3);
  -webkit-backdrop-filter:blur(var(--blur)) saturate(1.3);
  border-radius:var(--r-lg);
  overflow:hidden;
  width:100%; height:76px;
  display:none; align-items:center; justify-content:center;
  box-shadow:var(--e2), var(--e-inset);
  animation:riseIn .28s var(--ease);
}
.banner-card img {
  width:100%; height:100%;
  display:block; object-fit:contain; object-position:center;
}

/* Section labels */
.section-label {
  display:none;
  font-size:10px; font-weight:800;
  letter-spacing:.8px; text-transform:uppercase;
  color:var(--text-2);
  padding:4px 2px 0;
  align-items:center; gap:8px;
  animation:riseIn .26s var(--ease) both;
}
.section-label .bar {
  width:3px; height:11px;
  background:var(--gold); border-radius:2px;
}

/* Info grid — 3D cards */
.info-grid {
  display:none;
  grid-template-columns:1fr 1fr;
  gap:8px;
  width:100%;
}
.info-item {
  position:relative;
  background:var(--glass);
  backdrop-filter:blur(var(--blur-sm)) saturate(1.3);
  -webkit-backdrop-filter:blur(var(--blur-sm)) saturate(1.3);
  padding:10px 10px 9px;
  border-radius:12px;
  min-height:76px;
  display:flex; flex-direction:column; gap:5px;
  box-shadow:var(--e1), var(--e-inset);
  transition:background .18s var(--ease), transform .18s var(--spring), box-shadow .18s var(--ease);
  animation:riseIn .28s var(--ease) both;
  cursor:default;
  overflow:hidden;
}
.info-item:nth-child(1) { animation-delay:.06s; }
.info-item:nth-child(2) { animation-delay:.09s; }
.info-item:nth-child(3) { animation-delay:.12s; }
.info-item:nth-child(4) { animation-delay:.15s; }
.info-item:nth-child(5) { animation-delay:.18s; }
.info-item:nth-child(6) { animation-delay:.21s; }
.info-item:nth-child(7) { animation-delay:.24s; }
.info-item:nth-child(8) { animation-delay:.27s; }
.info-item:hover {
  background:var(--glass-2);
  transform:translateY(-2px);
  box-shadow:var(--e2);
}
.info-item .icon-badge {
  width:22px; height:22px; border-radius:7px;
  background:var(--accent-soft); color:var(--accent);
  display:flex; align-items:center; justify-content:center;
  font-size:10px; box-shadow:var(--e1);
}
.info-label {
  font-size:8px; text-transform:uppercase;
  letter-spacing:.5px; color:var(--text-2); font-weight:800;
}
.info-value {
  font-size:12px; font-weight:800; color:var(--text);
  display:flex; align-items:center; gap:5px;
  word-break:break-word; line-height:1.25;
}
.copy-btn {
  background:var(--s3); color:var(--text-2);
  border:none; width:18px; height:18px; border-radius:5px;
  font-size:9px; cursor:pointer;
  display:inline-flex; align-items:center; justify-content:center;
  transition:background .2s var(--ease), color .2s var(--ease), transform .15s var(--spring);
}
.copy-btn:hover { background:var(--accent); color:#fff; transform:scale(1.08); }

@keyframes riseIn {
  from { opacity:0; transform:translateY(14px) translateZ(-20px); }
  to { opacity:1; transform:translateY(0) translateZ(0); }
}

/* Settings / media */
.settings-panel {
  background:var(--glass);
  backdrop-filter:blur(var(--blur)) saturate(1.3);
  -webkit-backdrop-filter:blur(var(--blur)) saturate(1.3);
  border-radius:var(--r-lg);
  padding:14px;
  width:100%;
  display:none;
  flex-direction:column;
  gap:12px;
  box-shadow:var(--e2), var(--e-inset);
  animation:riseIn .28s var(--ease) .05s both;
}
.media-card { display:flex; flex-direction:column; gap:8px; }
.media-frame {
  width:100%; border-radius:var(--r-md); overflow:hidden;
  background:var(--s2); box-shadow:var(--e1);
}
.media-frame img { width:100%; display:block; object-fit:cover; }
.wide-frame { max-height:160px; }
.wide-frame img { max-height:160px; object-fit:cover; }
.qr-frame { max-width:180px; margin:0 auto; border-radius:12px; }
.qr-frame img { width:100%; }
.media-caption {
  font-size:10px; font-weight:700; color:var(--text-2);
  text-align:center; letter-spacing:.3px;
  display:flex; align-items:center; justify-content:center; gap:6px;
}

/* Pricing */
.price-section {
  background:var(--glass);
  backdrop-filter:blur(var(--blur)) saturate(1.35);
  -webkit-backdrop-filter:blur(var(--blur)) saturate(1.35);
  border-radius:var(--r-lg);
  padding:18px 16px;
  text-align:center;
  width:100%;
  display:flex; flex-direction:column; align-items:center; gap:8px;
  box-shadow:var(--e2), var(--e-inset);
  transition:transform .2s var(--ease);
}
.price-section:hover { transform:translateY(-2px) translateZ(8px); }
.badge {
  background:var(--gold-soft); color:var(--gold);
  padding:4px 10px; border-radius:6px;
  font-size:9px; font-weight:800;
  letter-spacing:.5px; text-transform:uppercase;
}
.price-sub { color:var(--text-2); font-size:11px; font-weight:700; }
.price-amount {
  font-family:'Sora',sans-serif;
  font-size:24px; font-weight:800; color:var(--text);
  line-height:1; margin:2px 0;
}
.price-amount sup {
  font-size:13px; color:var(--text-2); font-weight:700; margin-left:3px;
}
.btn-buy {
  position:relative; overflow:hidden;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  color:#fff; text-decoration:none;
  width:100%; padding:13px; border-radius:11px;
  font-weight:800; font-size:12px; letter-spacing:.3px;
  text-align:center;
  box-shadow:var(--e2);
  transition:transform .2s var(--spring), filter .2s var(--ease);
  margin-top:4px;
  display:flex; align-items:center; justify-content:center; gap:7px;
}
.btn-buy:hover { filter:brightness(1.1); transform:translateY(-2px); }
.btn-buy:active { transform:translateY(0) scale(.98); }

.ripple {
  position:absolute; border-radius:50%;
  background:rgba(255,255,255,.3);
  transform:scale(0);
  animation:ripple-anim .55s var(--ease);
  pointer-events:none;
}
@keyframes ripple-anim {
  to { transform:scale(2.6); opacity:0; }
}

/* Toast */
.toast-stack {
  position:fixed; top:18px; left:50%;
  transform:translateX(-50%);
  display:flex; flex-direction:column; gap:10px;
  z-index:999; width:92%; max-width:420px;
  pointer-events:none;
}
.toast {
  display:flex; align-items:center; gap:9px;
  background:var(--glass-3); color:var(--text);
  backdrop-filter:blur(16px) saturate(1.3);
  -webkit-backdrop-filter:blur(16px) saturate(1.3);
  padding:11px 14px; border-radius:11px;
  font-size:12px; font-weight:700;
  box-shadow:var(--e3);
  opacity:0; transform:translateY(-14px);
  transition:opacity .25s var(--ease), transform .25s var(--ease);
}
.toast.visible { opacity:1; transform:translateY(0); }
.toast .toast-icon {
  width:22px; height:22px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:11px; flex-shrink:0;
}
.toast.success .toast-icon { background:var(--success-soft); color:var(--success); }
.toast.error .toast-icon { background:var(--danger-soft); color:var(--danger); }
.toast.info .toast-icon { background:var(--accent-soft); color:var(--accent); }

footer {
  margin-top:20px; text-align:center;
  font-size:9px; font-weight:700;
  color:var(--text-3); letter-spacing:1.2px; text-transform:uppercase;
}
footer span { color:var(--gold); }

@media (max-width:340px) {
  .info-grid, .skel-grid { grid-template-columns:1fr; }
}
</style>
</head>
<body>
<div class="toast-stack" id="toastStack"></div>

<div class="wrapper">
  <div class="header">
    <div class="header-left">
      <div class="title-group">
        <h1 class="brand-title"><span class="brand-ckr">CKRPRO</span><span class="brand-x"> X </span><span class="brand-bbc">BBC</span></h1>
        <p class="brand-sub">FREE FIRE GLORY</p>
      </div>
    </div>
    <div class="header-right">
      <div class="sound-toggle" id="soundToggle" title="Sound"><i class="fas fa-volume-high"></i></div>
    </div>
  </div>

  <div class="search-wrap">
    <div class="search-container" id="searchContainer">
      <i class="fas fa-hashtag"></i>
      <input type="text" id="uidInput" placeholder="Enter Free Fire UID" inputmode="numeric" autocomplete="off">
      <button class="btn-search" id="searchBtn" onclick="fetchData(event)">
        <i class="fas fa-magnifying-glass"></i>
        <i class="fas fa-spinner spinner-icon"></i>
      </button>
    </div>
    <div class="input-error-msg" id="inputError">Enter a valid numeric UID (6+ digits)</div>
  </div>

  <div class="skeleton-block" id="skeletonBlock">
    <div class="skel skel-banner"></div>
    <div class="skel skel-hero"></div>
    <div class="skel-grid">
      <div class="skel skel-card"></div>
      <div class="skel skel-card"></div>
      <div class="skel skel-card"></div>
      <div class="skel skel-card"></div>
    </div>
  </div>

  <div class="banner-card" id="bannerCard">
    <img id="playerBanner" alt="Player banner">
  </div>

  <div class="section-label" id="labelGuild"><span class="bar"></span> Guild Information</div>
  <div class="info-grid" id="guildGrid">
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-id-card"></i></div>
      <span class="info-label">Guild Name</span>
      <span class="info-value" id="g_name">—</span>
    </div>
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-fingerprint"></i></div>
      <span class="info-label">Guild ID</span>
      <span class="info-value">
        <span id="g_id">—</span>
        <button class="copy-btn" onclick="copyText(event, 'g_id')" title="Copy"><i class="fas fa-copy"></i></button>
      </span>
    </div>
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-layer-group"></i></div>
      <span class="info-label">Guild Level</span>
      <span class="info-value" id="g_level">—</span>
    </div>
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-users"></i></div>
      <span class="info-label">Members</span>
      <span class="info-value" id="g_members">—</span>
    </div>
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-chart-pie"></i></div>
      <span class="info-label">Capacity</span>
      <span class="info-value" id="g_capacity">—</span>
    </div>
    <div class="info-item">
      <div class="icon-badge"><i class="fas fa-user-shield"></i></div>
      <span class="info-label">Leader</span>
      <span class="info-value" id="g_owner">—</span>
    </div>
  </div>

  <div class="empty-state" id="emptyState" style="display:none;flex-direction:column;align-items:center;gap:10px;padding:28px 16px;background:var(--glass);backdrop-filter:blur(var(--blur));border-radius:var(--r-lg);box-shadow:var(--e2);text-align:center;">
    <i class="fas fa-users-slash" style="font-size:22px;color:var(--text-3);"></i>
    <p style="font-size:12px;font-weight:600;color:var(--text-2);">No guild found for this UID.</p>
  </div>

  <div class="settings-panel" id="settingsPanel">
    <div class="media-card">
      <div class="media-frame wide-frame">
        <img src="https://i.ibb.co/SGDr3Sc/IMG-20260327-234910-055.jpg" alt="">
      </div>
      <div class="media-caption"><i class=""></i> </div>
    </div>
  </div>

  <div class="price-section">
    <span class="badge">Limited Offer</span>
    <p class="price-sub">PER SQUAD PRICE</p>
    <div class="price-amount">380<sup>NPR</sup></div>
    <div class="media-card">
      <div class="media-frame qr-frame">
        <img src="https://i.ibb.co/xtkSDp54/qr.jpg" alt="Payment QR">
      </div>
      <div class="media-caption"><i class="fas fa-qrcode"></i> Payment</div>
    </div>
    <a href="https://wa.me/9779840825493?text=I%20want%20to%20buy%20glory%20bot" class="btn-buy" id="buyBtn">
      <i class="fab fa-whatsapp"></i> BUY NOW
    </a>
  </div>

  <footer> <span></span> </footer>
</div>

<script>
const SoundEngine = (() => {
  let ctx = null, muted = false;
  function ensure() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function tone({ freq=440, duration=0.1, type='sine', gain=0.14, glideTo=null }) {
    if (muted) return;
    try {
      const a = ensure();
      const o = a.createOscillator(), g = a.createGain();
      o.type = type;
      o.frequency.setValueAtTime(freq, a.currentTime);
      if (glideTo) o.frequency.exponentialRampToValueAtTime(Math.max(glideTo, 40), a.currentTime + duration);
      g.gain.setValueAtTime(gain, a.currentTime);
      g.gain.exponentialRampToValueAtTime(0.0001, a.currentTime + duration);
      o.connect(g); g.connect(a.destination);
      o.start(); o.stop(a.currentTime + duration + 0.03);
    } catch (_) {}
  }
  function blip(f1, f2, d=0.08) {
    tone({ freq:f1, duration:d, type:'triangle', gain:0.16 });
    if (f2) setTimeout(() => tone({ freq:f2, duration:d*1.1, type:'sine', gain:0.12 }), 55);
  }
  return {
    click: () => blip(620, 880, 0.07),
    success: () => { tone({ freq:523, duration:0.1, type:'sine', gain:0.15 }); setTimeout(() => tone({ freq:784, duration:0.16, type:'sine', gain:0.14 }), 80); setTimeout(() => tone({ freq:1046, duration:0.12, type:'triangle', gain:0.1 }), 160); },
    error: () => tone({ freq:200, duration:0.28, type:'sawtooth', gain:0.12, glideTo:90 }),
    hover: () => tone({ freq:480, duration:0.04, type:'sine', gain:0.06 }),
    setMuted(v) { muted = v; },
    isMuted() { return muted; },
  };
})();

function showToast(message, kind='info', duration=3200) {
  const stack = document.getElementById('toastStack');
  const toast = document.createElement('div');
  toast.className = `toast ${kind}`;
  const icons = { success:'fa-circle-check', error:'fa-circle-exclamation', info:'fa-circle-info' };
  toast.innerHTML = `<span class="toast-icon"><i class="fas ${icons[kind]||icons.info}"></i></span><span>${message}</span>`;
  stack.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('visible'));
  setTimeout(() => { toast.classList.remove('visible'); setTimeout(() => toast.remove(), 260); }, duration);
}

function attachRipple(el) {
  el.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const ripple = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    ripple.className = 'ripple';
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size/2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size/2) + 'px';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
}
document.querySelectorAll('.btn-search, .btn-buy').forEach(attachRipple);

function animateCount(el, targetValue, { prefix='', suffix='', duration=420 } = {}) {
  const numeric = parseInt(String(targetValue).replace(/[^\d]/g, ''), 10);
  if (Number.isNaN(numeric)) { el.innerText = targetValue; return; }
  const start = performance.now();
  function frame(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.innerText = prefix + Math.round(numeric * eased).toLocaleString() + suffix;
    if (p < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

const uidInput = document.getElementById('uidInput');
const inputError = document.getElementById('inputError');
uidInput.addEventListener('input', () => {
  uidInput.value = uidInput.value.replace(/[^\d]/g, '');
  if (inputError.classList.contains('show')) validateUid(false);
});
uidInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') fetchData(e); });

function validateUid(show=true) {
  const valid = /^\d{6,}$/.test(uidInput.value.trim());
  if (!valid && show) { inputError.classList.add('show'); SoundEngine.error(); }
  else inputError.classList.remove('show');
  return valid;
}

function setText(id, val, fallback='—') {
  const el = document.getElementById(id);
  if (el) el.innerText = (val === 0 || val) ? String(val) : fallback;
}

async function fetchData(e) {
  if (e) e.preventDefault();
  SoundEngine.click();
  if (!validateUid(true)) return;
  const uid = uidInput.value.trim();

  const searchBtn = document.getElementById('searchBtn');
  const skeleton = document.getElementById('skeletonBlock');
  const bannerCard = document.getElementById('bannerCard');
  const bannerImg = document.getElementById('playerBanner');
  const guildGrid = document.getElementById('guildGrid');
  const settings = document.getElementById('settingsPanel');
  const labelG = document.getElementById('labelGuild');

  searchBtn.classList.add('loading');
  searchBtn.disabled = true;
  skeleton.classList.add('show');
  ['bannerCard', 'guildGrid', 'settingsPanel', 'labelGuild', 'emptyState'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });

  bannerImg.onerror = () => { bannerCard.style.display = 'none'; };
  bannerImg.onload = () => { bannerCard.style.display = 'flex'; };
  bannerImg.src = `/api/banner?uid=${encodeURIComponent(uid)}`;

  try {
    const response = await fetch(`/api/player-info?uid=${encodeURIComponent(uid)}`, {
      headers: { Accept: 'application/json' },
    });
    let payload;
    try { payload = await response.json(); }
    catch (_) { throw new Error('Server returned an unreadable response.'); }

    if (!response.ok || !payload.success) {
      throw new Error(payload.error || `Request failed (${response.status}).`);
    }

    const d = payload.data || {};
    const g = d.GuildInformation || {};
    const guildName = g.GuildName;
    const guildId = g.GuildID;

    if (!guildName && !guildId) {
      const empty = document.getElementById('emptyState');
      if (empty) empty.style.display = 'flex';
      showToast('No guild found for this UID.', 'info');
      SoundEngine.error();
      return;
    }

    setText('g_name', guildName);
    setText('g_id', guildId);
    animateCount(document.getElementById('g_level'), g.GuildLevel || 0, { prefix: 'Lv ' });
    const mem = g.LiveMembers;
    const max = g.MaxMembers;
    if (mem != null && max != null) {
      document.getElementById('g_members').innerText = mem + ' / ' + max;
      const cap = document.getElementById('g_capacity');
      if (cap) animateCount(cap, max);
    } else {
      animateCount(document.getElementById('g_members'), mem || 0);
      setText('g_capacity', max);
    }
    setText('g_owner', g.LeaderName || '—');

    labelG.style.display = 'flex';
    guildGrid.style.display = 'grid';
    settings.style.display = 'flex';

    showToast('Guild data loaded.', 'success');
    SoundEngine.success();
  } catch (err) {
    console.error(err);
    const isNet = err instanceof TypeError;
    showToast(isNet ? 'Cannot reach server. Check connection.' : (err.message || 'Something went wrong.'), 'error', 4200);
    SoundEngine.error();
  } finally {
    skeleton.classList.remove('show');
    searchBtn.classList.remove('loading');
    searchBtn.disabled = false;
  }
}

async function copyText(e, id) {
  e.stopPropagation();
  SoundEngine.click();
  const value = document.getElementById(id).innerText.trim();
  if (!value || value === '—') { showToast('Nothing to copy.', 'error'); return; }
  try {
    await navigator.clipboard.writeText(value);
    showToast('Copied to clipboard.', 'success');
  } catch (_) {
    showToast('Copy failed — select manually.', 'error');
  }
}

document.getElementById('soundToggle').addEventListener('click', () => {
  const m = !SoundEngine.isMuted();
  SoundEngine.setMuted(m);
  const btn = document.getElementById('soundToggle');
  btn.classList.toggle('muted', m);
  btn.innerHTML = `<i class="fas ${m ? 'fa-volume-xmark' : 'fa-volume-high'}"></i>`;
  if (!m) SoundEngine.click();
});

document.getElementById('buyBtn').addEventListener('click', () => SoundEngine.success());

document.addEventListener('click', (e) => {
  const t = e.target.closest('button, .btn-search, .btn-buy, .copy-btn, .sound-toggle, .status-pill, a.btn-buy');
  if (t) { try { SoundEngine.click(); } catch(_){} }
}, true);

</script>
</body>
</html>
"""

PLAYER_INFO_API = "https://ob55-info-by-ckrpro.vercel.app/info"
BANNER_API = "https://ff-banner-api-one.vercel.app/profile"
UPSTREAM_TIMEOUT = 12


def _valid_uid(uid: str) -> bool:
    return uid.isdigit() and len(uid) >= 6


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/player-info")
def api_player_info():
    uid = request.args.get("uid", "").strip()
    if not _valid_uid(uid):
        return jsonify(success=False, error="Please enter a valid numeric UID (6+ digits)."), 400

    try:
        upstream = requests.get(PLAYER_INFO_API, params={"uid": uid}, timeout=UPSTREAM_TIMEOUT)
    except requests.exceptions.Timeout:
        return jsonify(success=False, error="Player info service timed out. Try again."), 504
    except requests.exceptions.ConnectionError:
        return jsonify(success=False, error="Unable to reach the player info service."), 502
    except requests.exceptions.RequestException as exc:
        return jsonify(success=False, error=f"Network error: {exc}"), 502

    if upstream.status_code == 404:
        return jsonify(success=False, error="No player found for this UID."), 404
    if upstream.status_code != 200:
        return jsonify(
            success=False,
            error=f"Player info service returned status {upstream.status_code}.",
        ), 502

    try:
        data = upstream.json()
    except ValueError:
        return jsonify(success=False, error="Player info service returned unreadable data."), 502

    if not data or data.get("status") != "success":
        return jsonify(success=False, error="No data found for this UID."), 404

    return jsonify(success=True, data=data)


@app.route("/api/banner")
def api_banner():
    uid = request.args.get("uid", "").strip()
    if not _valid_uid(uid):
        return Response("Invalid UID.", status=400)

    try:
        upstream = requests.get(BANNER_API, params={"uid": uid}, timeout=UPSTREAM_TIMEOUT, stream=True)
    except requests.exceptions.Timeout:
        return Response("Banner service timed out.", status=504)
    except requests.exceptions.RequestException as exc:
        return Response(f"Banner unreachable: {exc}", status=502)

    if upstream.status_code != 200:
        return Response("Banner not available.", status=upstream.status_code)

    content_type = upstream.headers.get("Content-Type", "image/png")
    return Response(upstream.content, content_type=content_type)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
