import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import requests

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
# Mengatur judul tab browser, layout wide (lebar), dan state sidebar
st.set_page_config(
    layout="wide",
    page_title="Smart Object Counter Pro",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DEFINISI TEMA (DATABASE TEMA)
# ==========================================
# Dictionary ini menyimpan konfigurasi warna, font, background, dan shadow.
# Urutan: Cyberpunk (Default/Pertama), sisanya diurutkan Abjad (A-Z).
THEMES = {
    # --- TEMA DEFAULT (Tetap Paling Atas) ---
    "🤖 Cyberpunk HUD": {
        "primary": "#00f2ff", "secondary": "#bc13fe", "bg_col": "#050a14", "text": "#e0f2fe",
        "card_bg": "rgba(16, 23, 41, 0.7)", "border": "rgba(0, 242, 255, 0.2)",
        "font_head": "Orbitron", "font_body": "Inter", "shadow": "0 0 20px rgba(0, 242, 255, 0.3)",
        "gradient": "linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px)"
    },

    # --- TEMA LAINNYA (URUTAN A-Z) ---
    "🦇 Batman": {
        "primary": "#fbbf24", "secondary": "#4b5563", "bg_col": "#0f172a", "text": "#9ca3af",
        "card_bg": "rgba(31, 41, 55, 0.9)", "border": "rgba(75, 85, 99, 0.6)",
        "font_head": "Russo One", "font_body": "Exo 2", "shadow": "0 0 15px rgba(0,0,0, 0.8)",
        "gradient": "repeating-linear-gradient(45deg, #111827 0, #111827 5px, #1f2937 5px, #1f2937 10px)"
    },
    "😽 Doraemon": {
        "primary": "#0ea5e9", "secondary": "#ef4444", "bg_col": "#ffffff", "text": "#0284c7",
        "card_bg": "rgba(255, 255, 255, 0.9)", "border": "rgba(14, 165, 233, 0.4)",
        "font_head": "Fredoka One", "font_body": "Varela Round", "shadow": "none",
        "gradient": "radial-gradient(circle, #ffffff 20%, #bae6fd 100%)"
    },
    "🔪 Friday 13th (Horror)": {
        "primary": "#dc2626", "secondary": "#78350f", "bg_col": "#000000", "text": "#d6d3d1",
        "card_bg": "rgba(20, 20, 20, 0.95)", "border": "rgba(153, 27, 27, 0.8)",
        "font_head": "Nosifer", "font_body": "Creepster", "shadow": "0 0 15px #dc2626",
        "gradient": "linear-gradient(to bottom, #000000 60%, #270303 100%)"
    },
    "🌌 Galactic Empire": {
        "primary": "#ffffff", "secondary": "#ef4444", "bg_col": "#000000", "text": "#ffffff",
        "card_bg": "rgba(30, 30, 30, 0.8)", "border": "rgba(255, 255, 255, 0.6)",
        "font_head": "Orbitron", "font_body": "Roboto", "shadow": "0 0 10px rgba(255,255,255,0.8)",
        "gradient": "repeating-linear-gradient(90deg, transparent 0, transparent 28px, rgba(255,255,255,0.1) 28px, rgba(255,255,255,0.1) 30px)"
    },
    "💻 Hacker Terminal": {
        "primary": "#00ff00", "secondary": "#008f11", "bg_col": "#0d0208", "text": "#00ff41",
        "card_bg": "rgba(0, 20, 0, 0.8)", "border": "rgba(0, 255, 0, 0.4)",
        "font_head": "VT323", "font_body": "Courier Prime", "shadow": "0 0 10px rgba(0, 255, 0, 0.4)",
        "gradient": "repeating-linear-gradient(0deg, rgba(0, 255, 0, 0.05) 0px, rgba(0, 255, 0, 0.05) 1px, transparent 1px, transparent 2px)"
    },
    "⚡ Harry Potter": {
        "primary": "#fbbf24", "secondary": "#7f1d1d", "bg_col": "#2a0a0a", "text": "#fef3c7",
        "card_bg": "rgba(69, 10, 10, 0.8)", "border": "rgba(251, 191, 36, 0.5)",
        "font_head": "Cinzel Decorative", "font_body": "Crimson Text", "shadow": "0 0 15px rgba(251, 191, 36, 0.4)",
        "gradient": "radial-gradient(circle, #450a0a 0%, #000000 100%)"
    },
    "🎀 Hello Kitty": {
        "primary": "#ec4899", "secondary": "#f43f5e", "bg_col": "#fff1f2", "text": "#881337",
        "card_bg": "rgba(255, 255, 255, 0.8)", "border": "rgba(244, 63, 94, 0.3)",
        "font_head": "Pacifico", "font_body": "Quicksand", "shadow": "none",
        "gradient": "radial-gradient(circle, #fff1f2 0%, #ffe4e6 100%)"
    },
    "🏎️ Hot Wheels": {
        "primary": "#f97316", "secondary": "#3b82f6", "bg_col": "#0f172a", "text": "#ffffff", 
        "card_bg": "rgba(2, 6, 23, 0.95)", 
        "border": "rgba(249, 115, 22, 0.9)",
        "font_head": "Racing Sans One", "font_body": "Roboto Condensed", "shadow": "skew(-10deg) 2px 2px 0px #000",
        "gradient": "repeating-linear-gradient(135deg, #000000 0px, #000000 40px, #ea580c 40px, #ea580c 60px, #2563eb 60px, #2563eb 80px)"
    },
    "🤡 Joker": {
        "primary": "#a855f7", "secondary": "#22c55e", "bg_col": "#2e1065", "text": "#f0fdf4",
        "card_bg": "rgba(88, 28, 135, 0.85)", "border": "rgba(34, 197, 94, 0.6)",
        "font_head": "Creepster", "font_body": "Space Mono", "shadow": "0 0 10px #22c55e",
        "gradient": "repeating-linear-gradient(75deg, transparent, transparent 10px, rgba(34, 197, 94, 0.1) 10px, rgba(34, 197, 94, 0.1) 20px), repeating-linear-gradient(15deg, transparent, transparent 20px, rgba(168, 85, 247, 0.1) 20px, rgba(168, 85, 247, 0.1) 30px)"
    },
    "⚔️ Military Ops": {
        "primary": "#f59e0b", "secondary": "#84cc16", "bg_col": "#1c1917", "text": "#a8a29e",
        "card_bg": "rgba(41, 37, 36, 0.9)", "border": "rgba(245, 158, 11, 0.3)",
        "font_head": "Black Ops One", "font_body": "Share Tech Mono", "shadow": "2px 2px 0px rgba(0,0,0,0.5)",
        "gradient": "repeating-linear-gradient(45deg, #292524 25%, transparent 25%, transparent 75%, #292524 75%, #292524), repeating-linear-gradient(45deg, #292524 25%, #1c1917 25%, #1c1917 75%, #292524 75%, #292524)"
    },
    "🌋 Molten Core": {
        "primary": "#fbbf24", "secondary": "#ef4444", "bg_col": "#2a0a0a", "text": "#ffffff", 
        "card_bg": "rgba(10, 0, 0, 0.95)", 
        "border": "rgba(245, 158, 11, 0.8)",
        "font_head": "Bangers", "font_body": "Oswald", "shadow": "0 0 15px rgba(239, 68, 68, 0.8)",
        "gradient": "linear-gradient(to bottom, #000000 0%, #450a0a 100%)"
    },
    "🕵️ Noir Detective": {
        "primary": "#e5e5e5", "secondary": "#737373", "bg_col": "#171717", "text": "#d4d4d4",
        "card_bg": "rgba(40, 40, 40, 0.9)", "border": "rgba(115, 115, 115, 0.5)",
        "font_head": "Special Elite", "font_body": "Courier Prime", "shadow": "none",
        "gradient": "repeating-linear-gradient(105deg, transparent, transparent 10px, rgba(0,0,0,0.5) 10px, rgba(0,0,0,0.5) 12px)"
    },
    "🌑 Obsidian Luxury": {
        "primary": "#fcd34d", "secondary": "#2dd4bf", "bg_col": "#000000", "text": "#f8fafc",
        "card_bg": "rgba(20, 20, 20, 0.9)", "border": "rgba(252, 211, 77, 0.4)",
        "font_head": "Cinzel", "font_body": "Lato", "shadow": "0 0 10px rgba(252, 211, 77, 0.3)",
        "gradient": "linear-gradient(135deg, #000000 0%, #1c1917 100%)"
    },
    "👑 Puro Mangkunegaran": {
        "primary": "#facc15", "secondary": "#15803d", "bg_col": "#052e16", "text": "#f0fdf4",
        "card_bg": "rgba(20, 83, 45, 0.95)", "border": "rgba(250, 204, 21, 0.7)",
        "font_head": "Cinzel Decorative", "font_body": "Playfair Display", "shadow": "0 2px 10px rgba(250, 204, 21, 0.5)",
        "gradient": "repeating-linear-gradient(45deg, #064e3b 0, #064e3b 10px, #14532d 10px, #14532d 20px), repeating-linear-gradient(-45deg, transparent 0, transparent 10px, rgba(250, 204, 21, 0.1) 10px, rgba(250, 204, 21, 0.1) 20px)"
    },
    "👾 Retro Arcade": {
        "primary": "#facc15", "secondary": "#ec4899", "bg_col": "#171717", "text": "#ffffff",
        "card_bg": "rgba(38, 38, 38, 0.9)", "border": "rgba(236, 72, 153, 0.6)",
        "font_head": "Press Start 2P", "font_body": "VT323", "shadow": "3px 3px 0px #ec4899",
        "gradient": "linear-gradient(90deg, #171717 0%, #262626 100%)"
    },
    "🕷️ Spider-Man": {
        "primary": "#ef4444", "secondary": "#3b82f6", 
        "bg_col": "#450a0a", 
        "sidebar_bg": "#172554", # Background khusus sidebar (Biru Celana Spiderman)
        "text": "#ffffff",
        "card_bg": "rgba(23, 37, 84, 0.9)", 
        "border": "rgba(239, 68, 68, 0.5)",
        "font_head": "Metal Mania", 
        "font_body": "Marvel",
        "shadow": "2px 2px 0px #000000",
        "gradient": "repeating-linear-gradient(45deg, #450a0a 0, #450a0a 5px, #7f1d1d 5px, #7f1d1d 10px)"
    },
    "🦸 Superman": {
        "primary": "#ef4444", "secondary": "#facc15", "bg_col": "#172554", "text": "#ffffff",
        "card_bg": "rgba(23, 37, 84, 0.9)", "border": "rgba(239, 68, 68, 0.7)",
        "font_head": "Black Ops One", "font_body": "Roboto", "shadow": "2px 2px 0px #facc15",
        "gradient": "repeating-linear-gradient(45deg, #172554 0, #172554 2px, #1e3a8a 2px, #1e3a8a 4px), repeating-linear-gradient(-45deg, #172554 0, #172554 2px, #1e3a8a 2px, #1e3a8a 4px)"
    },
    "🌅 Synthwave Sunset": {
        "primary": "#d946ef", "secondary": "#00e5ff", "bg_col": "#240046", "text": "#e0aaff",
        "card_bg": "rgba(60, 9, 108, 0.8)", "border": "rgba(255, 0, 255, 0.4)",
        "font_head": "Audiowide", "font_body": "Rajdhani", "shadow": "0 0 15px rgba(255, 0, 255, 0.5)",
        "gradient": "linear-gradient(to bottom, #020617 0%, #2e1065 100%), repeating-linear-gradient(0deg, transparent 0, transparent 49px, #d946ef 50px), repeating-linear-gradient(90deg, transparent 0, transparent 49px, #d946ef 50px)"
    },
    "☢️ Toxic Wasteland": {
        "primary": "#a3e635", "secondary": "#a855f7", "bg_col": "#1a1c10", "text": "#ecfccb",
        "card_bg": "rgba(26, 28, 16, 0.9)", "border": "rgba(163, 230, 53, 0.7)",
        "font_head": "Creepster", "font_body": "Space Mono", "shadow": "0 0 15px #a3e635",
        "gradient": "radial-gradient(circle at 50% 50%, rgba(163, 230, 53, 0.1) 10%, transparent 10%), radial-gradient(circle at 0% 0%, rgba(163, 230, 53, 0.1) 10%, transparent 10%)"
    }
}

# ==========================================
# 3. MANAJEMEN SESSION STATE
# ==========================================
# Memastikan tema tersimpan meski halaman direfresh atau ada interaksi
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "🤖 Cyberpunk HUD"

# ==========================================
# 4. FUNGSI INJEKSI CSS (STYLING DINAMIS)
# ==========================================
def inject_css(theme_name):
    t = THEMES[theme_name]
    
    # Logika khusus untuk ukuran background (hanya untuk tema tertentu agar tekstur pas)
    bg_size = "30px 30px"
    if theme_name == "☢️ Toxic Wasteland":
        bg_size = "40px 40px"
    if theme_name == "🌅 Synthwave Sunset":
        bg_size = "100% 100%, 50px 50px, 50px 50px"
    
    # Logika Warna Sidebar: Jika tema punya 'sidebar_bg', pakai itu. Jika tidak, pakai warna 'bg_col'.
    sidebar_bg = t.get('sidebar_bg', t['bg_col'])
        
    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
    /* Mengimpor Font dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@400;600&family=Inter:wght@300;400;600&family=VT323&family=Courier+Prime&family=Cinzel:wght@500&family=Cinzel+Decorative&family=Playfair+Display&family=Audiowide&family=Rajdhani:wght@500&family=Black+Ops+One&family=Share+Tech+Mono&family=Russo+One&family=Roboto+Condensed&family=Michroma&family=Montserrat&family=Teko:wght@500&family=Oswald&family=Exo+2:wght@600&family=Lato&family=Righteous&family=Quicksand:wght@500&family=Creepster&family=Crimson+Text&family=Nunito&family=Iceland&family=Roboto&family=Bangers&family=Space+Mono&family=Press+Start+2P&family=Pacifico&family=Special+Elite&family=Alice&family=Racing+Sans+One&family=Rye&family=Nosifer&family=Dancing+Script&family=Merriweather&family=Varela+Round&family=Fredoka+One&family=Metal+Mania&family=Marvel&display=swap');

    /* Mengatur Gaya Halaman Utama */
    .stApp {{
        background-color: {t['bg_col']};
        background-image: {t['gradient']};
        background-size: {bg_size};
        background-position: center;
        background-attachment: fixed; 
        color: {t['text']};
        font-family: '{t['font_body']}', sans-serif;
    }}
    
    /* Memaksa warna label widget agar sesuai tema */
    .stMarkdown, .stText, p, label, .stWidgetLabel {{
        color: {t['text']} !important;
    }}

    /* Mengatur Gaya Header (Judul) */
    h1, h2, h3 {{
        font-family: '{t['font_head']}', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(90deg, {t['primary']}, {t['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: {t['shadow']};
    }}
    
    /* Mengatur Sub-header */
    h4, h5, h6 {{
        color: {t['text']} !important;
        opacity: 0.9;
        font-family: '{t['font_head']}', sans-serif !important;
    }}

    /* Mengatur Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {t['border']};
    }}
    
    /* Kartu HUD (Kotak Kontainer) */
    .hud-card {{
        background: {t['card_bg']};
        border: 1px solid {t['border']};
        box-shadow: 0 0 15px rgba(0,0,0, 0.05);
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }}
    
    .hud-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(to bottom, {t['primary']}, {t['secondary']});
    }}

    /* Gaya Teks Berjalan (Marquee) */
    .marquee-container {{
        width: 100%;
        background: {t['card_bg']};
        border: 1px solid {t['border']};
        border-radius: 4px;
        overflow: hidden;
        white-space: nowrap;
        margin-bottom: 30px;
        padding: 10px 0;
        position: relative;
    }}

    .marquee-container::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(to bottom, {t['primary']}, {t['secondary']});
        z-index: 2;
    }}

    .marquee-text {{
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
        font-family: '{t['font_head']}', sans-serif;
        color: {t['primary']};
        font-size: 0.9rem;
        letter-spacing: 2px;
    }}

    .marquee-text i {{
        margin: 0 15px;
        color: {t['secondary']};
    }}

    @keyframes marquee {{
        0%   {{ transform: translate(0, 0); }}
        100% {{ transform: translate(-100%, 0); }}
    }}

    /* Gaya Angka Statistik */
    .digital-val {{
        font-family: '{t['font_head']}', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: {t['text']};
    }}
    
    .digital-label {{
        font-size: 0.8rem;
        color: {t['text']};
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Kotak Info Citra */
    .info-monitor {{
        background: rgba(125,125,125, 0.1);
        border: 1px solid {t['primary']};
        border-radius: 4px;
        padding: 15px;
        color: {t['text']};
        font-family: '{t['font_body']}', monospace;
        font-size: 0.9rem;
    }}

    /* Kotak Area Statistik */
    .area-monitor {{
        background: {t['card_bg']};
        border: 1px dashed {t['secondary']};
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s;
    }}
    .area-monitor:hover {{
        transform: translateY(-5px);
        border-color: {t['primary']};
    }}
    .area-icon {{
        font-size: 1.2rem;
        color: {t['primary']};
        margin-bottom: 5px;
    }}

    /* Gaya Tombol */
    div[data-testid="stButton"] button {{
        background: transparent;
        color: {t['primary']};
        border: 1px solid {t['primary']};
        border-radius: 4px;
        font-family: '{t['font_head']}', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
        width: 100%;
    }}
    div[data-testid="stButton"] button:hover {{
        background: {t['primary']};
        color: {t['bg_col']}; /* Contrast Text on Hover */
        box-shadow: 0 0 15px {t['primary']};
    }}

    /* Gaya Tab */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 5px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(125,125,125,0.1);
        color: {t['text']};
        border: 1px solid transparent;
        border-radius: 0px;
        font-family: '{t['font_head']}', sans-serif;
        font-size: 0.8rem;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: rgba(125,125,125, 0.2) !important;
        color: {t['primary']} !important;
        border: 1px solid {t['primary']} !important;
    }}
    
    /* Gaya Expander (Dropdown Info) */
    .streamlit-expanderHeader {{
        background-color: {t['card_bg']};
        color: {t['primary']} !important;
        font-family: '{t['font_head']}', sans-serif;
        border: 1px solid {t['border']};
    }}
    
    /* Gaya Pop-up Dialog */
    div[role="dialog"] {{
        background: {t['bg_col']} !important;
        border: 1px solid {t['primary']} !important;
        box-shadow: 0 0 50px {t['border']} !important;
    }}
    
    /* Fix warna teks di inputan sidebar */
    .stSelectbox label, .stSlider label {{
        color: {t['text']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. KONTROL SIDEBAR (INPUT & PARAMETER)
# ==========================================
if "selected_theme_name" not in st.session_state:
    st.session_state.selected_theme_name = "🤖 Cyberpunk HUD"

current_t = THEMES[st.session_state.selected_theme_name] 

# Judul Sidebar
st.sidebar.markdown(f"<h3 style='text-align:center; color:{current_t['primary']}'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)

# Dropdown Pemilihan Tema
selected_theme = st.sidebar.selectbox("🎨 PILIH TEMA TAMPILAN", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.selected_theme_name))

# Update tema jika berubah
if selected_theme != st.session_state.selected_theme_name:
    st.session_state.selected_theme_name = selected_theme
    st.rerun()

# Terapkan CSS tema terpilih
inject_css(st.session_state.selected_theme_name)
current_t = THEMES[st.session_state.selected_theme_name] 

st.sidebar.markdown("---")
st.sidebar.info("💡 **TIPS:** Gunakan gambar dengan kontras tinggi untuk akurasi maksimal.")
st.sidebar.markdown(f"<p style='font-family:{current_t['font_head']}; color:{current_t['primary']};'><i class='fas fa-sliders-h'></i> PARAMETER DETEKSI</p>", unsafe_allow_html=True)

# Slider Parameter
blur_value = st.sidebar.slider("Tingkat Denoise (Blur)", 1, 15, 9, step=2)
threshold_value = st.sidebar.slider("Sensitivitas Threshold", 0, 255, 142)
min_area = st.sidebar.slider("Area Objek Min (px)", 10, 2000, 894)

# ==========================================
# 6. FUNGSI PEMROSESAN GAMBAR (CORE LOGIC)
# ==========================================
def hex_to_rgb(hex_color):
    """Mengubah kode warna HEX ke Tuple RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@st.cache_data
def process_image(file_content, blur_val, thresh_val, min_a, theme_color_hex):
    # Membaca gambar dari bytes
    file_bytes = np.asarray(bytearray(file_content), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    # Konversi BGR (OpenCV) ke RGB (Tampilan Web)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    theme_rgb = hex_to_rgb(theme_color_hex)
    
    # 1. Grayscale (Hitam Putih)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur (Menghaluskan noise)
    blurred = cv2.GaussianBlur(gray, (blur_val, blur_val), 0)
    
    # 3. Thresholding (Memisahkan objek dari background)
    _, thresh = cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY_INV)
    
    # 4. Morphology (Membersihkan bintik-bintik kecil)
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 5. Mencari Kontur Objek
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = [] 
    object_data = []    
    
    # Filter kontur berdasarkan luas area
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt) 
        if area > min_a:
            valid_contours.append(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0: circularity = 0
            else: circularity = 4 * np.pi * (area / (perimeter * perimeter))
            x, y, w, h = cv2.boundingRect(cnt)
            M = cv2.moments(cnt)
            if M["m00"] != 0: cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            else: cx, cy = 0, 0
            
            object_data.append({
                "Area (px²)": int(area),
                "Circularity": round(circularity, 3),
                "Posisi X": cx, "Posisi Y": cy,
                "Lebar": w, "Tinggi": h
            })
            
    # Menggambar hasil pada gambar duplikat
    result_img = img_rgb.copy()
    for idx, cnt in enumerate(valid_contours):
        # A. Gambar Kotak (Bounding Box) sesuai warna tema
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(result_img, (x, y), (x + w, y + h), theme_rgb, 2)
        
        # B. Gambar Kontur Asli (Outline Merah)
        cv2.drawContours(result_img, [cnt], -1, (255, 0, 0), 1)
        
        # C. Tulis Nomor ID (Stroke Hitam + Isi Kuning)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.putText(result_img, str(idx+1), (cx-10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 4)
            cv2.putText(result_img, str(idx+1), (cx-10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    return img_rgb, result_img, object_data, morph, gray, blurred, thresh

# Fungsi Konversi Gambar ke Bytes (untuk Download)
def convert_to_bytes(img_array, is_gray=False):
    if is_gray: img_encode = img_array
    else: img_encode = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    is_success, im_buf_arr = cv2.imencode(".png", img_encode)
    return im_buf_arr.tobytes()

# Fungsi Konversi Dataframe ke Excel
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Deteksi')
    return output.getvalue()

# ==========================================
# 7. POP-UP DIALOG DOWNLOAD
# ==========================================
@st.dialog("💾 DOWNLOAD SISTEM")
def interactive_download_popup(img_gray, img_blur, img_mask, img_result, img_thresh):
    if "dl_step" not in st.session_state: st.session_state.dl_step = "pilihan"
    if "selected_opt" not in st.session_state: st.session_state.selected_opt = None

    def go_to_validation():
        st.session_state.selected_opt = st.session_state.temp_choice
        st.session_state.dl_step = "validasi"

    if st.session_state.dl_step == "pilihan":
        st.markdown(f"<p style='text-align:center; color:{current_t['primary']};'><i class='fas fa-file-export'></i> PILIH FORMAT OUTPUT</p>", unsafe_allow_html=True)
        st.radio("Opsi:", ["Hasil Preprocessing (Gray, Blur, Thresh)", "Hasil Morfologi (Clean Mask)", 
                           "Hasil Akhir (Deteksi)", "Download Semua Gambar"], 
                 index=None, key="temp_choice", on_change=go_to_validation, label_visibility="collapsed")

    elif st.session_state.dl_step == "validasi":
        choice = st.session_state.selected_opt
        is_multi = (choice == "Hasil Preprocessing (Gray, Blur, Thresh)" or choice == "Download Semua Gambar")
        
        st.markdown(f"""
            <div style='background:rgba(255,255,255,0.05); padding:15px; border-left:3px solid {current_t['secondary']};'>
                <p style='color:{current_t['secondary']}; margin:0; font-size:0.8rem;'><i class='fas fa-exclamation-triangle'></i> KONFIRMASI AKSI</p>
                <h4 style='color:{current_t['text']}; margin:5px 0;'>{choice}</h4>
            </div><br>
        """, unsafe_allow_html=True)

        if not is_multi:
            if choice == "Hasil Morfologi (Clean Mask)":
                data, name = convert_to_bytes(img_mask, True), "morphology_mask.png"
            else:
                data, name = convert_to_bytes(img_result, False), "result.png"
            
            c1, c2 = st.columns(2)
            c1.download_button("✅ UNDUH", data, name, "image/png", use_container_width=True)
            if c2.button("❌ BATAL", use_container_width=True):
                st.session_state.dl_step = "pilihan"
                if "temp_choice" in st.session_state:
                    del st.session_state.temp_choice
                st.rerun()
        else:
            st.info("File tersedia di bawah ini:")
            if choice == "Hasil Preprocessing (Gray, Blur, Thresh)" or choice == "Download Semua Gambar":
                c_a, c_b, c_c = st.columns(3)
                c_a.download_button("⬇️ Grayscale", convert_to_bytes(img_gray, True), "gray.png", "image/png", use_container_width=True)
                c_b.download_button("⬇️ Blur", convert_to_bytes(img_blur, True), "blur.png", "image/png", use_container_width=True)
                c_c.download_button("⬇️ Threshold", convert_to_bytes(img_thresh, True), "threshold_raw.png", "image/png", use_container_width=True)
            
            if choice == "Download Semua Gambar":
                c_d, c_e = st.columns(2)
                c_d.download_button("⬇️ Morfologi", convert_to_bytes(img_mask, True), "morph_mask.png", "image/png", use_container_width=True)
                c_e.download_button("⬇️ Hasil", convert_to_bytes(img_result, False), "result.png", "image/png", use_container_width=True)
            
            st.markdown("---")
            if st.button("❌ TUTUP", use_container_width=True):
                 st.session_state.dl_step = "pilihan"
                 if "temp_choice" in st.session_state:
                    del st.session_state.temp_choice
                 st.rerun()

@st.dialog("📊 EKSPOR DATA")
def excel_download_popup(df):
    st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); padding:15px; border-left:3px solid {current_t['primary']};'>
            <p style='color:{current_t['primary']}; margin:0; font-size:0.8rem;'><i class='fas fa-file-excel'></i> FORMAT EKSPOR</p>
            <h4 style='color:{current_t['text']}; margin:5px 0;'>Microsoft Excel (.xlsx)</h4>
        </div><br>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.download_button("✅ UNDUH", convert_df_to_excel(df), "data_deteksi.xlsx", 
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    if c2.button("❌ BATAL", use_container_width=True): st.rerun()

# ==========================================
# 8. TAMPILAN UTAMA (LAYOUT)
# ==========================================
st.markdown(f"<h1 style='text-align: center;'>SMART OBJECT COUNTER <span style='font-size:1.5rem; color:{current_t['primary']}; vertical-align: super;'>PRO</span></h1>", unsafe_allow_html=True)

# Teks Berjalan (Marquee)
st.markdown(f"""
    <div class="marquee-container">
        <div class="marquee-text">
            <i class="fas fa-robot"></i> SELAMAT DATANG DI SMART OBJECT COUNTER PRO 
            <i class="fas fa-minus"></i> APLIKASI IMAGE PROCESSING BERBASIS STREAMLIT
            <i class="fas fa-minus"></i> TEMA SAAT INI: {st.session_state.selected_theme_name}
            <i class="fas fa-minus"></i> SILAKAN UNGGAH GAMBAR UNTUK MEMULAI DETEKSI OBJEK OTOMATIS 
            <i class="fas fa-check-circle"></i> SISTEM SIAP DIGUNAKAN
        </div>
    </div>
""", unsafe_allow_html=True)

# Pilihan Input (Radio Button)
input_method = st.radio(
    "👉 Pilih Sumber Gambar:", 
    ("📂 Unggah Gambar Sendiri", "🧪 Gunakan Gambar Contoh (Demo)"), 
    horizontal=True
)

file_bytes_content = None
file_extension = ""

if input_method == "🧪 Gunakan Gambar Contoh (Demo)":
    demo_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/smarties.png"
    try:
        response = requests.get(demo_url)
        if response.status_code == 200:
            file_bytes_content = response.content
            file_extension = "PNG"
            st.success("✅ Gambar contoh berhasil dimuat! Silakan lihat hasilnya di bawah.")
        else:
            st.error("Gagal memuat gambar contoh. Periksa koneksi internet Anda.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    uploaded_file = st.file_uploader("Upload Gambar disini", type=["jpg", "png", "jpeg", "bmp", "webp"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_bytes_content = uploaded_file.getvalue()
        file_extension = uploaded_file.name.split('.')[-1].upper()

# Info Aplikasi (Expander)
with st.expander("ℹ️ TENTANG APLIKASI & PANDUAN PENGGUNAAN (KLIK UNTUK BACA)", expanded=False):
    st.markdown(f"""
    <div class="hud-card" style="text-align: left; margin-bottom: 15px;">
        <h4 style="color: {current_t['primary']}; margin-bottom: 10px;">📖 DESKRIPSI SISTEM</h4>
        <p style="color: {current_t['text']}; font-size: 0.9rem; line-height: 1.6;">
            <b>Smart Object Counter Pro</b> adalah sistem visi komputer canggih untuk penghitungan otomatis objek mikroskopis dan komponen kecil.
            Sistem ini mengeliminasi kesalahan manusia (human error) dalam proses quality control dan inventarisasi dengan akurasi tinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_info1, c_info2 = st.columns(2)

    with c_info1:
        st.markdown(f"""
        <div class="hud-card" style="height: 100%; text-align: left;">
            <h5 style="color: {current_t['secondary']}; border-bottom: 1px solid {current_t['secondary']}; padding-bottom: 5px;">⚙️ ARSITEKTUR TEKNIS</h5>
            <ul style="color: {current_t['text']}; font-size: 0.85rem; list-style: none; padding-left: 0; line-height: 1.8;">
                <li><i class="fas fa-code-branch" style="color:{current_t['secondary']}; width:20px;"></i> <b>GRAYSCALE:</b> Konversi spektrum warna.</li>
                <li><i class="fas fa-tint" style="color:{current_t['secondary']}; width:20px;"></i> <b>GAUSSIAN BLUR:</b> Reduksi noise frekuensi tinggi.</li>
                <li><i class="fas fa-adjust" style="color:{current_t['secondary']}; width:20px;"></i> <b>THRESHOLDING:</b> Segmentasi biner adaptif.</li>
                <li><i class="fas fa-filter" style="color:{current_t['secondary']}; width:20px;"></i> <b>MORFOLOGI:</b> Opening/Closing struktur.</li>
                <li><i class="fas fa-vector-square" style="color:{current_t['secondary']}; width:20px;"></i> <b>CONTOUR:</b> Ekstraksi topologi objek.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_info2:
        st.markdown(f"""
        <div class="hud-card" style="height: 100%; text-align: left;">
            <h5 style="color: {current_t['primary']}; border-bottom: 1px solid {current_t['primary']}; padding-bottom: 5px;">🚀 PROTOKOL OPERASIONAL</h5>
            <ol style="color: {current_t['text']}; font-size: 0.85rem; padding-left: 20px; line-height: 1.6;">
                <li>Pilih mode: <b>Unggah Gambar</b> atau <b>Gambar Contoh</b>.</li>
                <li>Tunggu proses <b>Analisis AI</b> selesai.</li>
                <li>Lakukan kalibrasi manual pada <b>SIDEBAR</b> jika perlu:
                    <ul style="color: {current_t['text']}; opacity: 0.7; margin-top:5px; list-style: circle;">
                        <li><i>Denoise</i> untuk kejernihan.</li>
                        <li><i>Threshold</i> untuk sensitivitas.</li>
                    </ul>
                </li>
                <li>Ekspor data hasil deteksi via tombol <b>EKSPOR</b> pada bagian bawah aplikasi.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. EKSEKUSI PEMROSESAN GAMBAR
# ==========================================
if file_bytes_content is not None:
    # Menjalankan fungsi process_image
    original, result, data_list, mask, gray_img, blurred_img, thresh_raw = process_image(
        file_bytes_content, blur_value, threshold_value, min_area, current_t['primary']
    )
    h, w, c = original.shape
    
    if data_list:
        # Membuat Dataframe dari hasil deteksi
        df = pd.DataFrame(data_list)
        low, high = df["Area (px²)"].quantile(0.33), df["Area (px²)"].quantile(0.66)
        df["Jenis"] = df["Area (px²)"].apply(lambda x: "Kecil" if x < low else ("Sedang" if x < high else "Besar"))
        
        df["No"] = range(1, len(df) + 1)
        df = df[["No", "Jenis", "Area (px²)", "Circularity", "Posisi X", "Posisi Y", "Lebar", "Tinggi"]]
        counts = df["Jenis"].value_counts()
        
        # --- DASHBOARD STATISTIK ---
        st.markdown(f"### <i class='fas fa-satellite-dish'></i> HASIL DETEKSI", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        
        def render_hud_stat(col, label, value, icon_class, color):
            col.markdown(f"""
                <div class="hud-card" style="text-align:center; padding: 15px;">
                    <div class="hud-icon" style="color:{color}"><i class="{icon_class}"></i></div>
                    <div class="digital-val" style="color:{color}">{value}</div>
                    <div class="digital-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Menampilkan Kartu Statistik
        render_hud_stat(c1, "TOTAL TERDETEKSI", len(df), "fas fa-layer-group", current_t['text'])
        render_hud_stat(c2, "OBJEK KECIL", counts.get("Kecil", 0), "fas fa-compress-arrows-alt", current_t['primary'])
        render_hud_stat(c3, "OBJEK SEDANG", counts.get("Sedang", 0), "fas fa-expand", current_t['secondary'])
        render_hud_stat(c4, "OBJEK BESAR", counts.get("Besar", 0), "fas fa-expand-arrows-alt", "#000000" if "Clean" in st.session_state.selected_theme_name or "Blue Cat" in st.session_state.selected_theme_name or "Cute Kitty" in st.session_state.selected_theme_name or "Luxury" in st.session_state.selected_theme_name else "#ffffff")

        # --- TABS VISUALISASI ---
        tab1, tab2, tab3 = st.tabs(["👁️ VISUALISASI", "📈 ANALISIS", "💾 DATA MENTAH"])
        
        # TAB 1: GAMBAR HASIL
        with tab1:
            st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
            with st.expander("🔻 DETAIL ALUR PREPROCESSING (KLIK UNTUK BUKA/TUTUP)", expanded=True):
                st.markdown(f"<p style='font-family:{current_t['font_head']}; color:{current_t['text']}; font-size:0.9rem'>// <i class='fas fa-microchip'></i> TAHAPAN PROSES AWAL</p>", unsafe_allow_html=True)
                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                col_p1.image(original, caption="1. INPUT ASLI", use_container_width=True)
                col_p2.image(gray_img, caption="2. GRAYSACALE", use_container_width=True)
                col_p3.image(blurred_img, caption="3. GAUSSIAN BLUR", use_container_width=True)
                col_p4.image(thresh_raw, caption="4. THRESHOLD (RAW)", use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"<p style='font-family:{current_t['font_head']}; color:{current_t['text']}; font-size:0.9rem'>// <i class='fas fa-bullseye'></i> HASIL PEMROSESAN AKHIR</p>", unsafe_allow_html=True)
            col_r1, col_r2 = st.columns(2)
            col_r1.image(mask, caption="5. HASIL MORFOLOGI (CLEAN MASK)", use_container_width=True)
            col_r2.image(result, caption="6. OUTPUT AKHIR (BOUNDING BOX + CONTOUR)", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # TAB 2: GRAFIK
        with tab2:
            st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            
            graph_colors = [current_t['primary'], current_t['secondary'], '#94a3b8']
            
            # Pie Chart
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            fig1.patch.set_alpha(0)
            dist_data = counts.reset_index()
            dist_data.columns = ["Kategori", "Jumlah"]
            
            wedges, texts, autotexts = ax1.pie(dist_data["Jumlah"], labels=dist_data["Kategori"], 
                                             autopct='%1.1f%%', startangle=90, colors=graph_colors,
                                             textprops={'color': current_t['text'], 'fontsize': 10, 'fontweight': 'bold'})
            plt.setp(autotexts, size=12, weight="bold", color="black")
            g1.pyplot(fig1, use_container_width=True)
            
            # Bar Chart
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_alpha(0)
            ax2.set_facecolor("none")
            bars = ax2.bar(dist_data["Kategori"], dist_data["Jumlah"], color=graph_colors, edgecolor=current_t['text'], alpha=0.8)
            ax2.tick_params(colors=current_t['text'])
            
            for spine in ax2.spines.values(): spine.set_edgecolor(current_t['text'])
                
            ax2.grid(axis='y', linestyle='--', alpha=0.2, color=current_t['primary'])
            g2.pyplot(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # TAB 3: DATAFRAME
        with tab3:
            st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=400, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # --- INFO CITRA & AREA STATS ---
        st.markdown("---")
        col_bottom_1, col_bottom_2 = st.columns([1, 2])
        
        with col_bottom_1:
            st.markdown("### <i class='fas fa-info-circle'></i> INFO CITRA", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="info-monitor">
                    <div><i class="fas fa-ruler-combined"></i> DIMENSI : {w} x {h} px</div>
                    <div><i class="fas fa-file-image"></i> FORMAT  : {file_extension}</div>
                    <div><i class="fas fa-border-all"></i> PIXELS  : {w*h:,} px</div>
                    <div><i class="fas fa-wifi"></i> STATUS  : <span style="color:{current_t['primary']}">ONLINE</span></div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_bottom_2:
            st.markdown("### <i class='fas fa-chart-bar'></i> RINGKASAN STATISTIK AREA", unsafe_allow_html=True)
            area_min, area_max = df["Area (px²)"].min(), df["Area (px²)"].max()
            area_avg = int(df["Area (px²)"].mean().round(0))
            
            sc1, sc2, sc3, sc4 = st.columns(4)
            
            def render_area_stat(col, label, val, icon_class):
                col.markdown(f"""
                    <div class="area-monitor">
                        <div class="area-icon"><i class="{icon_class}"></i></div>
                        <div style="font-size:1.2rem; font-weight:bold; color:{current_t['text']};">{val}</div>
                        <div style="font-size:0.7rem; color:{current_t['text']}; opacity:0.7; margin-top:5px;">{label}</div>
                    </div>
                """, unsafe_allow_html=True)

            render_area_stat(sc1, "TOTAL", len(df), "fas fa-layer-group")
            render_area_stat(sc2, "MIN (px²)", f"{area_min:,.0f}", "fas fa-arrow-down")
            render_area_stat(sc3, "MAX (px²)", f"{area_max:,.0f}", "fas fa-arrow-up")
            render_area_stat(sc4, "RATA-RATA", f"{area_avg:,.0f}", "fas fa-chart-line")

        # --- TOMBOL DOWNLOAD ---
        st.write("")
        d1, d2 = st.columns(2)
        with d1:
            if st.button("📊 EKSPOR EXCEL", use_container_width=True):
                excel_download_popup(df)
        with d2:
            if st.button("🖼️ EKSPOR GAMBAR", use_container_width=True):
                if "dl_step" in st.session_state: del st.session_state.dl_step
                if "temp_choice" in st.session_state:
                    del st.session_state.temp_choice
                interactive_download_popup(gray_img, blurred_img, mask, result, thresh_raw)

    else:
        st.warning("⚠️ TIDAK ADA OBJEK TERDETEKSI. SESUAIKAN PARAMETER THRESHOLD.")
else:
    # Tampilan awal jika belum ada gambar
    st.markdown(f"""
    <div style='text-align: center; padding: 50px; opacity: 0.5;'>
        <h2 style='color:{current_t['primary']};'><i class='fas fa-power-off'></i> SISTEM SIAP DI GUNAKAN</h2>
        <p style='color:{current_t['text']};'>Menunggu Input Gambar...</p>
    </div>
    """, unsafe_allow_html=True)
