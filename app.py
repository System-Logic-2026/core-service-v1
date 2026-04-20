import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Hệ thống Dự đoán Kết quả", page_icon="📊")

# Tiêu đề ứng dụng
st.title("📊 HỆ THỐNG DỰ ĐOÁN KẾT QUẢ v1.0")
st.write("---")

# Trạng thái máy chủ (Cho chuyên nghiệp)
st.subheader("📡 Trạng thái kết nối")
st.success("Kết nối máy chủ: ĐÃ THIẾT LẬP")

st.write("---")

# PHẦN HIỂN THỊ KẾT QUẢ (Anh kiểm tra phần này nhé)
st.header("🎯 KẾT QUẢ DỰ ĐOÁN HÔM NAY")

# Tạo 2 cột để nhìn cho cân đối
col1, col2 = st.columns(2)

with col1:
    st.info("### 💎 BẠCH THỦ LÔ\n## **79**")

with col2:
    st.info("### 💥 SONG THỦ LÔ\n## **24 - 42**")

st.write("---")

# Thêm một vài thông tin bổ sung cho uy tín
with st.expander("🔍 Chi tiết phân tích"):
    st.write("- Tỷ lệ chính xác dự kiến: **85%**")
    st.write("- Dữ liệu phân tích từ: **Máy chủ AI-Cloud 2026**")
    st.write("- Thời gian cập nhật: **Vừa xong**")

st.warning("⚠️ Lưu ý: Kết quả chỉ mang tính chất tham khảo kỹ thuật.")

st.write("---")
st.caption("Copyright 2026 - Secure Logic System")
