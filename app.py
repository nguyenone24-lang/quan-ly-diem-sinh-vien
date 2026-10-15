import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Tạo dữ liệu DataFrame ban đầu cho 10 sinh viên
data = {
    'Ho_ten': ['An', 'Binh', 'Chi', 'Dung', 'Ha', 'Lan', 'Minh', 'Nam', 'Phuc', 'Trang'],
    'Chuyen_can': [9.0, 8.0, 7.5, 10.0, 6.5, 8.5, 9.0, 7.0, 8.0, 9.5],
    'Giua_ky': [7.0, 8.5, 6.0, 9.0, 5.5, 7.5, 8.0, 6.5, 7.0, 8.5],
    'Cuoi_ky': [8.0, 7.5, 6.5, 9.5, 6.0, 8.0, 8.5, 7.0, 7.5, 9.0]
}
df = pd.DataFrame(data)

# 2. Tính điểm tổng kết (20% Chuyên cần, 30% Giữa kỳ, 50% Cuối kỳ)
df['Tong_ket'] = (0.2 * df['Chuyen_can']) + (0.3 * df['Giua_ky']) + (0.5 * df['Cuoi_ky'])
df['Tong_ket'] = df['Tong_ket'].round(2)

# 3. Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# 4. Thống kê cơ bản
dtb_lop = df['Tong_ket'].mean()
sv_max = df.loc[df['Tong_ket'].idxmax()]
sv_min = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()


# ==========================================
# GIAO DIỆN WEB APP STREAMLIT
# ==========================================

# Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm chi tiết
st.subheader("Bảng điểm chi tiết của lớp")
st.dataframe(df, use_container_width=True)

# Hiển thị các thông tin thống kê
st.subheader("Thống kê chung")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình lớp", value=f"{dtb_lop:.2f}")
    st.metric(label="Số sinh viên đạt (>= 5.0)", value=f"{so_sv_dat}/10")
with col2:
    st.metric(label="Điểm cao nhất", value=f"{sv_max['Ho_ten']} ({sv_max['Tong_ket']}đ)")
    st.metric(label="Điểm thấp nhất", value=f"{sv_min['Ho_ten']} ({sv_min['Tong_ket']}đ)")

# Tạo danh sách xổ xuống (Selectbox) tra cứu sinh viên
st.subheader("Tra cứu thông tin cá nhân sinh viên")
chon_sv = st.selectbox("Chọn tên sinh viên:", df['Ho_ten'])

thong_tin_sv = df[df['Ho_ten'] == chon_sv].iloc[0]
st.info(f"""
* **Họ tên:** {thong_tin_sv['Ho_ten']}
* **Điểm chuyên cần:** {thong_tin_sv['Chuyen_can']}
* **Điểm giữa kỳ:** {thong_tin_sv['Giua_ky']}
* **Điểm cuối kỳ:** {thong_tin_sv['Cuoi_ky']}
* **Điểm tổng kết:** **{thong_tin_sv['Tong_ket']}**
* **Xếp loại:** **{thong_tin_sv['Xep_loai']}**
""")

# Hiển thị biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ phân bố điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df['Ho_ten'], df['Tong_ket'], color='skyblue', edgecolor='black')
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)

for i, txt in enumerate(df['Tong_ket']):
    ax.text(i, txt + 0.2, str(txt), ha='center', fontsize=9)

st.pyplot(fig)

# Chân trang hiển thị họ tên và MSSV chữ nhỏ
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: small; color: gray;'>Họ tên: [Phan Trọng Nguyên] - MSSV: [054208005729]</p>", unsafe_allow_html=True)