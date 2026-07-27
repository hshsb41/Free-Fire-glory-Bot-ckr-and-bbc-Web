import requests
from flask import Flask, Response, jsonify, render_template_string, request

app = Flask(__name__)

# ============================================================================
# CKRPRO AND BBC — Premium Glory Guild Dashboard
# ----------------------------------------------------------------------------
# Full single-file Flask app: premium dark UI, no glow/no border-line design
# (depth via layered elevation + shadow only), bold micro-typography, fully
# functional dropdowns, toast notifications instead of alert(), ripple click
# feedback, synthesized UI sound effects (Web Audio API — no external audio
# files needed), animated counters, clipboard copy, and input validation.
#
# v4 fix: the "Something went wrong" / no-response bug was the browser
# calling the third-party player-info API directly with fetch(). If that
# API doesn't send CORS headers for this app's origin, the browser silently
# blocks the request and the JS only ever sees a generic network error —
# no matter how good the frontend error handling is. The real fix is a
# server-side proxy: the Flask backend calls the third-party API itself
# (server-to-server requests are never subject to browser CORS), and the
# frontend only ever talks to this same-origin Flask app. See /api/player-info
# and /api/banner below.
# ============================================================================

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>CKRPRO AND BBC | Glory Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
/* ==========================================================================
   1. DESIGN TOKENS
   ========================================================================== */
:root {
    /* Surfaces — depth is created with these steps, never with borders */
    --bg:            #08080A;
    --bg-elevated:   #0E0E11;
    --surface-1:     #131316;
    --surface-2:     #191A1E;
    --surface-3:     #202126;
    --surface-hover: #26272D;

    /* Brand */
    --accent:        #8B5CF6;
    --accent-2:      #6D28D9;
    --accent-soft:   rgba(139, 92, 246, 0.14);
    --gold:          #F5A623;
    --gold-soft:     rgba(245, 166, 35, 0.14);

    /* Status */
    --success:       #22C55E;
    --success-soft:  rgba(34, 197, 94, 0.14);
    --danger:        #EF4444;
    --danger-soft:   rgba(239, 68, 68, 0.14);

    /* Typography */
    --text-primary:   #F5F5F7;
    --text-secondary: #9B9BA5;
    --text-tertiary:  #6B6B75;

    /* Elevation (neutral shadows only — no colored glow, no border rules) */
    --elev-1: 0 1px 2px rgba(0, 0, 0, 0.5);
    --elev-2: 0 4px 12px rgba(0, 0, 0, 0.45);
    --elev-3: 0 10px 30px rgba(0, 0, 0, 0.5);

    --radius-sm: 8px;
    --radius-md: 11px;
    --radius-lg: 15px;

    --ease: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ==========================================================================
   2. RESET
   ========================================================================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html { scroll-behavior: smooth; }

body {
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    background-image:
        radial-gradient(circle at 15% 0%, rgba(139, 92, 246, 0.08), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(245, 166, 35, 0.05), transparent 40%);
    background-attachment: fixed;
    color: var(--text-primary);
    font-size: 13px;
    line-height: 1.45;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding-bottom: 40px;
    -webkit-font-smoothing: antialiased;
}

::selection { background: var(--accent); color: white; }

/* Slim custom scrollbar — no border, just contrast */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: var(--surface-hover); }

/* ==========================================================================
   3. LAYOUT
   ========================================================================== */
.wrapper {
    width: 100%;
    max-width: 400px;
    padding: 0 14px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* ==========================================================================
   4. HEADER
   ========================================================================== */
.header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 0 4px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-wrap {
    position: relative;
    width: 34px;
    height: 34px;
    border-radius: 9px;
    overflow: hidden;
    flex-shrink: 0;
    background: var(--surface-2);
}

.logo-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.title-group h1 {
    font-family: 'Sora', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.2px;
    line-height: 1.15;
    background: linear-gradient(
        100deg,
        #FFFFFF 0%,
        var(--gold) 25%,
        #FFFFFF 50%,
        var(--gold) 75%,
        #FFFFFF 100%
    );
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: title-shimmer 6s linear infinite;
}

@keyframes title-shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: -300% 50%; }
}

.title-group p {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 2px;
}

