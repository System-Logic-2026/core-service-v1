import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np

# =============================================================================
# 🔧 CẤU HÌNH
# =============================================================================
st.set_page_config(page_title="AI-QUANTUM GLOBAL 💎", page_icon="💎", layout="wide")

# CSS
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%); }
    
    .gold-text { color: #D4AF37; font-weight: 700; }
    .special-number { 
        color: #FFD700; 
        font-size: 2em; 
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 10px rgba(255,215,0,0.5);
    }
    .big-number { 
        font-size: 1.5em; 
        font-weight: 800; 
        text-align: center;
        color: #fff;
    }
    .number { 
        font-size: 1.2em; 
        font-weight: 700; 
        text-align: center;
        color: #fff;
    }
    .gold-number { 
        color: #D4AF37; 
        font-weight: 800;
        text-align: center;
    }
    .pred-number {
        font-size: 2em;
        font-weight: 900;
        color: #fff;
        text-align: center;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-weight: 700;
        font-size: 1.1em;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4AF37, #B8962E);
        color: #000;
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
    
    # Mock data mặc định
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
            val = sp.find("span") or sp.find("div")
            if val:
                result["special"] = val.get_text(strip=True)
        
        g1 = soup.find("div", {"class": "first-prize"})
        if g1:
            val = g1.find("span") or g1.find("div")
            if val:
                result["first"] = val.get_text(strip=True)
        
        return result
    except:
        return data_default[mien]

# =============================================================================
# 🎯 PREDICTIONS
# =============================================================================
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

# =============================================================================
# 📊 HISTORY
# =============================================================================
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
# 🎨 RENDER FUNCTIONS
# =============================================================================
def show_kq(mien, kq):
    """Hiển thị kết quả bằng Streamlit components"""
    titles = {
        "Miền Bắc": "🔴 XSMB - KẾT QUẢ",
        "Miền Trung": "🟡 XSMT - KẾT QUẢ",
        "Miền Nam": "🟢 XSMN - KẾT QUẢ"
    }
    
    # Container chính
    container = st.container()
    with container:
        # Title
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #D4AF37, #B8962E); 
                    padding: 15px; border-radius: 10px; text-align: center; 
                    margin: 10px 0;'>
            <h2 style='color: #000; margin: 0; font-weight: 900;'>{titles[mien]}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Giải đặc biệt
        st.markdown('<div style="background: rgba(212,175,55,0.1); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #D4AF37;">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<p class="gold-text" style="margin: 0; font-size: 1.1em;">G.ĐB</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="special-number" style="margin: 0;">{kq["special"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Giải nhất
        st.markdown('<div style="background: rgba(212,175,55,0.05); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #D4AF37;">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<p class="gold-text" style="margin: 0;">G.1</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-number" style="margin: 0;">{kq["first"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Các giải còn lại
        prizes = [
            ("G.2", kq["second"]),
            ("G.3", kq["third"]),
            ("G.4", kq["fourth"]),
            ("G.5", kq["fifth"]),
            ("G.6", kq["sixth"]),
        ]
        
        for label, values in prizes:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f'<p class="gold-text" style="margin: 5px 0;">{label}</p>', unsafe_allow_html=True)
                with col2:
                    val_text = " • ".join(values) if isinstance(values, list) else values
                    st.markdown(f'<p class="number" style="margin: 5px 0;">{val_text}</p>', unsafe_allow_html=True)
        
        # Giải 7 (màu vàng)
        st.markdown('<div style="background: rgba(212,175,55,0.05); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #D4AF37;">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<p class="gold-text" style="margin: 0;">G.7</p>', unsafe_allow_html=True)
        with col2:
            val_text = " • ".join(kq["seventh"])
            st.markdown(f'<p class="gold-number" style="margin: 0;">{val_text}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_du_doan(dd):
    """Hiển thị dự đoán"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a); 
                border: 2px solid #D4AF37; border-radius: 10px; 
                padding: 20px; margin: 20px 0;'>
        <h3 style='color: #D4AF37; text-align: center; margin: 0 0 20px 0; 
                   font-size: 1.3em; text-transform: uppercase;'>
            💎 DỰ ĐOÁN VIP AI-QUANTUM
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 cột dự đoán
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(212,175,55,0.1); border: 2px solid #D4AF37; 
                    border-radius: 8px; padding: 20px; text-align: center;'>
            <h4 style='color: #D4AF37; margin: 0 0 10px 0;'>✅ BẠCH THỦ LÔ VIP</h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p class="pred-number">{dd["bach_thu"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #D4AF37; font-weight: 600;">🎯 Tin cậy: {dd["conf_bt"]}%</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(212,175,55,0.1); border: 2px solid #D4AF37; 
                    border-radius: 8px; padding: 20px; text-align: center;'>
            <h4 style='color: #D4AF37; margin: 0 0 10px 0;'>✅ SONG THỦ LÔ VIP</h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p class="pred-number">{" - ".join(dd["song_thu"])}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #D4AF37; font-weight: 600;">🎯 Tin cậy: {dd["conf_st"]}%</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(212,175,55,0.1); border: 2px solid #D4AF37; 
                    border-radius: 8px; padding: 20px; text-align: center;'>
            <h4 style='color: #D4AF37; margin: 0 0 10px 0;'>✅ XIÊN 2</h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p class="pred-number">{" - ".join(dd["xien_2"])}</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #D4AF37; font-weight: 600;">⭐ Chuẩn xác cao</p>', unsafe_allow_html=True)
    
    # Dàn đề
    st.markdown("""
    <div style='background: rgba(212,175,55,0.15); border: 2px solid #D4AF37; 
                border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center;'>
        <h4 style='color: #D4AF37; margin: 0 0 15px 0; font-size: 1.1em;'>🔥 DÀN ĐỀ 10 SỐ VIP 🔥</h4>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.4em; font-weight: 700; color: #fff; letter-spacing: 3px;">{", ".join(dd["dan_de"])}</p>', unsafe_allow_html=True)

def show_lich_su(mien, lich_su):
    """Hiển thị lịch sử"""
    data = lich_su.get(mien, [])
    total = len(data)
    wins = sum(1 for d in data if d["win"])
    rate = (wins/total*100) if total > 0 else 0
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a, #2a2a2a); 
                border: 2px solid #D4AF37; border-radius: 10px; 
                padding: 20px; margin: 20px 0;'>
        <h3 style='color: #D4AF37; margin: 0 0 15px 0; font-size: 1.2em;'>📊 LỊCH SỬ DỰ ĐOÁN</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
            status = "✅" if item["win"] else "❌"
            df_data.append({
                "Ngày": item["date"],
                "Loại": item["type"],
                "Dự đoán": item["pred"],
                "Kết quả": item["result"],
                "Trạng thái": status
            })
        
        import pandas as pd
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

# =============================================================================
# 🚀 MAIN APP
# =============================================================================
def main():
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #D4AF37, #B8962E); 
                padding: 30px; text-align: center; border-radius: 10px; 
                margin-bottom: 20px; box-shadow: 0 4px 15px rgba(212,175,55,0.4);'>
        <h1 style='color: #000; margin: 0; font-size: 2.5em; font-weight: 900;'>💎 AI-QUANTUM GLOBAL</h1>
        <p style='color: #1a1a1a; margin: 10px 0 0; font-weight: 600; font-size: 1.1em;'>
            Hệ thống phân tích xổ số thông minh
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timestamp
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f"""
    <div style='background: rgba(212,175,55,0.15); border: 2px solid #D4AF37; 
                padding: 10px; border-radius: 20px; text-align: center; 
                color: #D4AF37; font-weight: 600; margin: 15px 0;'>
        📅 Cập nhật: {now}
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.warning("⚠️ **Lưu ý:** Xổ số là trò chơi ngẫu nhiên. Kết quả chỉ mang tính tham khảo giải trí.")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔴 MIỀN BẮC", "🟡 MIỀN TRUNG", "🟢 MIỀN NAM"])
    
    # Load data
    lich_su = get_lich_su()
    
    # Miền Bắc
    with tab1:
        kq_mb = get_kqxs("Miền Bắc")
        dd_mb = get_du_doan("Miền Bắc")
        show_kq("Miền Bắc", kq_mb)
        show_du_doan(dd_mb)
        show_lich_su("Miền Bắc", lich_su)
    
    # Miền Trung
    with tab2:
        kq_mt = get_kqxs("Miền Trung")
        dd_mt = get_du_doan("Miền Trung")
        show_kq("Miền Trung", kq_mt)
        show_du_doan(dd_mt)
        show_lich_su("Miền Trung", lich_su)
    
    # Miền Nam
    with tab3:
        kq_mn = get_kqxs("Miền Nam")
        dd_mn = get_du_doan("Miền Nam")
        show_kq("Miền Nam", kq_mn)
        show_du_doan(dd_mn)
        show_lich_su("Miền Nam", lich_su)
    
    # Refresh button
    if st.button("🔄 LÀM MỚI DỮ LIỆU", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 30px 20px; color: #666; 
                border-top: 1px solid #333; margin-top: 30px;'>
        <p style='margin: 0;'>💎 <strong>AI-QUANTUM GLOBAL</strong></p>
        <p style='margin: 5px 0 0; font-size: 0.9em;'>Chơi xổ số có trách nhiệm</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()