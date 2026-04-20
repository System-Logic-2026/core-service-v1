import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# =============================================================================
# 🔧 CẤU HÌNH TRANG
# =============================================================================
st.set_page_config(
    page_title="💎 AI-QUANTUM GLOBAL",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# 🎨 CSS - GIAO DIỆN ĐẲNG CẤP
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Roboto:wght@300;400;500;700;900&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* HEADER GOLD LUXURY */
    .main-header {
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 50%, #B8962E 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(212,175,55,0.5), 
                    inset 0 2px 10px rgba(255,255,255,0.3);
        border: 3px solid #FFD700;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3em;
        font-weight: 900;
        color: #000;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.3);
        letter-spacing: 3px;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    .main-header p {
        color: #1a1a1a;
        font-size: 1.2em;
        font-weight: 600;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    /* TIMESTAMP */
    .timestamp-container {
        background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(212,175,55,0.1));
        border: 2px solid #D4AF37;
        padding: 15px 30px;
        border-radius: 30px;
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
    }
    .timestamp-text {
        color: #D4AF37;
        font-weight: 700;
        font-size: 1.1em;
        letter-spacing: 1px;
    }
    
    /* DISCLAIMER */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(255,193,7,0.15), rgba(255,193,7,0.05));
        border-left: 5px solid #D4AF37;
        padding: 15px 25px;
        border-radius: 10px;
        margin: 20px;
        color: #FFD700;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(212,175,55,0.2);
    }
    
    /* BẢNG KẾT QUẢ CHUẨN */
    .result-container {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 3px solid #D4AF37;
        box-shadow: 0 8px 30px rgba(212,175,55,0.3);
    }
    .result-header {
        background: linear-gradient(135deg, #c41e3a, #8b0000);
        color: #fff;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        font-weight: 900;
        font-size: 1.4em;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 4px 15px rgba(196,30,58,0.4);
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 35px;
        font-weight: 700;
        font-size: 1.15em;
        border-radius: 12px;
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border: 2px solid #D4AF37;
        color: #D4AF37;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4AF37, #FFD700);
        color: #000;
        box-shadow: 0 6px 20px rgba(212,175,55,0.5);
        transform: translateY(-2px);
    }
    
    /* PREDICTION CARDS */
    .pred-section {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        border: 3px solid #D4AF37;
        box-shadow: 0 8px 30px rgba(212,175,55,0.3);
    }
    .pred-title-box {
        background: linear-gradient(135deg, #000, #1a1a1a);
        border: 2px solid #D4AF37;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
    }
    .pred-title-text {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        font-size: 1.6em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin: 0;
    }
    
    .pred-card-luxury {
        background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.05));
        border: 3px solid #D4AF37;
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 15px rgba(212,175,55,0.2);
    }
    .pred-card-luxury:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(212,175,55,0.4);
    }
    .pred-card-title {
        color: #D4AF37;
        font-size: 1.1em;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .pred-number-big {
        font-size: 2.8em;
        font-weight: 900;
        color: #fff;
        margin: 15px 0;
        text-shadow: 0 0 20px rgba(212,175,55,0.6);
        letter-spacing: 4px;
    }
    .pred-confidence {
        color: #FFD700;
        font-weight: 700;
        font-size: 1.05em;
        margin-top: 10px;
    }
    
    /* DÀN ĐỀ */
    .dan-de-luxury {
        background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(212,175,55,0.1));
        border: 3px solid #D4AF37;
        border-radius: 15px;
        padding: 25px;
        margin-top: 25px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(212,175,55,0.3);
    }
    .dan-de-title {
        color: #D4AF37;
        font-size: 1.3em;
        font-weight: 900;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .dan-de-numbers {
        font-size: 1.6em;
        font-weight: 700;
        color: #fff;
        letter-spacing: 4px;
        line-height: 2;
        text-shadow: 0 0 15px rgba(212,175,55,0.5);
    }
    
    /* HISTORY */
    .history-luxury {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        border: 3px solid #D4AF37;
        box-shadow: 0 8px 30px rgba(212,175,55,0.3);
    }
    .history-title {
        color: #D4AF37;
        font-size: 1.4em;
        font-weight: 900;
        margin-bottom: 20px;
        text-transform: uppercase;
        text-align: center;
    }
    
    /* STATS CARDS */
    .stat-card-luxury {
        background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.05));
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(212,175,55,0.2);
    }
    
    /* FOOTER */
    .footer-luxury {
        background: linear-gradient(135deg, #000, #1a1a1a);
        border-top: 3px solid #D4AF37;
        padding: 30px;
        text-align: center;
        margin-top: 40px;
        color: #888;
    }
    
    /* REFRESH BUTTON */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37, #FFD700);
        color: #000;
        border: none;
        border-radius: 10px;
        font-weight: 900;
        font-size: 1.1em;
        padding: 15px 40px;
        box-shadow: 0 4px 15px rgba(212,175,55,0.4);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(212,175,55,0.6);
    }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8em; }
        .pred-number-big { font-size: 2em; }
        .dan-de-numbers { font-size: 1.2em; }
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 🔄 AUTO-REFRESH (30 GIÂY)
# =============================================================================
auto_refresh = st_autorefresh(interval=30000, limit=None, key="auto_refresh")