.status-pill {
    display: flex;
    align-items: center;
    gap: 5px;
    background: var(--success-soft);
    color: var(--success);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    padding: 5px 9px;
    border-radius: 999px;
}

.status-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ==========================================================================
   5. SEARCH BAR
   ========================================================================== */
.search-container {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--surface-1);
    border-radius: var(--radius-md);
    padding: 4px 4px 4px 13px;
    width: 100%;
    box-shadow: var(--elev-1);
    transition: background 0.25s var(--ease);
}

.search-container:focus-within {
    background: var(--surface-2);
}

.search-container i.fa-hashtag {
    color: var(--text-tertiary);
    font-size: 11px;
}

.search-container input {
    background: transparent;
    border: none;
    outline: none;
    color: var(--text-primary);
    padding: 8px 6px;
    flex: 1;
    font-size: 13px;
    font-weight: 600;
    min-width: 0;
}

.search-container input::placeholder {
    color: var(--text-tertiary);
    font-weight: 500;
}

.input-error-msg {
    display: none;
    font-size: 10px;
    font-weight: 700;
    color: var(--danger);
    padding: 2px 4px;
}

.input-error-msg.show { display: block; }

.btn-search {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    color: white;
    border: none;
    padding: 9px 16px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    cursor: pointer;
    transition: transform 0.2s var(--ease), filter 0.2s var(--ease);
    flex-shrink: 0;
}

.btn-search:hover { filter: brightness(1.1); }
.btn-search:active { transform: scale(0.96); }

.btn-search .spinner-icon { display: none; }
.btn-search.loading .fa-magnifying-glass { display: none; }
.btn-search.loading .spinner-icon { display: inline-block; }

/* ==========================================================================
   6. SKELETON LOADER (replaces the old spinner-only loader)
   ========================================================================== */
.skeleton-block {
    display: none;
    width: 100%;
    flex-direction: column;
    gap: 12px;
}

.skeleton-block.show { display: flex; }

.skeleton-banner {
    width: 100%;
    height: 92px;
    border-radius: var(--radius-lg);
    background: linear-gradient(100deg, var(--surface-1) 30%, var(--surface-3) 50%, var(--surface-1) 70%);
    background-size: 220% 100%;
    animation: shimmer 1.4s linear infinite;
}

.skeleton-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

.skeleton-card {
    height: 56px;
    border-radius: var(--radius-md);
    background: linear-gradient(100deg, var(--surface-1) 30%, var(--surface-3) 50%, var(--surface-1) 70%);
    background-size: 220% 100%;
    animation: shimmer 1.4s linear infinite;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* ==========================================================================
   7. BANNER CARD
   ========================================================================== */
.banner-card {
    background: var(--surface-1);
    border-radius: var(--radius-lg);
    overflow: hidden;
    width: 100%;
    height: 92px;
    display: none;
    align-items: center;
    justify-content: center;
    box-shadow: var(--elev-2);
    animation: fadeSlideIn 0.45s var(--ease);
}

.banner-card img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: contain;
    object-position: center;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ==========================================================================
   8. STAT / INFO GRID
   ========================================================================== */
.info-grid {
    display: none;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    width: 100%;
}

.info-item {
    position: relative;
    background: var(--surface-1);
    padding: 12px 12px 10px;
    border-radius: var(--radius-md);
    display: flex;
    flex-direction: column;
    gap: 6px;
    box-shadow: var(--elev-1);
    transition: background 0.2s var(--ease), transform 0.2s var(--ease);
    cursor: default;
}

.info-item:hover {
    background: var(--surface-2);
    transform: translateY(-2px);
}

.info-item .icon-badge {
    width: 24px;
    height: 24px;
    border-radius: 7px;
    background: var(--accent-soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
}

.info-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    font-weight: 800;
}

.info-value {
    font-size: 13px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 6px;
}

.copy-btn {
    background: var(--surface-3);
    color: var(--text-secondary);
    border: none;
    width: 18px;
    height: 18px;
    border-radius: 5px;
    font-size: 9px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s var(--ease), color 0.2s var(--ease);
}

.copy-btn:hover { background: var(--accent); color: white; }

/* ==========================================================================
   9. SETTINGS PANEL
   ========================================================================== */
.settings-panel {
    background: var(--surface-1);
    border-radius: var(--radius-lg);
    padding: 14px;
    width: 100%;
    display: none;
    flex-direction: column;
    gap: 14px;
    box-shadow: var(--elev-2);
}

.settings-header {
    font-size: 10px;
    font-weight: 800;
    color: var(--text-secondary);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 11px;
    position: relative;
}

/* Separator via a subtle background line instead of a hard border-bottom */
.settings-header::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 1px;
    background: var(--surface-3);
}

