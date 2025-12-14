import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import requests # Ditambahkan untuk fitur Demo Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    layout="wide",
    page_title="Smart Object Counter Pro",
    initial_sidebar_state="expanded"
)

# --- 2. ULTRA MODERN CSS (CYBERPUNK HUD THEME + FONTAWESOME + MARQUEE) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@400;600&family=Inter:wght@300;400;600&display=swap');

    /* BACKGROUND UTAMA - DEEP SPACE GRID */
    .stApp {
        background-color: #050a14;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #e0f2fe;
        font-family: 'Inter', sans-serif;
    }

    /* HEADERS - ORBITRON FONT (SCI-FI LOOK) */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #00f2ff, #bc13fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }
    
    h4, h5, h6 {
        color: #94a3b8 !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 10, 20, 0.9);
        border-right: 1px solid #1e293b;
    }
    
    /* CUSTOM HUD CARD */
    .hud-card {
        background: rgba(16, 23, 41, 0.7);
        border: 1px solid rgba(0, 242, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.05);
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .hud-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(to bottom, #00f2ff, #bc13fe);
    }

    /* --- ANIMASI RUNNING TEXT --- */
    .marquee-container {
        width: 100%;
        background: rgba(16, 23, 41, 0.9);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 4px;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 30px;
        padding: 10px 0;
        position: relative;
    }

    .marquee-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(to bottom, #00f2ff, #bc13fe);
        z-index: 2;
    }

    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        font-size: 0.9rem;
        letter-spacing: 2px;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
    }

    .marquee-text i {
        margin: 0 15px;
        color: #bc13fe;
    }

    @keyframes marquee {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }

    /* STATISTIK VALUE */
    .digital-val {
        font-family: 'Roboto Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .digital-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ICON */
    .hud-icon {
        font-size: 1.5rem;
        margin-bottom: 10px;
        opacity: 0.8;
    }

    /* INFO CITRA BOX */
    .info-monitor {
        background: rgba(6, 78, 59, 0.2);
        border: 1px solid #059669;
        border-radius: 4px;
        padding: 15px;
        color: #6ee7b7;
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
    }
    
    .info-monitor i {
        margin-right: 8px;
        width: 20px;
        text-align: center;
    }

    /* AREA STATS BOX */
    .area-monitor {
        background: rgba(30, 41, 59, 0.4);
        border: 1px dashed #475569;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s;
    }
    .area-monitor:hover {
        transform: translateY(-5px);
        border-color: #00f2ff;
    }
    .area-icon {
        font-size: 1.2rem;
        color: #00f2ff;
        margin-bottom: 5px;
    }

    /* TOMBOL */
    div[data-testid="stButton"] button {
        background: transparent;
        color: #00f2ff;
        border: 1px solid #00f2ff;
        border-radius: 0px;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
        box-shadow: 0 0 5px rgba(0, 242, 255, 0.2);
        width: 100%;
    }
    div[data-testid="stButton"] button:hover {
        background: rgba(0, 242, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.6);
        color: white;
        border-color: white;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.02);
        color: #94a3b8;
        border: 1px solid transparent;
        border-radius: 0px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 242, 255, 0.05) !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        box-shadow: inset 0 0 10px rgba(0, 242, 255, 0.1);
    }
    
    /* STYLING EXPANDER */
    .streamlit-expanderHeader {
        background-color: rgba(255,255,255,0.02);
        color: #00f2ff !important;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        border-radius: 4px;
        border: 1px solid rgba(0, 242, 255, 0.2);
    }
    
    /* Pop-up Styles */
    div[role="dialog"] {
        background: #0b1120 !important;
        border: 1px solid #1e293b !important;
        box-shadow: 0 0 50px rgba(0, 242, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.markdown("### <i class='fas fa-cogs'></i> KONTROL SISTEM", unsafe_allow_html=True)
st.sidebar.info("💡 **TIPS:** Gunakan gambar dengan kontras tinggi untuk akurasi maksimal.")
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-family:Orbitron; color:#00f2ff;'><i class='fas fa-sliders-h'></i> PARAMETER DETEKSI</p>", unsafe_allow_html=True)

blur_value = st.sidebar.slider("Tingkat Denoise (Blur)", 1, 15, 9, step=2)
threshold_value = st.sidebar.slider("Sensitivitas Threshold", 0, 255, 142)
min_area = st.sidebar.slider("Area Objek Min (px)", 10, 2000, 894)

# --- 4. FUNGSI PROCESS ---
@st.cache_data
def process_image(file_content, blur_val, thresh_val, min_a):
    file_bytes = np.asarray(bytearray(file_content), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (blur_val, blur_val), 0)
    
    # 3. Thresholding (RAW)
    _, thresh = cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY_INV)
    
    # 4. MORPHOLOGY (CLEAN)
    kernel = np.ones((3, 3), np.uint8)
    # Open: Hilangkan noise
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # Close: Tutup lubang
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 5. Contour Detection
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = [] 
    object_data = []    
    
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
            
    result_img = img_rgb.copy()
    for idx, cnt in enumerate(valid_contours):
        # GAMBAR BOUNDING BOX (KOTAK HIJAU)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Opsional: Contour tipis
        cv2.drawContours(result_img, [cnt], -1, (255, 0, 0), 1)
        
        # Tulis Nomor
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            cv2.putText(result_img, str(idx+1), (cx-10, cy-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Return LENGKAP: termasuk thresh (raw) dan morph (clean)
    return img_rgb, result_img, object_data, morph, gray, blurred, thresh

def convert_to_bytes(img_array, is_gray=False):
    if is_gray: img_encode = img_array
    else: img_encode = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    is_success, im_buf_arr = cv2.imencode(".png", img_encode)
    return im_buf_arr.tobytes()

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Deteksi')
    return output.getvalue()

# --- 5. POP-UP DIALOGS ---
@st.dialog("💾 DOWNLOAD SISTEM")
def interactive_download_popup(img_gray, img_blur, img_mask, img_result, img_thresh):
    if "dl_step" not in st.session_state: st.session_state.dl_step = "pilihan"
    if "selected_opt" not in st.session_state: st.session_state.selected_opt = None

    def go_to_validation():
        st.session_state.selected_opt = st.session_state.temp_choice
        st.session_state.dl_step = "validasi"

    if st.session_state.dl_step == "pilihan":
        st.markdown("<p style='text-align:center; color:#00f2ff;'><i class='fas fa-file-export'></i> PILIH FORMAT OUTPUT</p>", unsafe_allow_html=True)
        # Opsi Radio Button
        st.radio("Opsi:", ["Hasil Preprocessing (Gray, Blur, Thresh)", "Hasil Morfologi (Clean Mask)", 
                           "Hasil Akhir (Deteksi)", "Download Semua Gambar"], 
                 index=None, key="temp_choice", on_change=go_to_validation, label_visibility="collapsed")

    elif st.session_state.dl_step == "validasi":
        choice = st.session_state.selected_opt
        is_multi = (choice == "Hasil Preprocessing (Gray, Blur, Thresh)" or choice == "Download Semua Gambar")
        
        st.markdown(f"""
            <div style='background:rgba(255,255,255,0.05); padding:15px; border-left:3px solid #f59e0b;'>
                <p style='color:#f59e0b; margin:0; font-size:0.8rem;'><i class='fas fa-exclamation-triangle'></i> KONFIRMASI AKSI</p>
                <h4 style='color:white; margin:5px 0;'>{choice}</h4>
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
    st.markdown("""
        <div style='background:rgba(255,255,255,0.05); padding:15px; border-left:3px solid #10b981;'>
            <p style='color:#10b981; margin:0; font-size:0.8rem;'><i class='fas fa-file-excel'></i> FORMAT EKSPOR</p>
            <h4 style='color:white; margin:5px 0;'>Microsoft Excel (.xlsx)</h4>
        </div><br>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.download_button("✅ UNDUH", convert_df_to_excel(df), "data_deteksi.xlsx", 
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    if c2.button("❌ BATAL", use_container_width=True): st.rerun()

# --- 6. MAIN LAYOUT ---
st.markdown("<h1 style='text-align: center;'>SMART OBJECT COUNTER <span style='font-size:1.5rem; color:#00f2ff; vertical-align: super;'>PRO</span></h1>", unsafe_allow_html=True)

# --- RUNNING TEXT ---
st.markdown("""
    <div class="marquee-container">
        <div class="marquee-text">
            <i class="fas fa-robot"></i> SELAMAT DATANG DI SMART OBJECT COUNTER PRO 
            <i class="fas fa-minus"></i> APLIKASI IMAGE PROCESSING BERBASIS STREAMLIT
            <i class="fas fa-minus"></i> PENGHITUNGAN JUMLAH OBJEK KECIL 
            <i class="fas fa-minus"></i> SILAKAN UNGGAH GAMBAR UNTUK MEMULAI DETEKSI OBJEK OTOMATIS 
            <i class="fas fa-minus"></i> PASTIKAN KONTRAS GAMBAR BAIK UNTUK HASIL MAKSIMAL 
            <i class="fas fa-check-circle"></i> SISTEM SIAP DIGUNAKAN
        </div>
    </div>
""", unsafe_allow_html=True)

# --- PILIHAN INPUT (FITUR BARU) ---
# Radio button horizontal untuk memilih sumber
input_method = st.radio(
    "👉 Pilih Sumber Gambar:", 
    ("📂 Unggah Gambar Sendiri", "🧪 Gunakan Gambar Contoh (Demo)"), 
    horizontal=True
)

file_bytes_content = None
file_extension = ""

if input_method == "🧪 Gunakan Gambar Contoh (Demo)":
    # Link gambar koin/benda kecil dari internet yang stabil
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
    # Widget Upload Biasa
    uploaded_file = st.file_uploader("Upload Gambar disini", type=["jpg", "png", "jpeg", "bmp", "webp"], label_visibility="collapsed")
    if uploaded_file is not None:
        file_bytes_content = uploaded_file.getvalue()
        file_extension = uploaded_file.name.split('.')[-1].upper()

# --- INFO APLIKASI (EXPANDER DENGAN DESAIN GRID) ---
with st.expander("ℹ️ TENTANG APLIKASI & PANDUAN PENGGUNAAN (KLIK UNTUK BACA)", expanded=False):
    # Desain Baru Menggunakan HUD Cards agar Konsisten
    st.markdown("""
    <div class="hud-card" style="text-align: left; margin-bottom: 15px;">
        <h4 style="color: #00f2ff; margin-bottom: 10px;">📖 DESKRIPSI SISTEM</h4>
        <p style="color: #e0f2fe; font-size: 0.9rem; line-height: 1.6;">
            <b>Smart Object Counter Pro</b> adalah sistem visi komputer canggih untuk penghitungan otomatis objek mikroskopis dan komponen kecil.
            Sistem ini mengeliminasi kesalahan manusia (human error) dalam proses quality control dan inventarisasi dengan akurasi tinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_info1, c_info2 = st.columns(2)

    with c_info1:
        st.markdown("""
        <div class="hud-card" style="height: 100%; text-align: left;">
            <h5 style="color: #bc13fe; border-bottom: 1px solid #bc13fe; padding-bottom: 5px;">⚙️ ARSITEKTUR TEKNIS</h5>
            <ul style="color: #e0f2fe; font-size: 0.85rem; list-style: none; padding-left: 0; line-height: 1.8;">
                <li><i class="fas fa-code-branch" style="color:#bc13fe; width:20px;"></i> <b>GRAYSCALE:</b> Konversi spektrum warna.</li>
                <li><i class="fas fa-tint" style="color:#bc13fe; width:20px;"></i> <b>GAUSSIAN BLUR:</b> Reduksi noise frekuensi tinggi.</li>
                <li><i class="fas fa-adjust" style="color:#bc13fe; width:20px;"></i> <b>THRESHOLDING:</b> Segmentasi biner adaptif.</li>
                <li><i class="fas fa-filter" style="color:#bc13fe; width:20px;"></i> <b>MORFOLOGI:</b> Opening/Closing struktur.</li>
                <li><i class="fas fa-vector-square" style="color:#bc13fe; width:20px;"></i> <b>CONTOUR:</b> Ekstraksi topologi objek.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_info2:
        st.markdown("""
        <div class="hud-card" style="height: 100%; text-align: left;">
            <h5 style="color: #f59e0b; border-bottom: 1px solid #f59e0b; padding-bottom: 5px;">🚀 PROTOKOL OPERASIONAL</h5>
            <ol style="color: #e0f2fe; font-size: 0.85rem; padding-left: 20px; line-height: 1.6;">
                <li>Pilih mode: <b>Unggah Gambar</b> atau <b>Gambar Contoh</b>.</li>
                <li>Tunggu proses <b>Analisis AI</b> selesai.</li>
                <li>Lakukan kalibrasi manual pada <b>SIDEBAR</b> jika perlu:
                    <ul style="color: #94a3b8; margin-top:5px; list-style: circle;">
                        <li><i>Denoise</i> untuk kejernihan.</li>
                        <li><i>Threshold</i> untuk sensitivitas.</li>
                    </ul>
                </li>
                <li>Ekspor data hasil deteksi via tombol <b>EKSPOR</b> pada bagian bawah aplikasi.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

if file_bytes_content is not None:
    # Process
    # Unpack 7 variabel (sekarang termasuk thresh)
    original, result, data_list, mask, gray_img, blurred_img, thresh_raw = process_image(
        file_bytes_content, blur_value, threshold_value, min_area
    )
    h, w, c = original.shape
    
    if data_list:
        df = pd.DataFrame(data_list)
        low, high = df["Area (px²)"].quantile(0.33), df["Area (px²)"].quantile(0.66)
        df["Jenis"] = df["Area (px²)"].apply(lambda x: "Kecil" if x < low else ("Sedang" if x < high else "Besar"))
        
        df["No"] = range(1, len(df) + 1)
        df = df[["No", "Jenis", "Area (px²)", "Circularity", "Posisi X", "Posisi Y", "Lebar", "Tinggi"]]
        counts = df["Jenis"].value_counts()
        
        # --- DASHBOARD STATISTIK ---
        st.markdown("### <i class='fas fa-satellite-dish'></i> HASIL DETEKSI", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        
        def render_hud_stat(col, label, value, icon_class, color="#00f2ff"):
            col.markdown(f"""
                <div class="hud-card" style="text-align:center; padding: 15px;">
                    <div class="hud-icon" style="color:{color}"><i class="{icon_class}"></i></div>
                    <div class="digital-val" style="color:{color}">{value}</div>
                    <div class="digital-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
            
        render_hud_stat(c1, "TOTAL TERDETEKSI", len(df), "fas fa-layer-group", "#ffffff")
        render_hud_stat(c2, "OBJEK KECIL", counts.get("Kecil", 0), "fas fa-compress-arrows-alt", "#00f2ff")
        render_hud_stat(c3, "OBJEK SEDANG", counts.get("Sedang", 0), "fas fa-expand", "#bc13fe")
        render_hud_stat(c4, "OBJEK BESAR", counts.get("Besar", 0), "fas fa-expand-arrows-alt", "#f59e0b")

        # --- TABS SECTION ---
        tab1, tab2, tab3 = st.tabs(["👁️ VISUALISASI", "📈 ANALISIS", "💾 DATA MENTAH"])
        
        # === TAB 1: VISUALISASI ===
        with tab1:
            st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
            
            # --- EXPANDER: Menampilkan Tahapan Awal (Input -> Threshold Mentah) ---
            with st.expander("🔻 DETAIL ALUR PREPROCESSING (KLIK UNTUK BUKA/TUTUP)", expanded=True):
                st.markdown("<p style='font-family:Orbitron; color:#94a3b8; font-size:0.9rem'>// <i class='fas fa-microchip'></i> TAHAPAN PROSES AWAL</p>", unsafe_allow_html=True)
                # Tampilkan 4 Gambar: Asli, Gray, Blur, Threshold Mentah
                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                col_p1.image(original, caption="1. INPUT ASLI", use_container_width=True)
                col_p2.image(gray_img, caption="2. GRAYSACALE", use_container_width=True)
                col_p3.image(blurred_img, caption="3. GAUSSIAN BLUR", use_container_width=True)
                col_p4.image(thresh_raw, caption="4. THRESHOLD (RAW)", use_container_width=True)
            
            st.markdown("---")
            
            # --- AREA UTAMA: Hasil Morfologi & Final ---
            st.markdown("<p style='font-family:Orbitron; color:#94a3b8; font-size:0.9rem'>// <i class='fas fa-bullseye'></i> HASIL PEMROSESAN AKHIR</p>", unsafe_allow_html=True)
            col_r1, col_r2 = st.columns(2)
            # Menampilkan Mask yang sudah bersih (Morphology)
            col_r1.image(mask, caption="5. HASIL MORFOLOGI (CLEAN MASK)", use_container_width=True)
            # Menampilkan Hasil Akhir dengan Bounding Box
            col_r2.image(result, caption="6. OUTPUT AKHIR (BOUNDING BOX)", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='hud-card'>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            
            # Pie Chart
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            fig1.patch.set_alpha(0)
            colors = ['#00f2ff', '#bc13fe', '#f59e0b']
            dist_data = counts.reset_index()
            dist_data.columns = ["Kategori", "Jumlah"]
            
            wedges, texts, autotexts = ax1.pie(dist_data["Jumlah"], labels=dist_data["Kategori"], 
                                             autopct='%1.1f%%', startangle=90, colors=colors,
                                             textprops={'color':"white", 'fontsize': 10, 'fontweight': 'bold'})
            plt.setp(autotexts, size=12, weight="bold", color="black")
            g1.pyplot(fig1, use_container_width=True)
            
            # Bar Chart
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_alpha(0)
            ax2.set_facecolor("none")
            bars = ax2.bar(dist_data["Kategori"], dist_data["Jumlah"], color=colors, edgecolor="white", alpha=0.8)
            ax2.tick_params(colors='white')
            for spine in ax2.spines.values(): spine.set_edgecolor('#334155')
            ax2.grid(axis='y', linestyle='--', alpha=0.2, color='#00f2ff')
            g2.pyplot(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

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
                    <div><i class="fas fa-wifi"></i> STATUS  : <span style="color:#00f2ff">ONLINE</span></div>
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
                        <div style="font-size:1.2rem; font-weight:bold; color:#e2e8f0;">{val}</div>
                        <div style="font-size:0.7rem; color:#94a3b8; margin-top:5px;">{label}</div>
                    </div>
                """, unsafe_allow_html=True)

            render_area_stat(sc1, "TOTAL", len(df), "fas fa-layer-group")
            render_area_stat(sc2, "MIN (px²)", f"{area_min:,.0f}", "fas fa-arrow-down")
            render_area_stat(sc3, "MAX (px²)", f"{area_max:,.0f}", "fas fa-arrow-up")
            render_area_stat(sc4, "RATA-RATA", f"{area_avg:,.0f}", "fas fa-chart-line")

        # --- DOWNLOAD SECTION ---
        st.write("")
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
    # Tampilan awal kosong
    st.markdown("""
    <div style='text-align: center; padding: 50px; opacity: 0.5;'>
        <h2 style='color:#00f2ff;'><i class='fas fa-power-off'></i> SISTEM SIAP DI GUNAKAN</h2>
        <p>Menunggu Input Gambar...</p>
    </div>
    """, unsafe_allow_html=True)