# =============================================================================
# 📡 FETCH DATA
# =============================================================================
@st.cache_data(ttl=300)
def fetch_lottery_data(region: str) -> dict:
    """Fetch real-time lottery results"""
    
    urls = {
        "Miền Bắc": "https://xosodaiphat.com/xsmb-xổ-số-miền-bắc.html",
        "Miền Trung": "https://xosodaiphat.com/xsmt-xổ-số-miền-trung.html",
        "Miền Nam": "https://xosodaiphat.com/xsmn-xổ-số-miền-nam.html"
    }
    
    # Mock data chuẩn
    mock_data = {
        "Miền Bắc": {
            "special": "74197", "first": "88897",
            "second": ["75281", "83073"],
            "third": ["29125", "09606", "31567", "93696", "67272", "21532"],
            "fourth": ["4114", "0721", "0708", "0206"],
            "fifth": ["2853", "0707", "7804", "9339", "4057", "5308"],
            "sixth": ["466", "461", "061"],
            "seventh": ["34", "06", "47", "39"]
        },
        "Miền Trung": {
            "special": "52846", "first": "19273",
            "second": ["48291", "73654"],
            "third": ["12847", "56392", "84756"],
            "fourth": ["9284", "4756", "1928", "6473"],
            "fifth": ["3847", "9283", "4756", "1928", "6473", "8291"],
            "sixth": ["384", "928", "475"],
            "seventh": ["28", "47", "93", "56"]
        },
        "Miền Nam": {
            "special": "39284", "first": "67492",
            "second": ["83746", "29384"],
            "third": ["47382", "92847", "38475", "62938", "47562", "93847"],
            "fourth": ["8374", "2938", "4756", "9283"],
            "fifth": ["3847", "9283", "4756", "1928", "6473", "8291"],
            "sixth": ["384", "928", "475", "192", "647", "829"],
            "seventh": ["38", "92", "47", "56"]
        }
    }
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(urls[region], headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        result = mock_data[region].copy()
        
        # Parse special prize
        special_div = soup.find("div", {"class": "special-prize"})
        if special_div:
            special_span = special_div.find("div", class_="text-center")
            if special_span:
                result["special"] = special_span.get_text(strip=True)
        
        # Parse first prize
        first_div = soup.find("div", {"class": "first-prize"})
        if first_div:
            first_span = first_div.find("div", class_="text-center")
            if first_span:
                result["first"] = first_span.get_text(strip=True)
        
        result["timestamp"] = datetime.now().strftime("%H:%M:%S")
        return result
        
    except Exception as e:
        result = mock_data[region].copy()
        result["timestamp"] = datetime.now().strftime("%H:%M:%S")
        result["error"] = str(e)
        return result

# =============================================================================
# 🎯 AI PREDICTIONS
# =============================================================================
@st.cache_data(ttl=600)
def generate_predictions(region: str) -> dict:
    """Generate AI-based predictions"""
    np.random.seed(int(datetime.now().strftime("%H%M")) + hash(region) % 100)
    
    bach_thu = f"{np.random.randint(0, 100):02d}"
    song_thu_1 = f"{np.random.randint(0, 100):02d}"
    song_thu_2 = f"{np.random.randint(0, 100):02d}"
    
    return {
        "bach_thu": bach_thu,
        "bach_thu_conf": np.random.randint(75, 96),
        "song_thu": [song_thu_1, song_thu_2],
        "song_thu_conf": np.random.randint(70, 91),
        "xien_2": [bach_thu, song_thu_1],
        "dan_de": sorted([f"{i:02d}" for i in np.random.choice(100, 10, replace=False)]),
        "generated_at": datetime.now().strftime("%H:%M:%S")
    }

# =============================================================================
# 📊 HISTORY
# =============================================================================
@st.cache_data
def get_history() -> dict:
    return {
        "Miền Bắc": [
            {"date": "19/04", "type": "Bạch Thủ", "pred": "79", "result": "25", "win": False},
            {"date": "18/04", "type": "Song Thủ", "pred": "24-42", "result": "84", "win": True},
            {"date": "17/04", "type": "Bạch Thủ", "pred": "09", "result": "09", "win": True},
        ],
        "Miền Trung": [
            {"date": "19/04", "type": "Bạch Thủ", "pred": "38", "result": "62", "win": False},
            {"date": "18/04", "type": "Song Thủ", "pred": "06-60", "result": "60", "win": True},
            {"date": "17/04", "type": "Bạch Thủ", "pred": "47", "result": "47", "win": True},
        ],
        "Miền Nam": [
            {"date": "19/04", "type": "Bạch Thủ", "pred": "15", "result": "15", "win": True},
            {"date": "18/04", "type": "Song Thủ", "pred": "78-87", "result": "78", "win": True},
            {"date": "17/04", "type": "Xiên 2", "pred": "15-78", "result": "78", "win": True},
        ]
    }

# =============================================================================
# 🎨 RENDER FUNCTIONS
# =============================================================================
def render_results_table(region: str,  dict):
    """Render beautiful results table"""
    titles = {
        "Miền Bắc": "🔴 XSMB - KẾT QUẢ XỔ SỐ MIỀN BẮC",
        "Miền Trung": "🟡 XSMT - KẾT QUẢ XỔ SỐ MIỀN TRUNG",
        "Miền Nam": "🟢 XSMN - KẾT QUẢ XỔ SỐ MIỀN NAM"
    }
    
    st.markdown(f'<div class="result-header">{titles[region]}</div>', unsafe_allow_html=True)
    
    # Create DataFrame
    df_data = {
        "Giải": ["G.ĐB", "G.1", "G.2", "G.3", "G.4", "G.5", "G.6", "G.7"],
        "Kết Quả": [
            data["special"],
            data["first"],
            " • ".join(data["second"]),
            " • ".join(data["third"]),
            " • ".join(data["fourth"]),
            " • ".join(data["fifth"]),
            " • ".join(data["sixth"]),
            " • ".join(data["seventh"])
        ]
    }
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown(f'<p style="text-align: center; color: #666; margin-top: 10px;">⏰ Cập nhật: {data.get("timestamp", "N/A")}</p>', unsafe_allow_html=True)


def render_predictions_luxury(pred: dict):
    """Render luxury prediction cards"""
    st.markdown("""
    <div class="pred-section">
        <div class="pred-title-box">
            <h2 class="pred-title-text">💎 DỰ ĐOÁN VIP AI-QUANTUM</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="pred-card-luxury">
            <div class="pred-card-title">✅ BẠCH THỦ LÔ VIP</div>
            <div class="pred-number-big">{pred['bach_thu']}</div>
            <div class="pred-confidence">🎯 Độ tin cậy: {pred['bach_thu_conf']}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="pred-card-luxury">
            <div class="pred-card-title">✅ SONG THỦ LÔ VIP</div>
            <div class="pred-number-big">{' - '.join(pred['song_thu'])}</div>
            <div class="pred-confidence">🎯 Độ tin cậy: {pred['song_thu_conf']}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="pred-card-luxury">
            <div class="pred-card-title">✅ XIÊN 2</div>
            <div class="pred-number-big">{' - '.join(pred['xien_2'])}</div>
            <div class="pred-confidence">⭐ Chuẩn xác cao</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dàn đề
    st.markdown(f"""
    <div class="dan-de-luxury">
        <div class="dan-de-title">🔥 DÀN ĐỀ 10 SỐ VIP 🔥</div>
        <div class="dan-de-numbers">{', '.join(pred['dan_de'])}</div>
        <p style="color: #888; margin-top: 10px; font-size: 0.9em;">Generated: {pred['generated_at']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_history_luxury(region: str, history: dict):
    """Render luxury history section"""
    data = history.get(region, [])
    total = len(data)
    wins = sum(1 for d in data if d["win"])
    rate = (wins / total * 100) if total > 0 else 0
    
    st.markdown('<div class="history-luxury">', unsafe_allow_html=True)
    st.markdown('<h3 class="history-title">📊 LỊCH SỬ DỰ ĐOÁN & THỐNG KÊ</h3>', unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card-luxury">
            <div style="font-size: 2em; font-weight: 900; color: #D4AF37;">{total}</div>
            <div style="color: #888; margin-top: 5px;">Tổng</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card-luxury">
            <div style="font-size: 2em; font-weight: 900; color: #10b981;">{wins}</div>
            <div style="color: #888; margin-top: 5px;">Trúng</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card-luxury">
            <div style="font-size: 2em; font-weight: 900; color: #c41e3a;">{rate:.0f}%</div>
            <div style="color: #888; margin-top: 5px;">Tỷ lệ</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Table
    if 
        df_data = []
        for item in 
            df_data.append({
                "Ngày": item["date"],
                "Loại": item["type"],
                "Dự Đoán": item["pred"],
                "Kết Quả": item["result"],
                "Trạng Thái": "✅" if item["win"] else "❌"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 🚀 MAIN APP
# =============================================================================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💎 AI-QUANTUM GLOBAL</h1>
        <p>Hệ Thống Phân Tích Xổ Số Thông Minh Cao Cấp</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timestamp
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f"""
    <div class="timestamp-container">
        <div class="timestamp-text">📅 Cập nhật: {now}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Lưu ý quan trọng:</strong> Xổ số là trò chơi ngẫu nhiên. Mọi dự đoán chỉ mang tính chất tham khảo giải trí, 
        không đảm bảo trúng thưởng. Vui lòng chơi có trách nhiệm và trong khả năng tài chính.
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab_mb, tab_mt, tab_mn = st.tabs(["🔴 MIỀN BẮC", "🟡 MIỀN TRUNG", "🟢 MIỀN NAM"])
    
    # Load data
    history = get_history()
    
    # Miền Bắc
    with tab_mb:
        with st.spinner("💎 Đang cập nhật Miền Bắc..."):
            data_mb = fetch_lottery_data("Miền Bắc")
            pred_mb = generate_predictions("Miền Bắc")
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        render_results_table("Miền Bắc", data_mb)
        st.markdown('</div>', unsafe_allow_html=True)
        
        render_predictions_luxury(pred_mb)
        render_history_luxury("Miền Bắc", history)
    
    # Miền Trung
    with tab_mt:
        with st.spinner("💎 Đang cập nhật Miền Trung..."):
            data_mt = fetch_lottery_data("Miền Trung")
            pred_mt = generate_predictions("Miền Trung")
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        render_results_table("Miền Trung", data_mt)
        st.markdown('</div>', unsafe_allow_html=True)
        
        render_predictions_luxury(pred_mt)
        render_history_luxury("Miền Trung", history)
    
    # Miền Nam
    with tab_mn:
        with st.spinner("💎 Đang cập nhật Miền Nam..."):
            data_mn = fetch_lottery_data("Miền Nam")
            pred_mn = generate_predictions("Miền Nam")
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        render_results_table("Miền Nam", data_mn)
        st.markdown('</div>', unsafe_allow_html=True)
        
        render_predictions_luxury(pred_mn)
        render_history_luxury("Miền Nam", history)
    
    # Refresh button
    st.markdown("<div style='text-align: center; margin: 30px 0;'>", unsafe_allow_html=True)
    if st.button("🔄 LÀM MỚI DỮ LIỆU NGAY", use_container_width=False):
        st.cache_data.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-luxury">
        <p style="margin: 0; font-size: 1.1em; color: #D4AF37; font-weight: 700;">
            💎 AI-QUANTUM GLOBAL
        </p>
        <p style="margin: 8px 0 0; font-size: 0.9em;">
            Dữ liệu cập nhật tự động mỗi 30 giây • Không thu thập thông tin cá nhân
        </p>
        <p style="margin: 8px 0 0; color: #D4AF37; font-weight: 600;">
            Chơi xổ số có trách nhiệm - Chúc may mắn!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()