.settings-header .accent-bar {
    width: 3px;
    height: 11px;
    background: var(--gold);
    border-radius: 2px;
    flex-shrink: 0;
}

.setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
}

.setting-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
}

/* Segmented OFF / ON toggle — flat, no border ring */
.toggle {
    display: flex;
    background: var(--surface-3);
    border-radius: 8px;
    overflow: hidden;
    width: 120px;
    flex-shrink: 0;
}

.toggle-option {
    flex: 1;
    text-align: center;
    padding: 7px 0;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.4px;
    color: var(--text-secondary);
    background: transparent;
    cursor: pointer;
    transition: background 0.25s var(--ease), color 0.25s var(--ease);
    user-select: none;
}

.toggle-option.selected.off { background: var(--surface-hover); color: var(--text-primary); }
.toggle-option.selected.on  { background: var(--success); color: #06210F; }

.toggle-option:not(.selected):hover { color: var(--text-primary); }

/* Custom functional dropdown */
.dropdown {
    position: relative;
    flex-shrink: 0;
}

.dropdown-trigger {
    background: var(--surface-3);
    padding: 7px 10px;
    border-radius: 8px;
    min-width: 96px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    cursor: pointer;
    transition: background 0.2s var(--ease);
}

.dropdown-trigger:hover { background: var(--surface-hover); }
.dropdown-trigger i { font-size: 9px; transition: transform 0.25s var(--ease); }
.dropdown.open .dropdown-trigger i { transform: rotate(180deg); }
.dropdown.open .dropdown-trigger { color: var(--text-primary); }

.dropdown-menu {
    position: absolute;
    top: calc(100% + 5px);
    right: 0;
    min-width: 118px;
    background: var(--surface-2);
    border-radius: 9px;
    box-shadow: var(--elev-3);
    padding: 5px;
    display: none;
    flex-direction: column;
    gap: 2px;
    z-index: 20;
}

.dropdown.open .dropdown-menu {
    display: flex;
    animation: dropIn 0.16s var(--ease);
}

@keyframes dropIn {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.dropdown-menu-item {
    padding: 7px 9px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    cursor: pointer;
    transition: background 0.15s var(--ease), color 0.15s var(--ease);
}

.dropdown-menu-item:hover { background: var(--surface-hover); color: var(--text-primary); }
.dropdown-menu-item.active { background: var(--accent-soft); color: var(--accent); }

/* ==========================================================================
   10. PRICING SECTION
   ========================================================================== */
.price-section {
    background: var(--surface-1);
    border-radius: var(--radius-lg);
    padding: 18px 16px;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 7px;
    box-shadow: var(--elev-2);
}

.badge {
    background: var(--gold-soft);
    color: var(--gold);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.price-sub {
    color: var(--text-secondary);
    font-size: 11px;
    font-weight: 700;
}

.price-amount {
    font-family: 'Sora', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
    margin: 2px 0;
}

.price-amount sup {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 700;
    margin-left: 3px;
}

.btn-buy {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    color: white;
    text-decoration: none;
    width: 100%;
    padding: 13px;
    border-radius: 10px;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 0.3px;
    text-align: center;
    transition: transform 0.2s var(--ease-spring), filter 0.2s var(--ease);
    margin-top: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
}

.btn-buy:hover { filter: brightness(1.12); transform: translateY(-2px); }
.btn-buy:active { transform: translateY(0) scale(0.98); }

/* Ripple feedback — a plain expanding circle, not a colored glow */
.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.35);
    transform: scale(0);
    animation: ripple-anim 0.55s var(--ease);
    pointer-events: none;
}

@keyframes ripple-anim {
    to { transform: scale(2.6); opacity: 0; }
}

/* ==========================================================================
   11. TOAST NOTIFICATIONS (replaces alert())
   ========================================================================== */
.toast-stack {
    position: fixed;
    top: 18px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 999;
    width: 92%;
    max-width: 420px;
    pointer-events: none;
}

.toast {
    display: flex;
    align-items: center;
    gap: 9px;
    background: var(--surface-2);
    color: var(--text-primary);
    padding: 11px 14px;
    border-radius: 11px;
    font-size: 12px;
    font-weight: 700;
    box-shadow: var(--elev-3);
    opacity: 0;
    transform: translateY(-14px);
    transition: opacity 0.25s var(--ease), transform 0.25s var(--ease);
}

.toast.visible { opacity: 1; transform: translateY(0); }

.toast .toast-icon {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    flex-shrink: 0;
}

.toast.success .toast-icon { background: var(--success-soft); color: var(--success); }
.toast.error .toast-icon { background: var(--danger-soft); color: var(--danger); }
.toast.info .toast-icon { background: var(--accent-soft); color: var(--accent); }

/* ==========================================================================
   12. FOOTER
   ========================================================================== */
footer {
    margin-top: 24px;
    text-align: center;
    font-size: 9px;
    font-weight: 700;
    color: var(--text-tertiary);
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

footer span { color: var(--gold); }

/* ==========================================================================
   13. SOUND TOGGLE (small mute control in header)
   ========================================================================== */
.sound-toggle {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: var(--surface-2);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 11px;
    transition: background 0.2s var(--ease), color 0.2s var(--ease);
    flex-shrink: 0;
}

.sound-toggle:hover { background: var(--surface-hover); color: var(--text-primary); }
.sound-toggle.muted { color: var(--danger); }

.header-right { display: flex; align-items: center; gap: 8px; }

/* ==========================================================================
   14. RESPONSIVE
   ========================================================================== */
@media (max-width: 480px) {
    .info-grid, .skeleton-grid { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 340px) {
    .info-grid, .skeleton-grid { grid-template-columns: 1fr; }
    .toggle { width: 108px; }
    .dropdown-trigger { min-width: 84px; }
}

/* ==========================================================================
   15. MEDIA CARDS — framed + captioned images (Payment QR / instructions)
   ========================================================================== */
.media-card {
    background: var(--surface-1);
    border-radius: var(--radius-lg);
    padding: 12px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-shadow: var(--elev-2);
}

.media-frame {
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 2px solid var(--surface-3);
    background: var(--surface-2);
    display: flex;
    align-items: center;
    justify-content: center;
}

.media-frame img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
}

/* Payment QR — compact, square, centered (not full width) */
.media-frame.qr-frame {
    width: 148px;
    height: 148px;
}

/* Instructional / step image — wider, portrait-friendly, capped height */
.media-frame.wide-frame {
    width: 100%;
    height: 200px;
}

.media-caption {
    width: 100%;
    text-align: center;
    padding-top: 9px;
    border-top: 1px solid var(--surface-3);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.media-caption i { color: var(--gold); font-size: 10px; }
</style>
</head>
<body>

<div class="toast-stack" id="toastStack"></div>

<div class="wrapper">

    <!-- Header -->
    <div class="header">
        <div class="header-left">
            <div class="logo-wrap">
                <img src="https://i.ibb.co/Y4KjTgvP/Picsart-26-02-07-02-21-57-621.jpg" alt="Logo">
            </div>
            <div class="title-group">
                <h1>CKR AND BBC</h1>
                <p>FREE FIRE GLORY</p>
            </div>
        </div>
        <div class="header-right">
            <div class="status-pill"><span class="status-dot"></span>Online</div>
            <div class="sound-toggle" id="soundToggle" title="Toggle sound">
                <i class="fas fa-volume-high"></i>
            </div>
        </div>
    </div>

    <!-- Search -->
    <div>
        <div class="search-container" id="searchContainer">
            <i class="fas fa-hashtag"></i>
            <input type="text" id="uidInput" placeholder="ENTER FREE FIRE UID" inputmode="numeric" autocomplete="off">
            <button class="btn-search" id="searchBtn" onclick="fetchData(event)">
                <i class="fas fa-magnifying-glass"></i>
                <i class="fas fa-circle-notch fa-spin spinner-icon"></i>
                <span class="btn-search-label">Search</span>
            </button>
        </div>
        <div class="input-error-msg" id="inputError">Please enter a valid numeric UID (6+ digits).</div>
    </div>

    <!-- Skeleton loader -->
    <div class="skeleton-block" id="skeletonBlock">
        <div class="skeleton-banner"></div>
        <div class="skeleton-grid">
            <div class="skeleton-card"></div>
            <div class="skeleton-card"></div>
            <div class="skeleton-card"></div>
            <div class="skeleton-card"></div>
        </div>
    </div>

    <!-- Banner -->
    <div class="banner-card" id="bannerCard">
        <img id="playerBanner" src="" alt="Player Banner">
    </div>

    <!-- Info grid -->
    <div class="info-grid" id="infoGrid">
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
                <button class="copy-btn" onclick="copyGuildId(event)" title="Copy Guild ID">
                    <i class="fas fa-copy"></i>
                </button>
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
            <span class="info-label">Guild Owner</span>
            <span class="info-value" id="g_owner">—</span>
        </div>
    </div>

    <!-- Settings panel (now shows a step image instead of approval settings) -->
    <div class="settings-panel" id="settingsPanel">
        <div class="media-card">
            <div class="media-frame wide-frame">
                <img src="https://i.ibb.co/SGDr3Sc/IMG-20260327-234910-055.jpg" alt="Click Buy Now">
            </div>
            <div class="media-caption"><i class="fas fa-hand-pointer"></i>Click Buy Now</div>
        </div>
    </div>

    <!-- Pricing -->
    <div class="price-section">
        <span class="badge">Limited Offer</span>
        <p class="price-sub">PER SQUAD PRICE</p>
        <div class="price-amount">380<sup>NPR</sup></div>

        <!-- Payment QR — sits directly above the Buy Now button -->
        <div class="media-card">
            <div class="media-frame qr-frame">
                <img src="https://i.ibb.co/xtkSDp54/qr.jpg" alt="Payment QR">
            </div>
            <div class="media-caption"><i class="fas fa-qrcode"></i>Payment</div>
        </div>

        <a href="https://wa.me/9779840825493?text=I%20want%20to%20buy%20glory%20bot" class="btn-buy" id="buyBtn">
            <i class="fab fa-whatsapp"></i> BUY NOW
        </a>
    </div>

    <footer><span></span></footer>
</div>

<script>
/* ============================================================================
   1. SOUND ENGINE — synthesized UI feedback via Web Audio API.
      No external audio files required; a single shared AudioContext is
      lazily created/resumed on the user's first interaction (required by
      browser autoplay policies).
   ============================================================================ */
const SoundEngine = (() => {
    let ctx = null;
    let muted = false;

    function ensureContext() {
        if (!ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            ctx = new AudioCtx();
        }
        if (ctx.state === 'suspended') ctx.resume();
        return ctx;
    }

    function tone({ freq = 440, duration = 0.09, type = 'sine', gain = 0.06, glideTo = null }) {
        if (muted) return;
        try {
            const audioCtx = ensureContext();
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            if (glideTo) {
                osc.frequency.exponentialRampToValueAtTime(glideTo, audioCtx.currentTime + duration);
            }
            gainNode.gain.setValueAtTime(gain, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration + 0.02);
        } catch (err) {
            console.warn('SoundEngine: unable to play tone', err);
        }
    }

    return {
        click:   () => tone({ freq: 520, duration: 0.07, type: 'triangle', gain: 0.05 }),
        toggleOn:  () => tone({ freq: 440, duration: 0.11, type: 'sine', gain: 0.06, glideTo: 720 }),
        toggleOff: () => tone({ freq: 520, duration: 0.11, type: 'sine', gain: 0.06, glideTo: 260 }),
        success: () => {
            tone({ freq: 523, duration: 0.09, type: 'sine', gain: 0.06 });
            setTimeout(() => tone({ freq: 784, duration: 0.14, type: 'sine', gain: 0.06 }), 90);
        },
        error: () => tone({ freq: 180, duration: 0.22, type: 'sawtooth', gain: 0.05, glideTo: 90 }),
        dropdown: () => tone({ freq: 660, duration: 0.05, type: 'triangle', gain: 0.04 }),
        setMuted(value) { muted = value; },
        isMuted() { return muted; },
    };
})();

/* ============================================================================
   2. TOAST NOTIFICATIONS — replaces alert() with non-blocking feedback.
   ============================================================================ */
function showToast(message, kind = 'info', duration = 3200) {
    const stack = document.getElementById('toastStack');
    const toast = document.createElement('div');
    toast.className = `toast ${kind}`;

    const icons = { success: 'fa-circle-check', error: 'fa-circle-exclamation', info: 'fa-circle-info' };
    toast.innerHTML = `
        <span class="toast-icon"><i class="fas ${icons[kind] || icons.info}"></i></span>
        <span>${message}</span>
    `;
    stack.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add('visible'));

    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 260);
    }, duration);
}

