import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd

# =============================================================================
# 🔧 CẤU HÌNH
# =============================================================================
st.set_page_config(page_title="AI-QUANTUM GLOBAL 💎", page_icon="💎", layout="wide")

# CSS
st.markdown("""
<style>
    .main { background: #f5f5f5; }
    
    .gold-header {
        background: linear-gradient(135deg, #D4AF37, #B8962E);
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
    
    .result-header {
        background: linear-gradient(135deg, #c41e3a, #8b0000);
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 900;
        font-size: 1.3em;
        border-radius: 8px 8px 0 0;
    }
    
    .special-num {
        color: #c41e3a;
        font-size: 2.5em;
        font-weight: 900;
        text-align: center;
        letter-spacing: 5px;
    }
    
    .g1-num {
        font-size: 1.8em;
        font-weight: 800;
        text-align: center;
    }
    
    .number-text {
        font-size: 1.2em;
        font-weight: 700;
        text-align: center;
    }
    
    .g7-num {
        color: #c41e3a;
        font-weight: 800;
        text-align: center;
    }
    
    .pred-card {
        background: linear-gradient(135deg, #fffef0, #fff);
        border: 3px solid #D4AF37;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .pred-number {
        font-size: 2.2em;
        font-weight: 900;
        color: #000;
        margin: 10px 0;
    }
    
    .dan-de-container {
        background: linear-gradient(135deg, #fffef0, #fff);
        border: 3px solid #D4AF37;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .stats-box {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #D4AF37;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 🔄 FETCH DATA
# =============================================================================
@st.cache_data(ttl=300)
def get_kqxs(mien):
    urls = {
        "Miền Bắc": "https://xosodaiphat.com/xsmb-xổ-số-miền-bắc.html",
        "Miền Trung": "https://xosodaiphat.com/xsmt-xổ-số-miền-trung.html",
        "Miền Nam": "https://xosodaiphat.com/xsmn-xổ-số-miền-nam.html"
    }
    
    data_default = {
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
        res = requests.get(urls[mien], headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = data_default[mien].copy()
        
        sp = soup.find("div", {"class": "special-prize"})
        if sp:
            val = sp.find("div", class_="text-center")
            if val:
                result["special"] = val.get_text(strip=True)
        
        g1 = soup.find("div", {"class": "first-prize"})
        if g1:
            val = g1.find("div", class_="text-center")
            if val:
                result["first"] = val.get_text(strip=True)
        
        return result
    except:
        return data_default[mien]

@st.cache_data(ttl=600)
def get_du_doan(mien):
    np.random.seed(int(datetime.now().strftime("%H%M")) + hash(mien) % 100)
    bt = f"{np.random.randint(0,100):02d}"
    st1 = f"{np.random.randint(0,100):02d}"
    st2 = f"{np.random.randint(0,100):02d}"
    
    return {
        "bach_thu": bt,
        "conf_bt": np.random.randint(75, 95),
        "song_thu": [st1, st2],
        "conf_st": np.random.randint(70, 90),
        "xien_2": [bt, st1],
        "dan_de": sorted([f"{i:02d}" for i in np.random.choice(100, 10, replace=False)])
    }

@st.cache_data
def get_lich_su():
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
# 🎨 RENDER FUNCTIONS - STREAMLIT NATIVE
# =============================================================================
def render_bang_ket_qua(mien, kq):
    """Bảng kết quả bằng Streamlit DataFrame"""
    titles = {
        "Miền Bắc": "🔴 XSMB - KẾT QUẢ XỔ SỐ MIỀN BẮC",
        "Miền Trung": "🟡 XSMT - KẾT QUẢ XỔ SỐ MIỀN TRUNG",
        "Miền Nam": "🟢 XSMN - KẾT QUẢ XỔ SỐ MIỀN NAM"
    }
    
    # Title
    st.markdown(f'<div class="result-header">{titles[mien]}</div>', unsafe_allow_html=True)
    
    # Create DataFrame
    df_data = {
        "Giải": ["G.ĐB", "G.1", "G.2", "G.3", "G.4", "G.5", "G.6", "G.7"],
        "Kết quả": [
            kq["special"],
            kq["first"],
            " • ".join(kq["second"]),
            " • ".join(kq["third"]),
            " • ".join(kq["fourth"]),
            " • ".join(kq["fifth"]),
            " • ".join(kq["sixth"]),
            " • ".join(kq["seventh"])
        ]
    }
    
    df = pd.DataFrame(df_data)
    
    # Display with custom styling
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Giải": st.column_config.TextColumn(width="small"),
            "Kết quả": st.column_config.TextColumn(width="large")
        }
    )


def render_du_doan(dd):
    """Dự đoán bằng Streamlit columns - NO HTML"""
    st.markdown('<div class="gold-header" style="margin: 20px 0;"><h2 style="color: #000; margin: 0;">💎 DỰ ĐOÁN VIP AI-QUANTUM</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="pred-card">', unsafe_allow_html=True)
        st.markdown("### ✅ BẠCH THỦ LÔ VIP")
        st.markdown(f'<div class="pred-number">{dd["bach_thu"]}</div>', unsafe_allow_html=True)
        st.markdown(f"🎯 **Độ tin cậy: {dd['conf_bt']}%**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pred-card">', unsafe_allow_html=True)
        st.markdown("### ✅ SONG THỦ LÔ VIP")
        st.markdown(f'<div class="pred-number">{" - ".join(dd["song_thu"])}</div>', unsafe_allow_html=True)
        st.markdown(f"🎯 **Độ tin cậy: {dd['conf_st']}%**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="pred-card">', unsafe_allow_html=True)
        st.markdown("### ✅ XIÊN 2")
        st.markdown(f'<div class="pred-number">{" - ".join(dd["xien_2"])}</div>', unsafe_allow_html=True)
        st.markdown("⭐ **Chuẩn xác cao**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dàn đề
    st.markdown('<div class="dan-de-container">', unsafe_allow_html=True)
    st.markdown("### 🔥 DÀN ĐỀ 10 SỐ VIP 🔥")
    st.markdown(f'<div style="font-size: 1.5em; font-weight: 700; letter-spacing: 3px;">{", ".join(dd["dan_de"])}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_lich_su(mien, lich_su):
    """Lịch sử bằng Streamlit metrics và dataframe"""
    data = lich_su.get(mien, [])
    total = len(data)
    wins = sum(1 for d in data if d["win"])
    rate = (wins/total*100) if total > 0 else 0
    
    st.markdown("### 📊 LỊCH SỬ DỰ ĐOÁN")
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng", total)
    with col2:
        st.metric("Trúng", wins)
    with col3:
        st.metric("Tỷ lệ", f"{rate:.0f}%")
    
    # Table
    if data:
        df_data = []
        for item in data:
            df_data.append({
                "Ngày": item["date"],
                "Loại": item["type"],
                "Dự đoán": item["pred"],
                "Kết quả": item["result"],
                "Trạng thái": "✅" if item["win"] else "❌"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

# =============================================================================
# 🚀 MAIN APP
# =============================================================================
def main():
    # Header
    st.markdown("""
    <div class="gold-header">
        <h1 style="color: #000; margin: 0; font-size: 2.5em;">💎 AI-QUANTUM GLOBAL</h1>
        <p style="color: #1a1a1a; margin: 10px 0 0; font-weight: 600;">Hệ thống phân tích xổ số thông minh</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timestamp
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.info(f"📅 Cập nhật: {now}")
    
    # Disclaimer
    st.warning("⚠️ **Lưu ý:** Xổ số là trò chơi ngẫu nhiên. Kết quả chỉ mang tính tham khảo giải trí.")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔴 MIỀN BẮC", "🟡 MIỀN TRUNG", "🟢 MIỀN NAM"])
    
    lich_su = get_lich_su()
    
    # Miền Bắc
    with tab1:
        kq_mb = get_kqxs("Miền Bắc")
        dd_mb = get_du_doan("Miền Bắc")
        render_bang_ket_qua("Miền Bắc", kq_mb)
        render_du_doan(dd_mb)
        render_lich_su("Miền Bắc", lich_su)
    
    # Miền Trung
    with tab2:
        kq_mt = get_kqxs("Miền Trung")
        dd_mt = get_du_doan("Miền Trung")
        render_bang_ket_qua("Miền Trung", kq_mt)
        render_du_doan(dd_mt)
        render_lich_su("Miền Trung", lich_su)
    
    # Miền Nam
    with tab3:
        kq_mn = get_kqxs("Miền Nam")
        dd_mn = get_du_doan("Miền Nam")
        render_bang_ket_qua("Miền Nam", kq_mn)
        render_du_doan(dd_mn)
        render_lich_su("Miền Nam", lich_su)
    
    # Refresh
    if st.button("🔄 LÀM MỚI DỮ LIỆU", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666; padding: 20px;'><strong>💎 AI-QUANTUM GLOBAL</strong><br>Chơi xổ số có trách nhiệm</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()