import streamlit as st
import sqlite3
import datetime
import pandas as pd
import base64
import requests
import hashlib



# Configuración de la página

st.set_page_config(page_title="MAR'S GYM | Premium", page_icon="Logo GYM.png", layout="wide", initial_sidebar_state="collapsed")

# === Meta tags PWA (instalable como app) ===
st.markdown("""
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#FFB300">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="MARY'S GYM">
<meta name="application-name" content="MARY'S GYM">
<meta name="msapplication-TileColor" content="#0A0E17">
<link rel="icon" type="image/png" sizes="32x32" href="/static/icon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="/static/icon-64.png">
<link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/static/icon-512.png">
<link rel="shortcut icon" type="image/png" href="/static/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/static/icon-180.png">
<link rel="apple-touch-icon" sizes="192x192" href="/static/icon-192.png">
<link rel="apple-touch-icon" sizes="512x512" href="/static/icon-512.png">
""", unsafe_allow_html=True)

# Estilos CSS Avanzados (Mejorados)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Bebas+Neue&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    * { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

    /* ====== ANIMACIONES ====== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 179, 0, 0.5); }
        70% { box-shadow: 0 0 0 14px rgba(255, 179, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 179, 0, 0); }
    }
    @keyframes glowPulse {
        0%, 100% { filter: drop-shadow(0 0 18px rgba(255, 179, 0, 0.35)); }
        50% { filter: drop-shadow(0 0 32px rgba(255, 179, 0, 0.7)); }
    }
    @keyframes auroraMove {
        0%   { transform: translate(0, 0) scale(1);    opacity: 0.55; }
        50%  { transform: translate(40px, -30px) scale(1.15); opacity: 0.8; }
        100% { transform: translate(0, 0) scale(1);    opacity: 0.55; }
    }
    @keyframes auroraMoveAlt {
        0%   { transform: translate(0, 0) scale(1);    opacity: 0.45; }
        50%  { transform: translate(-50px, 40px) scale(1.2); opacity: 0.7; }
        100% { transform: translate(0, 0) scale(1);    opacity: 0.45; }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ====== FONDO PRINCIPAL ANIMADO ====== */
    .stApp {
        background: radial-gradient(ellipse at top left, #1a1530 0%, #0a0e17 45%, #050810 100%);
        color: #FFFFFF;
        position: relative;
        overflow-x: hidden;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: -25%;
        left: -15%;
        width: 60vw;
        height: 60vw;
        background: radial-gradient(circle, rgba(255, 179, 0, 0.18) 0%, rgba(255, 111, 0, 0.05) 35%, transparent 70%);
        border-radius: 50%;
        filter: blur(80px);
        animation: auroraMove 18s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }
    .stApp::after {
        content: "";
        position: fixed;
        bottom: -20%;
        right: -10%;
        width: 55vw;
        height: 55vw;
        background: radial-gradient(circle, rgba(120, 80, 220, 0.18) 0%, rgba(80, 40, 180, 0.05) 35%, transparent 70%);
        border-radius: 50%;
        filter: blur(90px);
        animation: auroraMoveAlt 22s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }
    [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container {
        position: relative;
        z-index: 1;
    }
    .block-container { padding-top: 2rem; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(10, 14, 23, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #FFB300, #FF6F00);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #FFC233, #FF8533); }

    /* Selección de texto */
    ::selection { background: rgba(255, 179, 0, 0.35); color: #fff; }

    /* ====== HEADER ====== */
    .header-container {
        text-align: center;
        padding: 45px 30px;
        background: linear-gradient(135deg, rgba(21, 28, 44, 0.55) 0%, rgba(40, 25, 60, 0.45) 100%);
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border-radius: 28px;
        margin-bottom: 35px;
        border: 1px solid rgba(255, 179, 0, 0.18);
        animation: fadeIn 0.8s ease-out;
        box-shadow:
            0 25px 60px rgba(0, 0, 0, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.08),
            0 0 50px rgba(255, 179, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    .header-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFB300, #FF6F00, #FFB300, transparent);
        background-size: 200% 100%;
        animation: shimmer 4s linear infinite;
    }
    .header-title {
        font-family: 'Bebas Neue', 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 4.2rem;
        background: linear-gradient(90deg, #FFD54F 0%, #FFB300 30%, #FF8F00 60%, #FF6F00 100%);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: 4px;
        animation: glowPulse 3.5s ease-in-out infinite, gradientShift 8s ease infinite;
    }
    .header-subtitle {
        font-weight: 500;
        color: #A8B5C7;
        font-size: 1.05rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-top: 10px;
    }
    .header-subtitle::before, .header-subtitle::after {
        content: "—"; color: #FFB300; margin: 0 14px; opacity: 0.7;
    }

    /* ====== MÉTRICAS ====== */
    .metric-card {
        background: linear-gradient(145deg, rgba(28, 35, 55, 0.7), rgba(15, 22, 38, 0.6));
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        padding: 28px 25px;
        border-radius: 22px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        text-align: center;
        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.06);
        max-width: 420px;
        margin: 0 auto 20px auto;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInScale 0.7s ease-out;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 179, 0, 0.08), transparent);
        transition: left 0.7s ease;
    }
    .metric-card:hover::before { left: 100%; }
    .metric-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 179, 0, 0.6);
        box-shadow:
            0 0 35px rgba(255, 179, 0, 0.25),
            0 25px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .metric-value {
        font-family: 'Bebas Neue', 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFD54F, #FFB300, #FF8F00);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 179, 0, 0.3);
        letter-spacing: 2px;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #A8B5C7;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 10px;
        font-weight: 700;
    }

    /* ====== TABS ====== */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(21, 28, 44, 0.65), rgba(15, 22, 38, 0.55));
        border-radius: 18px;
        padding: 10px;
        display: flex;
        justify-content: center;
        gap: 12px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    }
    .stTabs [data-baseweb="tab"] {
        color: #A8B5C7 !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 13px 26px;
        border-radius: 13px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        border: none !important;
        position: relative;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #FFFFFF !important;
        background: rgba(255, 179, 0, 0.08);
        transform: translateY(-1px);
    }
    .stTabs [aria-selected="true"] {
        color: #0A0E17 !important;
        background: linear-gradient(135deg, #FFD54F 0%, #FFB300 50%, #FF6F00 100%) !important;
        box-shadow:
            0 10px 25px rgba(255, 179, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transform: translateY(-3px);
        font-weight: 800;
    }

    /* ====== FORMULARIOS ====== */
    .stForm {
        background: linear-gradient(145deg, rgba(28, 35, 55, 0.55), rgba(15, 22, 38, 0.45)) !important;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: 26px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        padding: 35px !important;
        box-shadow:
            0 25px 50px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        animation: fadeIn 0.7s ease-out;
    }

    /* ====== BOTONES ====== */
    .stButton>button {
        background: linear-gradient(90deg, #FFD54F 0%, #FFB300 50%, #FF6F00 100%) !important;
        color: #0A0E17 !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        padding: 16px 22px !important;
        width: 100%;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow:
            0 8px 20px rgba(255, 179, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        position: relative;
        overflow: hidden;
    }
    .stButton>button::after {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s ease;
    }
    .stButton>button:hover::after { left: 100%; }
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow:
            0 0 35px rgba(255, 179, 0, 0.6),
            0 14px 30px rgba(255, 179, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        filter: brightness(1.08);
    }
    .stButton>button:active { transform: translateY(-1px); }

    /* ====== TARJETAS DE CLIENTE ====== */
    .client-card {
        background: linear-gradient(135deg, rgba(28, 35, 55, 0.55), rgba(15, 22, 38, 0.45));
        backdrop-filter: blur(15px);
        border-radius: 18px;
        padding: 22px 28px;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    .client-card::before {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #FFB300, #FF6F00);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .client-card:hover::before { opacity: 1; }
    .client-card:hover {
        background: linear-gradient(135deg, rgba(40, 30, 20, 0.7), rgba(20, 15, 25, 0.65));
        border-color: rgba(255, 179, 0, 0.4);
        transform: translateX(6px);
        box-shadow: 0 10px 25px rgba(255, 179, 0, 0.15), 0 0 20px rgba(255, 179, 0, 0.1);
    }

    .client-name { font-weight: 700; font-size: 1.25rem; color: #FFFFFF; letter-spacing: 0.3px; }
    .client-info { font-size: 0.95rem; color: #C8D2E0; margin-top: 8px; font-weight: 500; }
    .client-info .highlight { color: #FFB300; font-weight: 700; text-shadow: 0 0 10px rgba(255, 179, 0, 0.3); }

    .days-badge {
        background: linear-gradient(135deg, rgba(255, 179, 0, 0.18), rgba(255, 111, 0, 0.12));
        color: #FFD54F;
        padding: 5px 12px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 0.82rem;
        border: 1px solid rgba(255, 179, 0, 0.35);
        margin-left: 10px;
        display: inline-block;
        box-shadow: 0 3px 8px rgba(255, 179, 0, 0.15);
        letter-spacing: 0.5px;
    }

    /* ====== BADGES ====== */
    .badge {
        padding: 8px 18px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: inline-block;
    }
    .badge-active {
        background: linear-gradient(135deg, rgba(255, 179, 0, 0.15), rgba(255, 111, 0, 0.1));
        color: #FFD54F;
        border: 1px solid rgba(255, 179, 0, 0.4);
        animation: pulse 2.5s infinite;
    }
    .badge-warning {
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.18), rgba(255, 140, 0, 0.12));
        color: #FFAA00;
        border: 1px solid rgba(255, 170, 0, 0.4);
    }
    .badge-expired {
        background: linear-gradient(135deg, rgba(255, 0, 85, 0.15), rgba(200, 0, 60, 0.1));
        color: #FF3370;
        border: 1px solid rgba(255, 0, 85, 0.4);
    }
    .badge-plan {
        background: linear-gradient(135deg, rgba(120, 80, 220, 0.18), rgba(80, 40, 180, 0.12));
        color: #B19BFF;
        border: 1px solid rgba(140, 100, 240, 0.35);
        padding: 5px 13px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    /* ====== WHATSAPP LINK ====== */
    .wa-link {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: #FFFFFF !important;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 9px 18px;
        border-radius: 11px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 5px 14px rgba(37, 211, 102, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .wa-link:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(37, 211, 102, 0.5), 0 8px 20px rgba(37, 211, 102, 0.4);
        filter: brightness(1.12);
        color: #FFFFFF !important;
    }

    /* ====== TABLAS ====== */
    .custom-table-container {
        background: linear-gradient(145deg, rgba(28, 35, 55, 0.55), rgba(15, 22, 38, 0.45));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 22px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        margin-top: 18px;
        overflow-x: auto;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        color: white;
        text-align: left;
    }
    .custom-table th, .custom-table td {
        padding: 16px 22px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .custom-table th {
        background: linear-gradient(135deg, rgba(10, 14, 23, 0.8), rgba(20, 25, 40, 0.7));
        font-weight: 800;
        color: #FFB300;
        text-transform: uppercase;
        font-size: 0.78rem;
        letter-spacing: 2px;
        border-bottom: 2px solid rgba(255, 179, 0, 0.25);
    }
    .custom-table tr { transition: all 0.25s ease; }
    .custom-table tr:hover td {
        background: rgba(255, 179, 0, 0.06);
        color: #FFD54F;
    }
    .custom-table td { font-size: 0.95rem; font-weight: 500; }

    /* ====== INPUTS ====== */
    .stTextInput>div>div>input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea {
        background-color: rgba(15, 22, 38, 0.65) !important;
        border-radius: 13px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        padding: 13px 16px !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    .stSelectbox>div>div>div {
        background-color: rgba(15, 22, 38, 0.65) !important;
        border-radius: 13px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox>div>div>div:focus-within {
        border-color: #FFB300 !important;
        box-shadow: 0 0 0 3px rgba(255, 179, 0, 0.18), 0 0 20px rgba(255, 179, 0, 0.25) !important;
        background-color: rgba(20, 28, 48, 0.85) !important;
    }
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextArea label, .stCheckbox label {
        color: #C8D2E0 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.4px;
    }

    /* Checkbox */
    .stCheckbox > label > div:first-child {
        background-color: rgba(15, 22, 38, 0.7) !important;
        border-radius: 6px !important;
    }

    /* Mensajes */
    .stAlert, div[data-baseweb="notification"] {
        border-radius: 14px !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Expander */
    .streamlit-expanderHeader, [data-testid="stExpander"] summary {
        background: linear-gradient(135deg, rgba(28, 35, 55, 0.6), rgba(15, 22, 38, 0.5)) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        color: #FFB300 !important;
        transition: all 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover, [data-testid="stExpander"] summary:hover {
        border-color: rgba(255, 179, 0, 0.35) !important;
        background: linear-gradient(135deg, rgba(40, 30, 20, 0.6), rgba(25, 18, 35, 0.5)) !important;
    }

    /* Subheaders */
    h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
    }

    /* Login */
    .login-hero {
        text-align: center;
        margin: 70px auto 30px auto;
        padding: 30px 20px;
        animation: fadeInScale 0.9s ease-out;
    }
    .login-icon {
        font-size: 64px;
        background: linear-gradient(135deg, #FFD54F, #FFB300, #FF6F00);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 18px;
        animation: glowPulse 3s ease-in-out infinite, float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(255, 179, 0, 0.6));
    }
    .login-title {
        font-family: 'Bebas Neue', 'Outfit', sans-serif;
        font-size: 3.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFD54F, #FFB300, #FF6F00);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 6px;
        animation: gradientShift 6s ease infinite;
        margin-bottom: 8px;
    }
    .login-subtitle {
        font-weight: 600;
        color: #FFB300;
        font-size: 0.95rem;
        letter-spacing: 5px;
        text-transform: uppercase;
        opacity: 0.9;
    }
    .login-desc {
        color: #A8B5C7;
        font-size: 1rem;
        margin-top: 14px;
        letter-spacing: 0.5px;
    }

    /* Logo principal */
    .logo-glow {
        border-radius: 22px;
        margin-bottom: 18px;
        padding: 6px;
        background: linear-gradient(145deg, rgba(255, 179, 0, 0.18), rgba(255, 111, 0, 0.08));
        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.45),
            0 0 30px rgba(255, 179, 0, 0.25),
            inset 0 0 0 1px rgba(255, 179, 0, 0.3);
        animation: float 4s ease-in-out infinite, glowPulse 4s ease-in-out infinite;
        transition: transform 0.4s ease;
    }
    .logo-glow:hover {
        transform: scale(1.04) rotate(0.5deg);
    }

    /* Tab icon header (PNG redondo) */
    .tab-icon-header {
        text-align: center;
        margin: 20px 0 10px 0;
        animation: float 3.5s ease-in-out infinite;
    }
    .tab-icon-header img {
        border-radius: 50%;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.4),
            0 0 25px rgba(255, 179, 0, 0.25),
            inset 0 0 0 2px rgba(255, 179, 0, 0.4);
        padding: 4px;
        background: linear-gradient(145deg, rgba(255, 179, 0, 0.1), rgba(255, 111, 0, 0.05));
    }

</style>
""", unsafe_allow_html=True)

# === Registrar Service Worker para PWA ===
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registrado correctamente');
        setInterval(() => {
          registration.update();
        }, 60000);
      })
      .catch((error) => {
        console.error('Error al registrar Service Worker:', error);
      });

    let refreshing;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    });
  });
}
</script>
""", unsafe_allow_html=True)

# Cargar iconos para las pestañas
def get_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

icon_dash = get_base64("icon_dashboard.png")
icon_pay = get_base64("icon_payments.png")
icon_att = get_base64("icon_attendance.png")
icon_man = get_base64("icon_manage.png")
icon_his = get_base64("icon_history.png")
icon_att_his = get_base64("icon_attendance_history.png")

css_tabs = f"""
<style>
    div[data-baseweb="tab-list"] button:nth-child(1)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_dash}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    div[data-baseweb="tab-list"] button:nth-child(2)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_pay}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    div[data-baseweb="tab-list"] button:nth-child(3)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_att}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    div[data-baseweb="tab-list"] button:nth-child(4)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_man}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    div[data-baseweb="tab-list"] button:nth-child(5)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_his}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    div[data-baseweb="tab-list"] button:nth-child(6)::before {{
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        background-image: url('data:image/png;base64,{icon_att_his}');
        background-size: contain;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }}
    .tab-icon-header img {{
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}
</style>
"""
st.markdown(css_tabs, unsafe_allow_html=True)

# Inicialización de la Base de Datos
SUPABASE_URL = "https://zmvrfdtacxdudjmiswka.supabase.co"
SUPABASE_KEY = "sb_publishable__w3Thfledx3ORdNHxCigrw_WjyShcDg"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_login(username, password):
    hashed = hash_password(password)
    params = {
        "username": f"eq.{username}",
        "password": f"eq.{hashed}",
        "select": "username,rol"
    }
    res = supabase_request("GET", "usuarios", params=params)
    return res[0] if res else None

def supabase_request(method, table, params=None, json_data=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation" if method in ["POST", "PATCH"] else ""
    }
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, params=params, json=json_data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=params)
        
        if response.status_code in [200, 201, 204]:
            return response.json() if response.content else []
        else:
            st.error(f"Error en Supabase: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return []

# Funciones helper para teléfono (formato Colombia)
def telefono_para_mostrar(tel):
    """Devuelve solo los últimos 10 dígitos para mostrar en el input."""
    if not tel:
        return ""
    digitos = "".join(filter(str.isdigit, str(tel)))
    if len(digitos) > 10:
        return digitos[-10:]
    return digitos

def telefono_para_guardar(tel):
    """Normaliza el teléfono: si tiene 10 dígitos, le antepone el 57."""
    if not tel:
        return ""
    digitos = "".join(filter(str.isdigit, str(tel)))
    if len(digitos) == 10:
        return "57" + digitos
    return digitos

# Funciones de base de datos
def get_clientes():
    params = {
        "nombre": "neq.CLIENTE CASUAL",
        "or": "(borrado.is.null,borrado.eq.false)",
        "select": "*"
    }
    data = supabase_request("GET", "clientes", params=params)
    return pd.DataFrame(data) if data else pd.DataFrame(columns=['id', 'nombre', 'telefono', 'fecha_ultimo_pago', 'fecha_vencimiento', 'plan_actual', 'borrado'])

def get_tarifas():
    res = supabase_request("GET", "tarifas", params={"select": "categoria,plan_tipo,monto"})
    if res:
        tarifas = {"Normal": {}, "Con Entrenadora": {}}
        for r in res:
            tarifas[r['categoria']][r['plan_tipo']] = r['monto']
        return tarifas
    return {
        "Normal": {"Rutina": 5000, "Semana": 20000, "Quincena": 40000, "Mensual": 60000},
        "Con Entrenadora": {"Rutina": 10000, "Semana": 30000, "Quincena": 60000, "Mensual": 100000}
    }

def calcular_vencimiento(fecha_inicio, plan_tipo):
    if plan_tipo == "Rutina":
        return fecha_inicio
    elif plan_tipo == "Semana":
        return fecha_inicio + datetime.timedelta(days=6)
    elif plan_tipo == "Quincena":
        return fecha_inicio + datetime.timedelta(days=14)
    elif plan_tipo == "Mensual":
        vencimiento = pd.to_datetime(fecha_inicio) + pd.DateOffset(months=1) - pd.Timedelta(days=1)
        return vencimiento.date()
    return fecha_inicio

def registrar_pago(nombre, telefono, plan_tipo, con_entrenadora, metodo_pago):
    hoy = str(datetime.date.today())
    categoria = "Con Entrenadora" if con_entrenadora else "Normal"
    tarifas = get_tarifas()
    monto = tarifas[categoria][plan_tipo]
    vencimiento = str(calcular_vencimiento(datetime.date.today(), plan_tipo))
    
    # Buscar cliente
    params = {"nombre": f"eq.{nombre}", "select": "id"}
    clientes = supabase_request("GET", "clientes", params=params)
    
    if clientes:
        cliente_id = clientes[0]['id']
        # Update
        json_data = {
            "fecha_ultimo_pago": hoy,
            "fecha_vencimiento": vencimiento,
            "telefono": telefono,
            "plan_actual": plan_tipo,
            "con_entrenadora": con_entrenadora
        }
        supabase_request("PATCH", "clientes", params={"id": f"eq.{cliente_id}"}, json_data=json_data)
    else:
        # Insert
        json_data = {
            "nombre": nombre,
            "telefono": telefono,
            "fecha_ultimo_pago": hoy,
            "fecha_vencimiento": vencimiento,
            "plan_actual": plan_tipo,
            "con_entrenadora": con_entrenadora
        }
        res = supabase_request("POST", "clientes", json_data=json_data)
        if res:
            cliente_id = res[0]['id']
        else:
            return
            
    # Registrar pago
    pago_data = {
        "cliente_id": cliente_id,
        "monto": monto,
        "fecha": hoy,
        "plan_tipo": plan_tipo,
        "metodo_pago": metodo_pago,
        "con_entrenadora": con_entrenadora
    }
    supabase_request("POST", "pagos", json_data=pago_data)

def registrar_pago_casual(monto, notas):
    hoy = str(datetime.date.today())
    
    # Buscar CLIENTE CASUAL
    params = {"nombre": "eq.CLIENTE CASUAL", "select": "id"}
    clientes = supabase_request("GET", "clientes", params=params)
    
    if clientes:
        cliente_id = clientes[0]['id']
    else:
        # Crear si no existe
        res = supabase_request("POST", "clientes", json_data={"nombre": "CLIENTE CASUAL"})
        cliente_id = res[0]['id'] if res else None
        
    if cliente_id:
        pago_data = {
            "cliente_id": cliente_id,
            "monto": monto,
            "fecha": hoy,
            "notas": notas
        }
        supabase_request("POST", "pagos", json_data=pago_data)

def get_ingresos_hoy():
    hoy = str(datetime.date.today())
    params = {"fecha": f"eq.{hoy}", "select": "monto"}
    pagos = supabase_request("GET", "pagos", params=params)
    return sum(p['monto'] for p in pagos) if pagos else 0.0

def get_casuales_hoy():
    hoy = str(datetime.date.today())
    params = {
        "fecha": f"eq.{hoy}",
        "select": "monto,notas,clientes!inner(nombre)",
        "clientes.nombre": "eq.CLIENTE CASUAL"
    }
    data = supabase_request("GET", "pagos", params=params)
    if data:
        return pd.DataFrame([{"monto": r["monto"], "notas": r["notas"]} for r in data])
    return pd.DataFrame(columns=["monto", "notas"])

def registrar_asistencia(cliente_id):
    hoy = str(datetime.date.today())
    params = {
        "cliente_id": f"eq.{cliente_id}",
        "fecha": f"gte.{hoy}T00:00:00",
        "select": "id"
    }
    asistencias = supabase_request("GET", "asistencia", params=params)
    
    if not asistencias:
        supabase_request("POST", "asistencia", json_data={"cliente_id": int(cliente_id)})

def get_ingresos_semana():
    hoy = datetime.date.today()
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    params = [
        ("fecha", f"gte.{inicio_semana}"),
        ("fecha", f"lte.{hoy}"),
        ("select", "monto")
    ]
    pagos = supabase_request("GET", "pagos", params=params)
    return sum(p['monto'] for p in pagos) if pagos else 0.0

def get_ingresos_mes():
    hoy = datetime.date.today()
    inicio_mes = hoy.replace(day=1)
    params = [
        ("fecha", f"gte.{inicio_mes}"),
        ("fecha", f"lte.{hoy}"),
        ("select", "monto")
    ]
    pagos = supabase_request("GET", "pagos", params=params)
    return sum(p['monto'] for p in pagos) if pagos else 0.0

def get_asistencia_hoy():
    hoy = str(datetime.date.today())
    params = {
        "fecha": f"gte.{hoy}T00:00:00",
        "select": "fecha,clientes!inner(nombre)"
    }
    data = supabase_request("GET", "asistencia", params=params)
    if data:
        formatted = []
        for r in data:
            dt = pd.to_datetime(r["fecha"])
            formatted.append({
                "nombre": r["clientes"]["nombre"],
                "dia": dt.strftime('%d/%m/%Y'),
                "hora": dt.strftime('%H:%M:%S')
            })
        return pd.DataFrame(formatted)
    return pd.DataFrame(columns=["nombre", "dia", "hora"])

# --- INTERFAZ ---

# Manejo de Sesión / Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

if not st.session_state.logged_in:
    st.markdown('''
    <div class="login-hero">
        <div class="login-icon"><i class="fa-solid fa-dumbbell"></i></div>
        <div class="login-title">MARY'S GYM</div>
        <div class="login-subtitle">— Acceso al Panel —</div>
        <div class="login-desc">Ingresa tus credenciales para acceder</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit_login = st.form_submit_button("INICIAR SESIÓN")
            
            if submit_login:
                user = verificar_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user['rol']
                    st.session_state.username = user['username']
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
    st.stop()
# Cargar Logo
try:
    with open("Logo GYM.png", "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    logo_base64 = ""

# Header
logo_img_html = f'<img src="data:image/png;base64,{logo_base64}" width="220" class="logo-glow" />' if logo_base64 else ""
st.markdown(
    '<div class="header-container"><div>'
    + logo_img_html
    + '<div class="header-title">MARY&#39;S GYM</div>'
    + '<div class="header-subtitle">Panel de Control Premium</div>'
    + '</div></div>',
    unsafe_allow_html=True
)

# Botón de Cerrar Sesión
col_logout1, col_logout2 = st.columns([5, 1])
with col_logout2:
    if st.button("Cerrar Sesión", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.rerun()

# KPIs
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_hoy():,.0f}</div><div class="metric-label">Ingresos Hoy</div></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_semana():,.0f}</div><div class="metric-label">Esta Semana</div></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${get_ingresos_mes():,.0f}</div><div class="metric-label">Este Mes</div></div>', unsafe_allow_html=True)

# Tabs dependientes del rol
if st.session_state.user_role == 'super_admin':
    tabs = st.tabs(["DASHBOARD", "REGISTRAR PAGO", "ASISTENCIA", "GESTIONAR", "HISTORIAL", "HIST. ASISTENCIA", "CONFIGURACIÓN"])
    tab_dash, tab_reg, tab_asist, tab_gest, tab_hist, tab_asist_hist, tab_config = tabs
else:
    tabs = st.tabs(["DASHBOARD", "REGISTRAR PAGO", "ASISTENCIA", "GESTIONAR", "HISTORIAL", "HIST. ASISTENCIA"])
    tab_dash, tab_reg, tab_asist, tab_gest, tab_hist, tab_asist_hist = tabs

with tab_dash:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_dashboard.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Estado de Clientes")
    df_clientes = get_clientes()
    
    if not df_clientes.empty:
        df_clientes['fecha_vencimiento'] = pd.to_datetime(df_clientes['fecha_vencimiento']).dt.date
        hoy = datetime.date.today()
        df_clientes['Dias_Restantes'] = df_clientes['fecha_vencimiento'].apply(lambda x: (x - hoy).days)
        df_clientes = df_clientes.sort_values('Dias_Restantes')
        
        # Filtrar clientes con planes largos (Semana, Quincena, Mensual) para las columnas
        df_planes_largos = df_clientes[df_clientes['plan_actual'].isin(['Semana', 'Quincena', 'Mensual'])]
        
        # Filtrar clientes de rutina pagados HOY
        df_rutinas_hoy = df_clientes[(df_clientes['plan_actual'] == 'Rutina') & (df_clientes['fecha_ultimo_pago'] == str(hoy))]
        
        col_act, col_por, col_ven = st.columns(3)
        
        with col_act:
            st.markdown("### Activos")
            for index, row in df_planes_largos[df_planes_largos['Dias_Restantes'] > 3].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Vence: <span class="highlight">{row["fecha_vencimiento"]}</span> <span class="days-badge">{row["Dias_Restantes"]} días</span></div></div><div><span class="badge badge-active">Activo</span></div></div>', unsafe_allow_html=True)
        
        with col_por:
            st.markdown("### Por Vencer")
            for index, row in df_planes_largos[(df_planes_largos['Dias_Restantes'] <= 3) & (df_planes_largos['Dias_Restantes'] >= 0)].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Vence: <span class="highlight">{row["fecha_vencimiento"]}</span> <span class="days-badge">{row["Dias_Restantes"]} días</span></div></div><div><span class="badge badge-warning">Alerta</span></div></div>', unsafe_allow_html=True)
                
                if row['telefono']:
                    tel_limpio = "".join(filter(str.isdigit, row['telefono']))
                    msg = f"Hola {row['nombre']}, te recordamos que tu plan en MARY'S GYM está por vencer. ¡Te esperamos!"
                    link = f"https://wa.me/{tel_limpio}?text={msg.replace(' ', '%20')}"
                    st.markdown(f'<div style="text-align: right; margin-top: 5px;"><a href="{link}" target="_blank" class="wa-link">💬 WhatsApp</a></div>', unsafe_allow_html=True)


        with col_ven:
            st.markdown("### Vencidos")
            for index, row in df_planes_largos[df_planes_largos['Dias_Restantes'] < 0].iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">{row["plan_actual"]}</div><div class="client-info">Venció: <span class="highlight">{row["fecha_vencimiento"]}</span> <span class="days-badge">{abs(row["Dias_Restantes"])} días</span></div></div><div><span class="badge badge-expired">Vencido</span></div></div>', unsafe_allow_html=True)
                
                if row['telefono']:
                    tel_limpio = "".join(filter(str.isdigit, row['telefono']))
                    msg = f"Hola {row['nombre']}, tu plan en MARY'S GYM ya venció. Te invitamos a renovarlo. ¡Gracias!"
                    link = f"https://wa.me/{tel_limpio}?text={msg.replace(' ', '%20')}"
                    st.markdown(f'<div style="text-align: right; margin-top: 5px;"><a href="{link}" target="_blank" class="wa-link">💬 WhatsApp</a></div>', unsafe_allow_html=True)

                    
        # Sección para Rutinas de Hoy
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Rutinas de Hoy")
        if not df_rutinas_hoy.empty:
            for index, row in df_rutinas_hoy.iterrows():
                st.markdown(f'<div class="client-card"><div><div class="client-name">{row["nombre"]}</div><div class="badge-plan">RUTINA</div></div><div><span class="badge badge-active">Hoy</span></div></div>', unsafe_allow_html=True)
        else:
            st.info("No hay clientes con plan de Rutina registrados hoy.")
    else:
        st.info("No hay clientes registrados.")

with tab_reg:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_payments.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Registrar Pago")
    
    if 'success_pago' in st.session_state:
        st.success(st.session_state.success_pago)
        del st.session_state.success_pago
        
    st.markdown('''
<style>
    .tarifas-container {
        display: flex;
        gap: 22px;
        margin-bottom: 28px;
        animation: fadeIn 0.8s ease-out;
    }
    .tarifa-column {
        flex: 1;
        background: linear-gradient(145deg, rgba(28, 35, 55, 0.6), rgba(15, 22, 38, 0.5));
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: 20px;
        padding: 24px 22px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .tarifa-column::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 179, 0, 0.6), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .tarifa-column:hover::before { opacity: 1; }
    .tarifa-column:hover {
        border-color: rgba(255, 179, 0, 0.45);
        transform: translateY(-6px);
        box-shadow: 0 0 30px rgba(255, 179, 0, 0.18), 0 22px 45px rgba(0, 0, 0, 0.4);
    }
    .tarifa-column h3 {
        font-family: 'Bebas Neue', 'Outfit', sans-serif;
        background: linear-gradient(90deg, #FFD54F, #FFB300, #FF6F00);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.35rem;
        margin-bottom: 18px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 0;
        font-weight: 700;
    }
    .tarifa-item {
        display: flex;
        justify-content: space-between;
        padding: 12px 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.95rem;
        transition: all 0.25s ease;
    }
    .tarifa-item:hover {
        background: rgba(255, 179, 0, 0.04);
        padding-left: 12px;
    }
    .tarifa-item:last-child {
        border-bottom: none;
    }
    .tarifa-item span:first-child {
        color: #C8D2E0;
        font-weight: 600;
        letter-spacing: 0.4px;
    }
    .tarifa-item span:last-child {
        color: #FFD54F;
        font-weight: 800;
        text-shadow: 0 0 12px rgba(255, 179, 0, 0.35);
        letter-spacing: 0.3px;
    }
</style>
''', unsafe_allow_html=True)

    tarifas = get_tarifas()
    st.markdown(f'''
<div class="tarifas-container">
    <div class="tarifa-column">
        <h3>Plan Normal</h3>
        <div class="tarifa-item"><span>Rutina</span><span>${format(int(tarifas["Normal"]["Rutina"]), ",")}</span></div>
        <div class="tarifa-item"><span>Semana</span><span>${format(int(tarifas["Normal"]["Semana"]), ",")}</span></div>
        <div class="tarifa-item"><span>Quincena</span><span>${format(int(tarifas["Normal"]["Quincena"]), ",")}</span></div>
        <div class="tarifa-item"><span>Mensual</span><span>${format(int(tarifas["Normal"]["Mensual"]), ",")}</span></div>
    </div>
    <div class="tarifa-column">
        <h3>Con Entrenadora</h3>
        <div class="tarifa-item"><span>Rutina</span><span>${format(int(tarifas["Con Entrenadora"]["Rutina"]), ",")}</span></div>
        <div class="tarifa-item"><span>Semana</span><span>${format(int(tarifas["Con Entrenadora"]["Semana"]), ",")}</span></div>
        <div class="tarifa-item"><span>Quincena</span><span>${format(int(tarifas["Con Entrenadora"]["Quincena"]), ",")}</span></div>
        <div class="tarifa-item"><span>Mensual</span><span>${format(int(tarifas["Con Entrenadora"]["Mensual"]), ",")}</span></div>
    </div>
</div>
''', unsafe_allow_html=True)
    
    df_clientes = get_clientes()
    nombres_existentes = ["-- NUEVO CLIENTE --"] + sorted(df_clientes['nombre'].tolist()) if not df_clientes.empty else ["-- NUEVO CLIENTE --"]
    
    cliente_sel = st.selectbox("Seleccionar Cliente (para renovar) o 'NUEVO CLIENTE'", nombres_existentes)
    
    with st.form("registro_pago_form", clear_on_submit=True):
        if cliente_sel == "-- NUEVO CLIENTE --":
            nombre = st.text_input("Nombre del Cliente")
            tel_defecto = ""
        else:
            nombre = cliente_sel
            st.markdown(f"**Renovando plan para:** <span class='highlight'>{nombre}</span>", unsafe_allow_html=True)
            cliente_info = df_clientes[df_clientes['nombre'] == cliente_sel].iloc[0]
            tel_defecto = telefono_para_mostrar(cliente_info['telefono']) if 'telefono' in cliente_info else ""

        telefono = st.text_input("Teléfono (10 dígitos, ej: 3001234567)", value=tel_defecto, max_chars=10, placeholder="3001234567")
        plan = st.selectbox("Tipo de Plan", ["Rutina", "Semana", "Quincena", "Mensual"])
        entrenadora = st.checkbox("Con Entrenadora")
        metodo = st.selectbox("Método de Pago", ["Efectivo", "Nequi", "Transferencia", "Otro"])
        
        submit_btn = st.form_submit_button("REGISTRAR PAGO")
        
        if submit_btn:
            if nombre:
                telefono_norm = telefono_para_guardar(telefono)
                if telefono and len(telefono_norm) != 12:
                    st.error("El teléfono debe tener 10 dígitos.")
                else:
                    registrar_pago(nombre, telefono_norm, plan, entrenadora, metodo)
                    st.session_state.success_pago = f"¡Pago registrado para {nombre}!"
                    st.rerun()
            else:
                st.error("Por favor completa el nombre.")

with tab_asist:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_attendance.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Control de Asistencia")
    
    if 'success_asist' in st.session_state:
        st.success(st.session_state.success_asist)
        del st.session_state.success_asist
        
    df_clientes = get_clientes()
    if not df_clientes.empty:
        # Filtrar solo clientes con plan Semana, Quincena o Mensual
        df_clientes_filtrados = df_clientes[df_clientes['plan_actual'].isin(['Semana', 'Quincena', 'Mensual'])]
        
        # Obtener los que ya asistieron hoy
        df_asist_hoy = get_asistencia_hoy()
        asistidos_hoy = df_asist_hoy['nombre'].tolist() if not df_asist_hoy.empty else []
        
        # Filtrar los que NO han asistido hoy
        df_clientes_por_asistir = df_clientes_filtrados[~df_clientes_filtrados['nombre'].isin(asistidos_hoy)]
        
        if not df_clientes_por_asistir.empty:
            nombres_clientes = df_clientes_por_asistir['nombre'].tolist()
            
            with st.form("asistencia_form", clear_on_submit=False):
                cliente_sel = st.selectbox("Seleccionar Cliente para Asistencia", nombres_clientes)
                submit_asist = st.form_submit_button("REGISTRAR ENTRADA")
                
                if submit_asist:
                    cliente_id = df_clientes_por_asistir[df_clientes_por_asistir['nombre'] == cliente_sel]['id'].values[0]
                    registrar_asistencia(cliente_id)
                    st.session_state.success_asist = f"¡Asistencia registrada para {cliente_sel}!"
                    st.rerun()
        else:
            if df_clientes_filtrados.empty:
                st.info("No hay clientes con planes de Semana, Quincena o Mensual para registrar asistencia.")
            else:
                st.success("¡Todos los clientes aptos ya registraron su asistencia el día de hoy! 🏋️‍♂️")
            
    st.subheader("Asistentes de Hoy")
    df_asist = get_asistencia_hoy()
    if not df_asist.empty:
        html = '''<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Nombre</th>
<th>Día</th>
<th>Hora</th>
</tr>
</thead>
<tbody>'''
        for index, row in df_asist.iterrows():
            html += f'''<tr>
<td>{row["nombre"]}</td>
<td>{row["dia"]}</td>
<td>{row["hora"]}</td>
</tr>'''
        html += '''</tbody>
</table>
</div>'''
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay asistencia registrada hoy.")
with tab_gest:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_manage.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Gestionar Clientes")
    
    df_clientes = get_clientes()
    if not df_clientes.empty:
        df_clientes = df_clientes[df_clientes['plan_actual'].isin(['Semana', 'Quincena', 'Mensual'])]
        
    if df_clientes.empty:
        st.info("No hay clientes con planes de Semana, Quincena o Mensual para gestionar.")
    else:
        nombres_clientes = sorted(df_clientes['nombre'].tolist())
        cliente_sel = st.selectbox("Seleccionar Cliente para Editar", nombres_clientes)
        
        cliente_info = df_clientes[df_clientes['nombre'] == cliente_sel].iloc[0]
        
        with st.form("edit_cliente_form"):
            nuevo_nombre = st.text_input("Nombre", value=cliente_info['nombre'])
            nuevo_telefono = st.text_input("Teléfono (10 dígitos)", value=telefono_para_mostrar(cliente_info['telefono']), max_chars=10, placeholder="3001234567")
            nuevo_vencimiento = st.date_input("Fecha de Vencimiento", value=pd.to_datetime(cliente_info['fecha_vencimiento']).date())
            
            planes = ["Rutina", "Semana", "Quincena", "Mensual"]
            plan_actual = cliente_info['plan_actual']
            def_idx = planes.index(plan_actual) if plan_actual in planes else 0
            nuevo_plan = st.selectbox("Plan Actual", planes, index=def_idx)
            
            submit_edit = st.form_submit_button("GUARDAR CAMBIOS")
            
            if submit_edit:
                if nuevo_nombre:
                    telefono_norm = telefono_para_guardar(nuevo_telefono)
                    if nuevo_telefono and len(telefono_norm) != 12:
                        st.error("El teléfono debe tener 10 dígitos.")
                    else:
                        json_data = {
                            "nombre": nuevo_nombre,
                            "telefono": telefono_norm,
                            "fecha_vencimiento": str(nuevo_vencimiento),
                            "plan_actual": nuevo_plan
                        }
                        supabase_request("PATCH", "clientes", params={"id": f"eq.{int(cliente_info['id'])}"}, json_data=json_data)
                        st.success(f"¡Datos de {nuevo_nombre} actualizados!")
                        st.rerun()
                else:
                    st.error("El nombre no puede estar vacío.")
        
        st.markdown("---")
        st.subheader("Eliminar Cliente")
        
        with st.form("delete_cliente_form"):
            st.warning("⚠️ Esta acción quitará al cliente de las listas pero conservará su historial de pagos.")
            novedad = st.text_area("Novedad / Motivo del retiro", placeholder="Ej: Se retiró al día siguiente. Se le cobró solo el día.")
            
            # Buscar el último pago del cliente
            params = {
                "cliente_id": f"eq.{int(cliente_info['id'])}",
                "select": "id,monto,notas",
                "order": "id.desc",
                "limit": "1"
            }
            pagos = supabase_request("GET", "pagos", params=params)
            ultimo_pago = [pagos[0]['id'], pagos[0]['monto'], pagos[0]['notas']] if pagos else None
            
            monto_actual = ultimo_pago[1] if ultimo_pago else 0.0
            pago_id = ultimo_pago[0] if ultimo_pago else None
            
            nuevo_monto = st.number_input("Monto final a cobrar (ajustar si aplica devolución)", value=float(monto_actual))
            
            submit_delete = st.form_submit_button("ELIMINAR CLIENTE Y AJUSTAR PAGO")
            
            if submit_delete:
                # 1. Marcar cliente como borrado
                supabase_request("PATCH", "clientes", params={"id": f"eq.{int(cliente_info['id'])}"}, json_data={"borrado": True})
                
                # 2. Actualizar el pago si existe
                if pago_id:
                    supabase_request("PATCH", "pagos", params={"id": f"eq.{int(pago_id)}"}, json_data={"monto": nuevo_monto, "notas": novedad})
                st.success(f"¡Cliente {cliente_info['nombre']} eliminado y pago ajustado!")
                st.rerun()

with tab_hist:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_history.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Historial de Pagos")
    params = {
        "select": "fecha,monto,plan_tipo,metodo_pago,con_entrenadora,clientes!inner(nombre)",
        "order": "fecha.desc"
    }
    data = supabase_request("GET", "pagos", params=params)
    if data:
        formatted = []
        for r in data:
            formatted.append({
                "fecha": r["fecha"],
                "nombre": r["clientes"]["nombre"],
                "monto": r["monto"],
                "plan_tipo": r["plan_tipo"],
                "metodo_pago": r["metodo_pago"],
                "con_entrenadora": r["con_entrenadora"]
            })
        df_pagos = pd.DataFrame(formatted)
    else:
        df_pagos = pd.DataFrame(columns=['fecha', 'nombre', 'monto', 'plan_tipo', 'metodo_pago', 'con_entrenadora'])
    
    if not df_pagos.empty:
        df_pagos['con_entrenadora'] = df_pagos['con_entrenadora'].apply(lambda x: "Sí" if x else "No")
        
        # Agrupar por mes y año
        df_pagos['datetime'] = pd.to_datetime(df_pagos['fecha'])
        df_pagos['ano'] = df_pagos['datetime'].dt.year
        df_pagos['mes'] = df_pagos['datetime'].dt.month
        
        meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        grupos = df_pagos.groupby(['ano', 'mes'], sort=False)
        
        for (ano, mes), group in grupos:
            nombre_mes = meses_es[mes-1]
            # Solo el mes actual empieza abierto
            esta_abierto = bool(ano == datetime.date.today().year and mes == datetime.date.today().month)
            
            with st.expander(f"Mes: {nombre_mes} {ano}", expanded=esta_abierto):
                html = """<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Fecha</th>
<th>Cliente</th>
<th>Monto</th>
<th>Plan</th>
<th>Método</th>
<th>Entrenadora</th>
</tr>
</thead>
<tbody>"""
                for index, row in group.iterrows():
                    html += f"""<tr>
<td>{row["fecha"]}</td>
<td>{row["nombre"]}</td>
<td>${format(int(row["monto"]), ",")}</td>
<td>{row["plan_tipo"]}</td>
<td>{row["metodo_pago"]}</td>
<td>{row["con_entrenadora"]}</td>
</tr>"""
                html += """</tbody>
</table>
</div>"""
                st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay historial de pagos.")

with tab_asist_hist:
    st.markdown(f'<div class="tab-icon-header"><img src="data:image/png;base64,{get_base64("icon_attendance_history.png")}" width="60"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Historial de Asistencia")
    params = {
        "select": "fecha,clientes!inner(nombre)",
        "order": "fecha.desc"
    }
    data = supabase_request("GET", "asistencia", params=params)
    if data:
        formatted = []
        for r in data:
            formatted.append({
                "nombre": r["clientes"]["nombre"],
                "datetime_str": r["fecha"]
            })
        df_asist_full = pd.DataFrame(formatted)
    else:
        df_asist_full = pd.DataFrame(columns=['nombre', 'datetime_str'])
    
    if not df_asist_full.empty:
        df_asist_full['datetime'] = pd.to_datetime(df_asist_full['datetime_str'])
        df_asist_full['dia'] = df_asist_full['datetime'].dt.strftime('%d/%m/%Y')
        df_asist_full['hora'] = df_asist_full['datetime'].dt.strftime('%H:%M:%S')
        df_asist_full['ano'] = df_asist_full['datetime'].dt.year
        df_asist_full['mes'] = df_asist_full['datetime'].dt.month
        
        meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        grupos = df_asist_full.groupby(['ano', 'mes'], sort=False)
        
        for (ano, mes), group in grupos:
            nombre_mes = meses_es[mes-1]
            esta_abierto = bool(ano == datetime.date.today().year and mes == datetime.date.today().month)
            
            with st.expander(f"Mes: {nombre_mes} {ano}", expanded=esta_abierto):
                html = """<div class="custom-table-container">
<table class="custom-table">
<thead>
<tr>
<th>Nombre</th>
<th>Día</th>
<th>Hora</th>
</tr>
</thead>
<tbody>"""
                for index, row in group.iterrows():
                    html += f"""<tr>
<td>{row["nombre"]}</td>
<td>{row["dia"]}</td>
<td>{row["hora"]}</td>
</tr>"""
                html += """</tbody>
</table>
</div>"""
                st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No hay historial de asistencia.")

# Tab de Configuración (Solo para Super Admin)
if st.session_state.user_role == 'super_admin':
    with tab_config:
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <div style="font-size: 24px; font-weight: 700; color: #FFB300;">Gestión de Usuarios</div>
            <div style="color: #8A99AD;">Crea nuevos usuarios para el sistema</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("create_user_form"):
            nuevo_user = st.text_input("Nombre de Usuario")
            nueva_clave = st.text_input("Contraseña", type="password")
            rol_sel = st.selectbox("Rol", ["admin", "super_admin"])
            submit_u = st.form_submit_button("CREAR USUARIO")
            
            if submit_u:
                if nuevo_user and nueva_clave:
                    hashed_c = hash_password(nueva_clave)
                    user_data = {
                        "username": nuevo_user,
                        "password": hashed_c,
                        "rol": rol_sel
                    }
                    res = supabase_request("POST", "usuarios", json_data=user_data)
                    if res:
                        st.success(f"¡Usuario {nuevo_user} creado con éxito!")
                    else:
                        st.error("Error al crear usuario (puede que ya exista).")
                else:
                    st.error("Todos los campos son obligatorios.")
                    
        st.markdown("---")
        st.subheader("Usuarios Existentes")
        usuarios = supabase_request("GET", "usuarios", params={"select": "username,rol"})
        if usuarios:
            df_users = pd.DataFrame(usuarios)
            st.dataframe(df_users, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Gestión de Tarifas")
        tarifas = get_tarifas()
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("### Plan Normal")
            with st.form("tarifas_normal_form"):
                rutina_n = st.number_input("Rutina", value=float(tarifas["Normal"]["Rutina"]))
                semana_n = st.number_input("Semana", value=float(tarifas["Normal"]["Semana"]))
                quincena_n = st.number_input("Quincena", value=float(tarifas["Normal"]["Quincena"]))
                mensual_n = st.number_input("Mensual", value=float(tarifas["Normal"]["Mensual"]))
                submit_tn = st.form_submit_button("ACTUALIZAR NORMAL")
                
                if submit_tn:
                    for plan, monto in [("Rutina", rutina_n), ("Semana", semana_n), ("Quincena", quincena_n), ("Mensual", mensual_n)]:
                        supabase_request("PATCH", "tarifas", params={"categoria": "eq.Normal", "plan_tipo": f"eq.{plan}"}, json_data={"monto": monto})
                    st.success("¡Tarifas normales actualizadas!")
                    st.rerun()
                    
        with col_t2:
            st.markdown("### Con Entrenadora")
            with st.form("tarifas_entrenadora_form"):
                rutina_e = st.number_input("Rutina", value=float(tarifas["Con Entrenadora"]["Rutina"]))
                semana_e = st.number_input("Semana", value=float(tarifas["Con Entrenadora"]["Semana"]))
                quincena_e = st.number_input("Quincena", value=float(tarifas["Con Entrenadora"]["Quincena"]))
                mensual_e = st.number_input("Mensual", value=float(tarifas["Con Entrenadora"]["Mensual"]))
                submit_te = st.form_submit_button("ACTUALIZAR ENTRENADORA")
                
                if submit_te:
                    for plan, monto in [("Rutina", rutina_e), ("Semana", semana_e), ("Quincena", quincena_e), ("Mensual", mensual_e)]:
                        supabase_request("PATCH", "tarifas", params={"categoria": "eq.Con Entrenadora", "plan_tipo": f"eq.{plan}"}, json_data={"monto": monto})
                    st.success("¡Tarifas con entrenadora actualizadas!")
                    st.rerun()