/* ============================================================================
   3. RIPPLE EFFECT — plain expanding circle on click, no colored glow.
   ============================================================================ */
function attachRipple(el) {
    el.addEventListener('click', function (e) {
        const rect = this.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
        this.style.position = this.style.position || 'relative';
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
}

document.querySelectorAll('.btn-search, .btn-buy').forEach(attachRipple);

/* ============================================================================
   4. ANIMATED NUMBER COUNT-UP — for guild level / members / capacity.
   ============================================================================ */
function animateCount(el, targetValue, { prefix = '', suffix = '', duration = 650 } = {}) {
    const numeric = parseInt(String(targetValue).replace(/[^\d]/g, ''), 10);
    if (Number.isNaN(numeric)) {
        el.innerText = targetValue;
        return;
    }
    const start = performance.now();
    function frame(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(numeric * eased);
        el.innerText = `${prefix}${current}${suffix}`;
        if (progress < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
}

/* ============================================================================
   5. INPUT VALIDATION
   ============================================================================ */
const uidInput = document.getElementById('uidInput');
const inputError = document.getElementById('inputError');
const searchContainer = document.getElementById('searchContainer');

uidInput.addEventListener('input', () => {
    uidInput.value = uidInput.value.replace(/[^\d]/g, '');
    if (inputError.classList.contains('show')) validateUid(false);
});

function validateUid(showFeedback = true) {
    const value = uidInput.value.trim();
    const valid = /^\d{6,}$/.test(value);
    if (!valid && showFeedback) {
        inputError.classList.add('show');
        searchContainer.style.background = 'var(--surface-2)';
        SoundEngine.error();
    } else {
        inputError.classList.remove('show');
    }
    return valid;
}

uidInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') fetchData(e);
});

/* ============================================================================
   6. FETCH + RENDER
   ============================================================================ */
async function fetchData(e) {
    if (e) e.preventDefault();
    SoundEngine.click();

    if (!validateUid(true)) return;
    const uid = uidInput.value.trim();

    const searchBtn = document.getElementById('searchBtn');
    const skeletonBlock = document.getElementById('skeletonBlock');
    const bannerCard = document.getElementById('bannerCard');
    const bannerImg = document.getElementById('playerBanner');
    const infoGrid = document.getElementById('infoGrid');
    const settingsPanel = document.getElementById('settingsPanel');

    searchBtn.classList.add('loading');
    searchBtn.disabled = true;
    skeletonBlock.classList.add('show');
    bannerCard.style.display = 'none';
    infoGrid.style.display = 'none';
    settingsPanel.style.display = 'none';

    // Banner is loaded independently of the info lookup below: if the
    // banner service is slow/down it should never block or fail the rest
    // of the dashboard. A broken image just hides itself, quietly.
    bannerImg.onerror = () => { bannerCard.style.display = 'none'; };
    bannerImg.onload = () => { bannerCard.style.display = 'flex'; };
    bannerImg.src = `/api/banner?uid=${encodeURIComponent(uid)}`;

    try {
        // Same-origin call — the browser never applies CORS to this, so a
        // blocked/CORS-less third-party API can no longer cause a silent
        // "Something went wrong" with no real explanation.
        const response = await fetch(`/api/player-info?uid=${encodeURIComponent(uid)}`, {
            headers: { 'Accept': 'application/json' },
        });

        let payload;
        try {
            payload = await response.json();
        } catch (parseErr) {
            throw new Error('The server sent back an unreadable response.');
        }

        if (!response.ok || !payload.success) {
            // The backend always supplies a specific, human-readable reason.
            throw new Error(payload.error || `Request failed (status ${response.status}).`);
        }

        const g = payload.data.GuildInfo || {};
        document.getElementById('g_name').innerText = g.GuildName || 'N/A';
        document.getElementById('g_id').innerText = g.GuildID || 'N/A';
        animateCount(document.getElementById('g_level'), g.GuildLevel || 0, { prefix: 'Level ' });
        animateCount(document.getElementById('g_members'), g.GuildMember || 0);
        animateCount(document.getElementById('g_capacity'), g.GuildCapacity || 0);
        document.getElementById('g_owner').innerText = g.GuildOwner || 'N/A';

        infoGrid.style.display = 'grid';
        settingsPanel.style.display = 'flex';
        showToast('Guild data loaded successfully.', 'success');
        SoundEngine.success();
    } catch (err) {
        console.error(err);
        // Network-level failure (server unreachable, offline, etc.) vs. a
        // specific error message from our own backend get slightly
        // different, still-honest wording.
        const isNetworkFailure = err instanceof TypeError;
        const message = isNetworkFailure
            ? 'Cannot reach the server. Check your connection and try again.'
            : (err.message || 'Something went wrong. Please try again.');
        showToast(message, 'error', 4200);
        SoundEngine.error();
    } finally {
        skeletonBlock.classList.remove('show');
        searchBtn.classList.remove('loading');
        searchBtn.disabled = false;
    }
}

/* ============================================================================
   7. COPY GUILD ID
   ============================================================================ */
async function copyGuildId(e) {
    e.stopPropagation();
    SoundEngine.click();
    const value = document.getElementById('g_id').innerText.trim();
    if (!value || value === '—') {
        showToast('Nothing to copy yet.', 'error');
        return;
    }
    try {
        await navigator.clipboard.writeText(value);
        showToast('Guild ID copied to clipboard.', 'success');
    } catch (err) {
        console.warn('Clipboard write failed', err);
        showToast('Unable to copy automatically — please copy manually.', 'error');
    }
}

/* ============================================================================
   8. SEGMENTED TOGGLE
   ============================================================================ */
document.querySelectorAll('.toggle').forEach((toggle) => {
    toggle.querySelectorAll('.toggle-option').forEach((option) => {
        option.addEventListener('click', function () {
            const value = this.dataset.value;
            toggle.querySelectorAll('.toggle-option').forEach((o) => o.classList.remove('selected', 'on', 'off'));
            this.classList.add('selected', value);
            toggle.dataset.state = value;
            if (value === 'on') {
                SoundEngine.toggleOn();
                showToast('Auto approval enabled.', 'success', 1800);
            } else {
                SoundEngine.toggleOff();
                showToast('Auto approval disabled.', 'info', 1800);
            }
        });
    });
});

/* ============================================================================
   9. FUNCTIONAL DROPDOWNS
   ============================================================================ */
document.querySelectorAll('.dropdown').forEach((dropdown) => {
    const trigger = dropdown.querySelector('.dropdown-trigger');
    const valueLabel = dropdown.querySelector('.dropdown-value');
    const items = dropdown.querySelectorAll('.dropdown-menu-item');

    trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const wasOpen = dropdown.classList.contains('open');
        document.querySelectorAll('.dropdown.open').forEach((d) => d.classList.remove('open'));
        if (!wasOpen) {
            dropdown.classList.add('open');
            SoundEngine.dropdown();
        }
    });

    items.forEach((item) => {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            items.forEach((i) => i.classList.remove('active'));
            item.classList.add('active');
            valueLabel.innerText = item.dataset.value;
            dropdown.classList.remove('open');
            SoundEngine.click();
            showToast(`${dropdown.dataset.name} set to ${item.dataset.value}.`, 'info', 1800);
        });
    });
});

