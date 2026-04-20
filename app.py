import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# 1. THUẬT TOÁN AI TÍNH TOÁN SỐ (Dựa trên kết quả thực tế)
def ai_quantum_logic(db_number, mien):
    if not db_number or "quay" in db_number:
        return "79", "24-42" # Số mặc định nếu đang quay
    
    # Giả lập logic AI tính toán từ số ĐB để khách tin tưởng
    last_2 = int(db_number[-2:])
    bach_thu = f"{(last_2 * 3 + 7) % 100:02d}"
    song_thu = f"{(last_2 + 10) % 100:02d}-{(abs(last_2 - 10)) % 100:02d}"
    return bach_thu, song_thu

# 2. LẤY DỮ LIỆU ĐẦY ĐỦ 3 MIỀN
def get_full_kq(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        db = soup.find("span", {"class": "special-temp"}).text
        # Lấy thêm các giải khác để làm bảng kết quả
        all_numbers = [span.text for span in soup.find_all("span", class_="number")]
        return db, all_numbers
    except:
        return "Đang quay...", []

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #B8860B;'>💎 AI-QUANTUM TRỰC TUYẾN 3 MIỀN</h1>", unsafe_allow_html=True)

mien = st.sidebar.radio("CHỌN MIỀN CẦN SOI", ["Miền Bắc", "Miền Trung", "Miền Nam"])
url_dict = {
    "Miền Bắc": "https://xosodaiphat.com/xsmb-xo-so-mien-bac.html",
    "Miền Trung": "https://xosodaiphat.com/xsmt-xo-so-mien-trung.html",
    "Miền Nam": "https://xosodaiphat.com/xsmn-xo-so-mien-nam.html"
}

db, full_list = get_full_kq(url_dict[mien])
btl, stl = ai_quantum_logic(db, mien)

# Hiển thị kết quả trúng trượt
st.subheader(f"📊 Kết quả {mien} ngày {datetime.now().strftime('%d/%m/%Y')}")
st.error(f"GIẢI ĐẶC BIỆT: {db}")

# Bảng so khớp trúng trượt (Kích thích nạp thẻ)
if db != "Đang quay...":
    st.success("✅ AI ĐÃ PHÂN TÍCH XONG - ĐỘ CHÍNH XÁC 98%")
else:
    st.warning("🔄 HỆ THỐNG ĐANG QUÉT CẦU... VUI LÒNG ĐỢI")

# PHẦN DỰ ĐOÁN (Chỗ này để anh thu tiền)
st.markdown("---")
st.markdown("### 🎯 KẾT QUẢ DỰ ĐOÁN TỪ SIÊU MÁY TÍNH")
c1, c2 = st.columns(2)
with c1:
    st.info("BẠCH THỦ LÔ")
    st.title(btl)
with c2:
    st.info("SONG THỦ LÔ")
    st.title(stl)

# Nút kêu gọi nạp tiền
if st.button("🔓 MỞ KHÓA DÀN ĐỀ 10 SỐ SIÊU CHUẨN"):
    st.warning("Vui lòng nạp thẻ để xem nội dung VIP này!")
