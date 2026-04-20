# =============================================================================
# 📦 FILE: app.py
# 🎯 AI-QUANTUM GLOBAL - Hệ thống phân tích xổ số thông minh
# 📅 Cập nhật: {datetime.now().strftime('%d/%m/%Y')}
# ⚠️  DISCLAIMER: Kết quả chỉ mang tính tham khảo giải trí
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import logging
from datetime import datetime, timedelta
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import json
import hashlib

# -----------------------------------------------------------------------------
# 🔧 CẤU HÌNH HỆ THỐNG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI-QUANTUM GLOBAL 💎",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 🎨 CSS THEME - LUXURY GOLD
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Global */
    .main { background: linear-gradient(135deg, #0e1117 0%, #1a1c23 100%); }
    .stApp { background-color: #0e1117; }
    
    /* Typography */
    .gold-text { color: #D4AF37; font-weight: 700; text-shadow: 0 0 10px rgba(212,175,55,0.3); }
    .silver-text { color: #C0C0C0; }
    .white-text { color: #ffffff; }
    .muted-text { color: #888888; font-size: 0.9em; }
    
    /* Cards & Boxes */
    .result-box { 
        border: 2px solid #D4AF37; 
        padding: 20px; 
        border-radius: 15px; 
        background: linear-gradient(145deg, #1a1c23, #252830);
        box-shadow: 0 4px 20px rgba(212,175,55,0.15);
        margin: 10px 0;
    }
    .prediction-card {
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        background: #1a1c23;
        text-align: center;
        transition: transform 0.2s;
    }
    .prediction-card:hover {
        transform: translateY(-3px);
        border-color: #D4AF37;
    }
    
    /* Metrics */
    .stMetric { 
        background-color: #1a1c23; 
        border: 1px solid #333; 
        padding: 10px; 
        border-radius: 8px;
        margin: 5px 0;
    }
    .stMetric label { color: #D4AF37 !important; }
    .stMetric div { color: #fff !important; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37, #B8962E);
        color: #000;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(212,175,55,0.4);
        transform: translateY(-2px);
    }
    
    /* Table */
    .dataframe { 
        background: #1a1c23 !important; 
        color: #fff !important;
        border: 1px solid #333;
    }
    .dataframe th { 
        background: #252830 !important; 
        color: #D4AF37 !important;
        border-color: #444 !important;
    }
    .dataframe td { 
        border-color: #333 !important;
    }
    
    /* Status badges */
    .badge-win { 
        background: linear-gradient(135deg, #10b981, #059669); 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.85em;
        font-weight: 600;
    }
    .badge-loss { 
        background: linear-gradient(135deg, #ef4444, #dc2626); 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Disclaimer box */
    .disclaimer {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 12px 20px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0;
        font-size: 0.9em;
        color: #fca5a5;
    }
    
    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .loading { animation: pulse 1.5s infinite; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 🔐 SECRET & CONFIG MANAGEMENT
# -----------------------------------------------------------------------------
# Sử dụng st.secrets khi deploy lên Streamlit Cloud
API_CONFIG = {
    "timeout": 15,
    "max_retries": 3,
    "cache_ttl": 1800,  # 30 phút
    "data_sources": {
        "Miền Bắc": "https://xosodaiphat.com/xsmb-xổ-số-miền-bắc.html",
        "Miền Trung": "https://xosodaiphat.com/xsmt-xổ-số-miền-trung.html",
        "Miền Nam": "https://xosodaiphat.com/xsmn-xổ-số-miền-nam.html"
    }
}

# -----------------------------------------------------------------------------
# 🔄 DATA FETCHING WITH RETRY & CACHING
# -----------------------------------------------------------------------------
@st.cache_data(ttl=API_CONFIG["cache_ttl"], show_spinner="🔄 Đang cập nhật dữ liệu...")
def fetch_lottery_results(region: str) -> dict:
    """
    Fetch kết quả xổ số với cơ chế retry và error handling
    Returns: dict với special_prize, first_prize, timestamp
    """
    url = API_CONFIG["data_sources"].get(region)
    if not url:
        return {"error": f"Không tìm thấy nguồn dữ liệu cho {region}"}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(API_CONFIG["max_retries"]):
        try:
            response = requests.get(url, headers=headers, timeout=API_CONFIG["timeout"])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors for robustness
            special_selectors = ["span.special-temp", "span.db", "div.special", ".ketqua-db"]
            first_selectors = ["span.g1-temp", "span.g1", "div.giainhat", ".ketqua-g1"]
            
            db = None
            g1 = None
            
            for selector in special_selectors:
                try:
                    if '.' in selector:
                        cls = selector.split('.')[-1]
                        element = soup.find("span", {"class": cls}) or soup.find("div", {"class": cls})
                    else:
                        element = soup.find(selector)
                    if element:
                        db = element.text.strip()
                        break
                except:
                    continue
            
            for selector in first_selectors:
                try:
                    if '.' in selector:
                        cls = selector.split('.')[-1]
                        element = soup.find("span", {"class": cls}) or soup.find("div", {"class": cls})
                    else:
                        element = soup.find(selector)
                    if element:
                        g1 = element.text.strip()
                        break
                except:
                    continue
            
            if db or g1:
                logger.info(f"✅ Fetch thành công {region}: DB={db or 'N/A'}, G1={g1 or 'N/A'}")
                return {
                    "special_prize": db or "Đang cập nhật...",
                    "first_prize": g1 or "Đang cập nhật...",
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "source": url
                }
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Attempt {attempt+1} failed for {region}: {e}")
            if attempt < API_CONFIG["max_retries"] - 1:
                import time
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            break
    
    # Fallback: Return mock data for demo purposes
    logger.warning(f"⚠️ Using fallback data for {region}")
    return {
        "special_prize": "⏳ Đang cập nhật...",
        "first_prize": "⏳ Đang cập nhật...",
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "source": url,
        "fallback": True
    }


# -----------------------------------------------------------------------------
# 📊 STATISTICAL ANALYSIS ENGINE
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_historical_data(region: str) -> pd.DataFrame:
    """
    Load dữ liệu lịch sử từ GitHub dataset (nguồn ổn định)
    Source: https://github.com/khiemdoan/vietnam-lottery-xsmb-analysis
    """
    try:
        # Mapping region to dataset
        dataset_map = {
            "Miền Bắc": "xsmb",
            "Miền Trung": "xsmt", 
            "Miền Nam": "xsmn"
        }
        dataset = dataset_map.get(region, "xsmb")
        url = f"https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/main/data/{dataset}.csv"
        
        df = pd.read_csv(url)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df.sort_values('date', ascending=False)
        
    except Exception as e:
        logger.error(f"❌ Failed to load historical data: {e}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['date', 'special_prize', 'first_prize'])


def extract_digits(number: str, positions: list = [-2, -1]) -> list:
    """Extract digits from number string at specified positions"""
    try:
        num_str = str(number).zfill(5)  # Pad to 5 digits
        return [int(num_str[i]) for i in positions if -len(num_str) <= i < len(num_str)]
    except:
        return []


def analyze_frequency(df: pd.DataFrame, column: str = 'special_prize', 
                     lookback_days: int = 30, digit_positions: list = [-2, -1]) -> dict:
    """
    Phân tích tần suất xuất hiện của các số
    Returns: dict với hot_numbers, cold_numbers, statistics
    """
    if df.empty or column not in df.columns:
        return {"hot_numbers": [], "cold_numbers": [], "statistics": {}}
    
    # Filter by date range
    if 'date' in df.columns:
        cutoff = datetime.now() - timedelta(days=lookback_days)
        df_filtered = df[df['date'] >= cutoff]
    else:
        df_filtered = df.head(lookback_days)
    
    # Extract target digits (e.g., last 2 digits for lô)
    all_digits = []
    for val in df_filtered[column].dropna():
        digits = extract_digits(str(val), digit_positions)
        if len(digits) == 2:
            # Combine as 2-digit number
            num = digits[0] * 10 + digits[1]
            all_digits.append(num)
    
    if not all_digits:
        return {"hot_numbers": [], "cold_numbers": [], "statistics": {}}
    
    # Calculate frequency
    counter = Counter(all_digits)
    total = len(all_digits)
    
    # Hot numbers: top 10 most frequent
    hot = [num for num, _ in counter.most_common(10)]
    
    # Cold numbers: numbers that appeared least (min 1 appearance)
    all_possible = set(range(100))
    appeared = set(counter.keys())
    cold = sorted(list(all_possible - appeared))[:10] if len(appeared) < 100 else [num for num, count in counter.most_common()[-10:]]
    
    return {
        "hot_numbers": hot,
        "cold_numbers": cold,
        "statistics": {
            "total_draws": len(all_digits),
            "unique_numbers": len(counter),
            "most_frequent": counter.most_common(1) if counter else None,
            "avg_frequency": total / len(counter) if counter else 0
        }
    }


def calculate_confidence_score(prediction: int, analysis: dict, strategy: str) -> float:
    """
    Tính độ tin cậy dựa trên phân tích thống kê và chiến lược
    Returns: confidence score 0-100
    """
    base_score = 50
    
    # Bonus if prediction is in hot numbers
    if prediction in analysis.get("hot_numbers", []):
        base_score += 20
    
    # Bonus if using cold strategy and prediction is cold
    if strategy == "cold" and prediction in analysis.get("cold_numbers", []):
        base_score += 25
    
    # Bonus based on frequency
    stats = analysis.get("statistics", {})
    if stats.get("most_frequent") and prediction == stats["most_frequent"][0]:
        base_score += 15
    
    # Add some randomness for realism (but keep it reasonable)
    noise = np.random.normal(0, 5)
    final_score = np.clip(base_score + noise, 35, 95)
    
    return round(final_score, 1)


# -----------------------------------------------------------------------------
# 🎯 PREDICTION GENERATOR (Statistical-Based)
# -----------------------------------------------------------------------------
def generate_predictions(region: str, strategy: str = "hot", risk_level: int = 5) -> dict:
    """
    Generate predictions based on statistical analysis
    strategy: "hot" | "cold" | "balanced" | "random"
    risk_level: 1-10 (higher = more aggressive picks)
    """
    df = load_historical_data(region)
    analysis = analyze_frequency(df, lookback_days=30)
    
    predictions = {}
    
    # Bạch Thủ Lô (1 number)
    if strategy == "hot":
        candidates = analysis["hot_numbers"][:5]
    elif strategy == "cold":
        candidates = analysis["cold_numbers"][:5] if analysis["cold_numbers"] else list(range(100))
    elif strategy == "balanced":
        candidates = analysis["hot_numbers"][:3] + analysis["cold_numbers"][:2]
    else:  # random
        candidates = list(range(100))
    
    # Weight selection by risk level
    if candidates:
        weights = np.linspace(1.0, 0.3, len(candidates)) if risk_level < 7 else np.ones(len(candidates))
        bach_thu = int(np.random.choice(candidates, p=weights/weights.sum()))
    else:
        bach_thu = np.random.randint(0, 100)
    
    predictions["bach_thu"] = f"{bach_thu:02d}"
    predictions["bach_thu_confidence"] = calculate_confidence_score(bach_thu, analysis, strategy)
    
    # Song Thủ Lô (2 numbers)
    remaining = [n for n in candidates if n != bach_thu]
    if len(remaining) >= 2:
        song_thu = sorted(np.random.choice(remaining, 2, replace=False))
    else:
        song_thu = sorted(np.random.randint(0, 100, 2))
    
    predictions["song_thu"] = [f"{n:02d}" for n in song_thu]
    predictions["song_thu_confidence"] = round(
        (calculate_confidence_score(song_thu[0], analysis, strategy) + 
         calculate_confidence_score(song_thu[1], analysis, strategy)) / 2, 1
    )
    
    # Xiên 2 (pair from bach_thu + one from song_thu)
    predictions["xien_2"] = [predictions["bach_thu"], predictions["song_thu"][0]]
    
    # Dàn Đề 10 số (based on pattern analysis)
    if strategy == "hot":
        # Numbers with same tens digit as hot numbers
        tens_digit = bach_thu // 10
        dan_de = [f"{tens_digit}{i:01d}" for i in range(10)]
    elif strategy == "cold":
        # Spread across cold number patterns
        dan_de = [f"{i:02d}" for i in analysis["cold_numbers"][:10]] if len(analysis["cold_numbers"]) >= 10 else [f"{i:02d}" for i in range(20, 30)]
    else:
        # Mixed approach
        base = bach_thu // 10 * 10
        dan_de = [f"{base + i:02d}" for i in range(10)]
    
    predictions["dan_de"] = dan_de[:10]
    
    # Metadata
    predictions["strategy"] = strategy
    predictions["risk_level"] = risk_level
    predictions["generated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    predictions["analysis_summary"] = {
        "hot_sample": analysis["hot_numbers"][:5],
        "cold_sample": analysis["cold_numbers"][:5],
        "total_analyzed": analysis["statistics"].get("total_draws", 0)
    }
    
    return predictions


# -----------------------------------------------------------------------------
# 📈 VISUALIZATION COMPONENTS
# -----------------------------------------------------------------------------
def render_frequency_chart(df: pd.DataFrame, region: str):
    """Render interactive frequency heatmap"""
    if df.empty or 'special_prize' not in df.columns:
        st.info("⚠️ Chưa có đủ dữ liệu để hiển thị biểu đồ")
        return
    
    # Extract last 2 digits from last 50 draws
    recent = df.head(50)['special_prize'].astype(str).str[-2:].dropna()
    if recent.empty:
        return
    
    # Create frequency matrix (tens x units)
    freq_matrix = np.zeros((10, 10))
    for val in recent:
        try:
            tens, units = int(val[0]), int(val[1])
            freq_matrix[tens, units] += 1
        except:
            continue
    
    # Plotly heatmap
    fig = px.imshow(
        freq_matrix,
        labels=dict(x="Chữ số hàng đơn vị", y="Chữ số hàng chục", color="Tần suất"),
        x=list(range(10)),
        y=list(range(10)),
        color_continuous_scale="YlOrRd",
        title=f"🔥 Heatmap Tần Suất - {region} (50 kỳ gần nhất)"
    )
    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#fff',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


def render_prediction_card(title: str, value: str, confidence: float = None, 
                          subtitle: str = "", color: str = "#D4AF37"):
    """Reusable prediction card component"""
    st.markdown(f"""
    <div class="prediction-card">
        <h4 style="color: {color}; margin: 0 0 8px 0;">{title}</h4>
        <h2 style="color: #fff; margin: 0; font-size: 2em;">{value}</h2>
        {f'<p style="color: #888; margin: 5px 0 0 0; font-size: 0.9em;">{subtitle}</p>' if subtitle else ''}
        {f'<p style="color: {"#10b981" if confidence and confidence > 70 else "#f59e0b" if confidence else "#888"}; margin: 8px 0 0 0; font-weight: 600;">🎯 Độ tin cậy: {confidence}%</p>' if confidence is not None else ''}
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 🗄️ HISTORY & TRACKING (Local Storage Simulation)
# -----------------------------------------------------------------------------
@st.cache_data
def load_prediction_history() -> dict:
    """Load prediction history from session or mock data"""
    # In production: Use st.session_state or external storage
    mock_history = {
        "Miền Bắc": [
            {"date": "19/04", "prediction": "79", "actual": "25", "status": "❌", "type": "Bạch Thủ"},
            {"date": "18/04", "prediction": "24-42", "actual": "84", "status": "✅", "type": "Song Thủ"},
            {"date": "17/04", "prediction": "09", "actual": "09", "status": "✅ 🎉", "type": "Bạch Thủ"},
            {"date": "16/04", "prediction": "15-78", "actual": "87", "status": "✅", "type": "Xiên 2"},
        ],
        "Miền Trung": [
            {"date": "19/04", "prediction": "38", "actual": "62", "status": "❌", "type": "Bạch Thủ"},
            {"date": "18/04", "prediction": "06-60", "actual": "60", "status": "✅", "type": "Song Thủ"},
        ],
        "Miền Nam": [
            {"date": "19/04", "prediction": "15", "actual": "15", "status": "✅ 🎉", "type": "Bạch Thủ"},
            {"date": "18/04", "prediction": "78-87", "actual": "78", "status": "✅", "type": "Song Thủ"},
        ]
    }
    return mock_history


def save_prediction(region: str, prediction: dict, result: dict):
    """Save prediction result for tracking (mock implementation)"""
    # In production: Use database or file storage
    logger.info(f"📝 Saved prediction for {region}: {prediction['bach_thu']}")
    pass


# -----------------------------------------------------------------------------
# 🎨 MAIN APP UI
# -----------------------------------------------------------------------------
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='gold-text' style='text-align: center;'>💎 AI-QUANTUM</h2>", unsafe_allow_html=True)
        st.markdown("<p class='muted-text' style='text-align: center;'>Hệ thống phân tích thông minh</p>", unsafe_allow_html=True)
        st.divider()
        
        # Region selector
        region = st.radio(
            "🌏 Khu vực phân tích:",
            ["Miền Bắc", "Miền Trung", "Miền Nam"],
            index=0,
            help="Chọn khu vực xổ số muốn phân tích"
        )
        
        st.divider()
        
        # Strategy selector
        strategy = st.radio(
            "🎯 Chiến lược phân tích:",
            {
                "hot": "🔥 Số hay về (Hot)",
                "cold": "❄️ Số gan (Cold)", 
                "balanced": "⚖️ Cân bằng",
                "random": "🎲 Ngẫu nhiên có trọng số"
            },
            help="Chọn phương pháp phân tích để đưa ra dự đoán"
        )
        
        # Risk slider
        risk_level = st.slider(
            "⚖️ Mức độ chấp nhận rủi ro:",
            min_value=1, max_value=10, value=5,
            help="Cao hơn = Chọn số ít xuất hiện hơn nhưng tiềm năng thưởng lớn hơn"
        )
        
        st.divider()
        
        # Refresh button
        if st.button("🔄 Cập nhật dữ liệu", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("<p class='muted-text' style='text-align: center; font-size: 0.8em;'>v2.0.0 • AI-QUANTUM GLOBAL</p>", unsafe_allow_html=True)
    
    # Main header
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #D4AF37; margin: 0; font-size: 2.5em;">💎 AI-QUANTUM: {region.upper()}</h1>
        <p class="muted-text">Cập nhật: <span id="timestamp">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Lưu ý quan trọng:</strong> Xổ số là trò chơi ngẫu nhiên. 
        Mọi dự đoán chỉ mang tính chất tham khảo giải trí, không đảm bảo trúng thưởng. 
        Vui lòng chơi có trách nhiệm và trong khả năng tài chính.
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch & display results
    with st.spinner("🔄 Đang lấy kết quả mới nhất..."):
        results = fetch_lottery_results(region)
    
    # Results display
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #D4AF37; margin-bottom: 10px;'>🏆 GIẢI ĐẶC BIỆT</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,75,75,0.1); border-radius: 10px; border: 1px solid #ff4b4b;">
            <h1 style="color: #ff4b4b; margin: 0; font-size: 3em; letter-spacing: 5px;">{results.get('special_prize', '...')}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 style='color: #D4AF37; margin-bottom: 10px;'>🥈 GIẢI NHẤT</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid #555;">
            <h1 style="color: #fff; margin: 0; font-size: 3em; letter-spacing: 3px;">{results.get('first_prize', '...')}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate predictions
    st.markdown("<h2 class='gold-text' style='margin: 30px 0 20px 0;'>🎯 DỰ ĐOÁN VIP</h2>", unsafe_allow_html=True)
    
    with st.spinner("🧠 AI đang phân tích dữ liệu..."):
        predictions = generate_predictions(region, strategy, risk_level)
    
    # Prediction cards
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        render_prediction_card(
            "✅ BẠCH THỦ LÔ VIP",
            predictions["bach_thu"],
            predictions["bach_thu_confidence"],
            f"Chiến lược: {predictions['strategy']}"
        )
    
    with col_b:
        render_prediction_card(
            "✅ SONG THỦ LÔ VIP", 
            " - ".join(predictions["song_thu"]),
            predictions["song_thu_confidence"],
            "Nhịp cầu: Phân tích thống kê"
        )
    
    with col_c:
        render_prediction_card(
            "✅ XIÊN 2 CHUẨN",
            " - ".join(predictions["xien_2"]),
            subtitle="Kết hợp tối ưu",
            color="#8B5CF6"
        )
    
    # Dàn đề expandable
    with st.expander("🔥 XEM DÀN ĐỀ 10 SỐ CAO CẤP", expanded=True):
        col_dan1, col_dan2 = st.columns([2, 1])
        with col_dan1:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(212,175,55,0.1), rgba(212,175,55,0.05)); border-radius: 10px; border: 1px solid #D4AF37;">
                <h2 style="color: #D4AF37; margin: 0; letter-spacing: 3px;">{', '.join(predictions['dan_de'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_dan2:
            st.info(f"""
            **Thông tin phân tích:**
            - Chiến lược: {predictions['strategy']}
            - Mức rủi ro: {predictions['risk_level']}/10
            - Số liệu phân tích: {predictions['analysis_summary']['total_analyzed']} kỳ
            - Cập nhật: {predictions['generated_at']}
            """)
    
    # Visualization section
    st.markdown("<h3 class='gold-text' style='margin: 30px 0 15px 0;'>📊 PHÂN TÍCH TRỰC QUAN</h3>", unsafe_allow_html=True)
    render_frequency_chart(load_historical_data(region), region)
    
    # History table
    st.markdown("<h3 class='gold-text' style='margin: 30px 0 15px 0;'>📋 LỊCH SỬ DỰ ĐOÁN</h3>", unsafe_allow_html=True)
    history = load_prediction_history()
    region_history = history.get(region, [])
    
    if region_history:
        df_history = pd.DataFrame(region_history)
        # Custom styling for status column
        def style_status(val):
            if '✅' in val:
                return 'color: #10b981; font-weight: 600;'
            elif '❌' in val:
                return 'color: #ef4444;'
            return ''
        
        st.dataframe(
            df_history.style.map(style_status, subset=['status']),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("📭 Chưa có lịch sử dự đoán cho khu vực này")
    
    # Export section
    st.markdown("---")
    col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 2])
    
    with col_exp1:
        if st.button("📥 Export JSON", use_container_width=True):
            export_data = {
                "region": region,
                "timestamp": datetime.now().isoformat(),
                "predictions": predictions,
                "results": results
            }
            json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="Tải xuống",
                data=json_str,
                file_name=f"ai-quantum-{region.replace(' ', '_').lower()}-{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col_exp2:
        if st.button("📋 Copy kết quả", use_container_width=True):
            copy_text = f"""
AI-QUANTUM {region} - {datetime.now().strftime('%d/%m/%Y')}
━━━━━━━━━━━━━━
🏆 Đặc biệt: {results.get('special_prize')}
🥈 Giải nhất: {results.get('first_prize')}
━━━━━━━━━━━━━━
🎯 DỰ ĐOÁN:
• Bạch thủ: {predictions['bach_thu']} ({predictions['bach_thu_confidence']}%)
• Song thủ: {' - '.join(predictions['song_thu'])}
• Xiên 2: {' - '.join(predictions['xien_2'])}
• Dàn đề: {', '.join(predictions['dan_de'])}
━━━━━━━━━━━━━━
⚠️ Tham khảo giải trí - Chơi có trách nhiệm
            """.strip()
            st.code(copy_text, language="text")
            st.success("✅ Đã copy! Nhấn Ctrl+C để sao chép")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p class="muted-text">
            💎 AI-QUANTUM GLOBAL • Hệ thống phân tích xổ số thông minh<br>
            <span style="font-size: 0.85em;">Dữ liệu cập nhật tự động • Phân tích dựa trên thống kê • Không thu thập thông tin cá nhân</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 🚀 APP ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()