document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown.open').forEach((d) => d.classList.remove('open'));
});

/* ============================================================================
   10. SOUND MUTE TOGGLE
   ============================================================================ */
const soundToggleBtn = document.getElementById('soundToggle');
soundToggleBtn.addEventListener('click', () => {
    const nowMuted = !SoundEngine.isMuted();
    SoundEngine.setMuted(nowMuted);
    soundToggleBtn.classList.toggle('muted', nowMuted);
    soundToggleBtn.innerHTML = `<i class="fas ${nowMuted ? 'fa-volume-xmark' : 'fa-volume-high'}"></i>`;
    if (!nowMuted) SoundEngine.click();
});

/* ============================================================================
   11. BUY BUTTON FEEDBACK
   ============================================================================ */
document.getElementById('buyBtn').addEventListener('click', () => {
    SoundEngine.success();
});
</script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render the CKRPRO AND BBC dashboard."""
    return render_template_string(HTML_TEMPLATE)


# ============================================================================
# Backend proxy routes
# ----------------------------------------------------------------------------
# The frontend never talks to the third-party APIs directly anymore — it
# only calls these same-origin endpoints. That removes the CORS failure
# mode entirely and lets us return one consistent, typed response shape
# regardless of what the upstream API does:
#     {"success": true,  "data": {...}}
#     {"success": false, "error": "<specific, human-readable reason>"}
# ============================================================================
PLAYER_INFO_API = "https://player-info-by-ckrpro.vercel.app/get"
BANNER_API = "https://ff-banner-api-one.vercel.app/profile"
UPSTREAM_TIMEOUT = 10  # seconds


def _valid_uid(uid: str) -> bool:
    """A Free Fire UID is purely numeric and realistically 6+ digits."""
    return uid.isdigit() and len(uid) >= 6


@app.route('/api/player-info')
def api_player_info():
    """
    Server-side proxy for the player/guild-info lookup. Every failure
    mode gets its own specific, user-facing reason instead of a generic
    "something went wrong" — matching what the dashboard displays.
    """
    uid = request.args.get('uid', '').strip()
    if not _valid_uid(uid):
        return jsonify(success=False, error="Please enter a valid numeric UID (6+ digits)."), 400

    try:
        upstream = requests.get(PLAYER_INFO_API, params={"uid": uid}, timeout=UPSTREAM_TIMEOUT)
    except requests.exceptions.Timeout:
        return jsonify(success=False, error="The player info service timed out. Please try again."), 504
    except requests.exceptions.ConnectionError:
        return jsonify(success=False, error="Unable to reach the player info service right now."), 502
    except requests.exceptions.RequestException as exc:
        return jsonify(success=False, error=f"Network error while contacting the player info service: {exc}"), 502

    if upstream.status_code == 404:
        return jsonify(success=False, error="No player found for this UID."), 404
    if upstream.status_code != 200:
        return jsonify(
            success=False,
            error=f"Player info service returned an unexpected status ({upstream.status_code}).",
        ), 502

    try:
        data = upstream.json()
    except ValueError:
        return jsonify(success=False, error="Player info service returned an unreadable response."), 502

    if not data or "GuildInfo" not in data:
        return jsonify(success=False, error="No guild data found for this UID."), 404

    return jsonify(success=True, data=data)


@app.route('/api/banner')
def api_banner():
    """
    Server-side proxy for the player banner image. Streams the upstream
    image bytes back through this same origin so <img> never depends on
    the third-party host being directly reachable/CORS-friendly, and so
    the frontend can cleanly detect failure via a normal HTTP status
    instead of a broken-image icon with no explanation.
    """
    uid = request.args.get('uid', '').strip()
    if not _valid_uid(uid):
        return Response("Invalid UID.", status=400)

    try:
        upstream = requests.get(BANNER_API, params={"uid": uid}, timeout=UPSTREAM_TIMEOUT, stream=True)
    except requests.exceptions.Timeout:
        return Response("Banner service timed out.", status=504)
    except requests.exceptions.RequestException as exc:
        return Response(f"Banner service unreachable: {exc}", status=502)

    if upstream.status_code != 200:
        return Response("Banner not available.", status=upstream.status_code)

    content_type = upstream.headers.get("Content-Type", "image/png")
    return Response(upstream.content, content_type=content_type)


if __name__ == '__main__':
    app.run(debug=True)
