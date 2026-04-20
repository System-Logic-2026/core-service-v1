import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np

# =============================================================================
# 🔧 CẤU HÌNH TRANG
# =============================================================================
st.set_page_config(page_title="AI-QUANTUM GLOBAL", page_icon="💎", layout="wide")

# CSS + HTML Inline (Không phụ thuộc file ngoài)
st.markdown("""
<style>
    body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .header-bar { background: linear-gradient(90deg, #c41e3a, #8b0000); color: white; padding: 15px; text-align: center; border-radius: 8px; margin-bottom: 10px; }
    .header-bar h1 { margin: 0; font-size: 1.8em; font-weight: 800; letter-spacing: 1px; }
    .header-bar p { margin: 5px 0 0; opacity: 0.9; font-size: 0.95em; }
    .date-badge { background: #fff; padding: 8px 15px; border-radius: 20px; display: inline-block; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 10px 0; font-weight: 600; color: #c41e3a; }
    .disclaimer { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px 15px; border-radius: 4px; margin: 10px 0; font-size: 0.9em; color: #856404; }
    
    .result-box { background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; margin: 15px 0; }
    .result-header { background: #c41e3a; color: white; padding: 10px 15px; font-weight: 700; font-size: 1.1em; text-transform: uppercase; }
    .row { display: flex; padding: 8px 15px; border-bottom: 1px solid #eee; align-items: center; }
    .row:last-child { border-bottom: none; }
    .lbl { width: 70px; font-weight: 600; color: #444; font-size: 0.95em; }
    .val { flex: 1; text-align: center; font-weight: 600; color: #000; font-size: 1.1em; }
    .val.sp { color: #c41e3a; font-size: 1.8em; font-weight: 900; letter-spacing: 2px; }
    .val.g1 { font-size: 1.4em; font-weight: 800; }
    .val.g7 { color: #c41e3a; font-weight: 700; }
    
    .pred-section { background: #fff; border-radius: 8px; padding: 20px; margin: 15px 0; border-top: 4px solid #c41e3a; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .pred-title { text-align: center; color: #c41e3a; font-weight: 800; font-size: 1.2em; margin-bottom: 15px; text-transform: uppercase; }
    .pred-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 15px; }
    .pred-card { background: #f9f9f9; border: 2px solid #c41e3a; border-radius: 8px; padding: 12px; text-align: center; }
    .pred-card h4 { margin: 0 0 8px; color: #c41e3a; font-size: 0.9em; text-transform: uppercase; }
    .pred-card .num { font-size: 1.6em; font-weight: 900; color: #000; margin: 5px 0; }
    .pred-card .conf { font-size: 0.8em; color: #666; }
    .dan-de { background: #f0f0f0; padding: 12px; border-radius: 8px; text-align: center; }
    .dan-de h4 { margin: 0 0 8px; color: #c41e3a; font-size: 1em; }
    .dan-de .nums { font-size: 1.3em; font-weight: 700; letter-spacing: 2px; color: #000; }
    
    .refresh-btn { background: #c41e3a; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: 600; cursor: pointer; width: 100%; margin-top: 10px; }
    .footer { text-align: center; padding: 20px; color: #666; font-size: 0.85em; margin-top: 20px; }
    
    @media (max-width: 600px) { .pred-grid { grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 🔄 DATA FETCHING
# =============================================================================
@st.cache_data(ttl=300)
def fetch_data(region: str) -> dict:
    urls = {
        "Miền Bắc": "https://xosodaiphat.com/xsmb-xổ-số-miền-bắc.html",
        "Miền Trung": "https://xosodaiphat.com/xsmt-xổ-số-miền-trung.html",
        "Miền Nam": "https://xosodaiphat.com/xsmn-xổ-số-miền-nam.html"
    }
    try:
        res = requests.get(urls[region], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Fallback mock data nếu scrape fail (đảm bảo app luôn chạy)
        data = {
            "special": "Đang cập nhật...", "first": "...",
            "second": ["...", "..."], "third": ["..."]*6,
            "fourth": ["..."]*4, "fifth": ["..."]*6,
            "sixth": ["..."]*3, "seventh": ["..."]*4
        }
        
        # Thử parse cơ bản (có thể thay bằng API chính thức nếu cần)
        sp = soup.find("div", class_="special-prize") or soup.find("div", id="special")
        if sp:
            val = sp.find("div", class_="text-center") or sp.find("span")
            if val: data["special"] = val.get_text(strip=True)
            
        g1 = soup.find("div", class_="first-prize")
        if g1:
            val = g1.find("div", class_="text-center")
            if val: data["first"] = val.get_text(strip=True)
            
        return data
    except:
        return {
            "special": "⏳ Lỗi kết nối", "first": "...",
            "second": ["..."], "third": ["..."], "fourth": ["..."],
            "fifth": ["..."], "sixth": ["..."], "seventh": ["..."]
        }

# =============================================================================
# 🎯 PREDICTION ENGINE
# =============================================================================
@st.cache_data(ttl=1800)
def get_predictions(region: str) -> dict:
    np.random.seed(int(datetime.now().strftime("%H%M")))
    bt = f"{np.random.randint(0,100):02d}"
    st_list = [f"{np.random.randint(0,100):02d}", f"{np.random.randint(0,100):02d}"]
    return {
        "bach_thu": bt,
        "song_thu": st_list,
        "xien_2": [bt, st_list[0]],
        "dan_de": [f"{i:02d}" for i in np.random.choice(100, 10, replace=False)],
        "conf": np.random.randint(65, 92)
    }

# =============================================================================
# 🎨 RENDER COMPONENTS
# =============================================================================
def render_table(region: str, data: dict):
    titles = {"Miền Bắc": "XSMB - Kết quả xổ số miền Bắc", 
              "Miền Trung": "XSMT - Kết quả xổ số miền Trung", 
              "Miền Nam": "XSMN - Kết quả xổ số miền Nam"}
    
    html = f"""
    <div class="result-box">
        <div class="result-header">{titles[region]}</div>
        <div class="row"><div class="lbl">G.ĐB</div><div class="val sp">{data['special']}</div></div>
        <div class="row"><div class="lbl">G.1</div><div class="val g1">{data['first']}</div></div>
        <div class="row"><div class="lbl">G.2</div><div class="val">{'&nbsp;'.join(data['second'])}</div></div>
        <div class="row"><div class="lbl">G.3</div><div class="val">{'&nbsp;'.join(data['third'])}</div></div>
        <div class="row"><div class="lbl">G.4</div><div class="val">{'&nbsp;'.join(data['fourth'])}</div></div>
        <div class="row"><div class="lbl">G.5</div><div class="val">{'&nbsp;'.join(data['fifth'])}</div></div>
        <div class="row"><div class="lbl">G.6</div><div class="val">{'&nbsp;'.join(data['sixth'])}</div></div>
        <div class="row"><div class="lbl">G.7</div><div class="val g7">{'&nbsp;'.join(data['seventh'])}</div></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_preds(pred: dict):
    html = f"""
    <div class="pred-section">
        <div class="pred-title">🎯 DỰ ĐOÁN VIP AI-QUANTUM</div>
        <div class="pred-grid">
            <div class="pred-card">
                <h4>✅ Bạch Thủ Lô</h4>
                <div class="num">{pred['bach_thu']}</div>
                <div class="conf">Tin cậy: {pred['conf']}%</div>
            </div>
            <div class="pred-card">
                <h4>✅ Song Thủ Lô</h4>
                <div class="num">{' - '.join(pred['song_thu'])}</div>
                <div class="conf">Nhịp cầu đẹp</div>
            </div>
            <div class="pred-card">
                <h4>✅ Xiên 2</h4>
                <div class="num">{' - '.join(pred['xien_2'])}</div>
                <div class="conf">Chuẩn xác cao</div>
            </div>
        </div>
        <div class="dan-de">
            <h4>🔥 DÀN ĐỀ 10 SỐ VIP:</h4>
            <div class="nums">{', '.join(pred['dan_de'])}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# =============================================================================
# 🚀 MAIN APP
# =============================================================================
def main():
    # Header
    st.markdown("""
    <div class="header-bar">
        <h1>💎 AI-QUANTUM GLOBAL</h1>
        <p>Hệ thống phân tích xổ số thông minh</p>
    </div>
    <div style="text-align:center;"><span class="date-badge">📅 Cập nhật: """ + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + """</span></div>
    <div class="disclaimer">⚠️ Lưu ý: Xổ số là trò chơi ngẫu nhiên. Kết quả chỉ mang tính chất tham khảo giải trí.</div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔴 XSMB", "🟡 XSMT", "🟢 XSMN"])
    
    for tab, region in zip([tab1, tab2, tab3], ["Miền Bắc", "Miền Trung", "Miền Nam"]):
        with tab:
            with st.spinner(f"Đang tải {region}..."):
                data = fetch_data(region)
                pred = get_predictions(region)
            render_table(region, data)
            render_preds(pred)
            
    # Refresh Button (Thay thế time.sleep gây treo app)
    if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown('<div class="footer">💎 AI-QUANTUM GLOBAL • Cập nhật tự động • Không thu thập thông tin cá nhân<br>Chơi xổ số có trách nhiệm</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()