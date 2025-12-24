import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / 'src'))

from models.predict_xgboost import load_latest_model

st.set_page_config(
    page_title="Dự đoán Giá Nhà Việt Nam",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Ứng dụng Dự đoán Giá Nhà Việt Nam")
st.markdown("Nhập thông tin về ngôi nhà để dự đoán giá")

@st.cache_resource
def load_model_cached():
    return load_latest_model()

try:
    model, preprocessor, metadata = load_model_cached()
    st.sidebar.success("Đã tải model thành công!")
    st.sidebar.info(f"Model được train với {metadata['n_features']} features")
except Exception as e:
    st.error(f"Lỗi khi tải model: {str(e)}")
    st.stop()

provinces_list = [
    "", "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "An Giang", "Bà Rịa - Vũng Tàu", "Bạc Liêu", "Bắc Giang", "Bắc Kạn",
    "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước",
    "Bình Thuận", "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông",
    "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",
    "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình",
    "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu",
    "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định",
    "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên",
    "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị",
    "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên",
    "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang",
    "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
]

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        province = st.selectbox("Tỉnh/Thành phố", provinces_list)
        area = st.number_input("Diện tích (m²)", min_value=0.0, value=68.5, step=0.1)
        frontage = st.number_input("Mặt tiền (m)", min_value=0.0, value=5.0, step=0.1)
        access_road = st.number_input("Đường vào (m)", min_value=0.0, value=7.0, step=0.1)
        floors = st.number_input("Số tầng", min_value=1, max_value=10, value=3, step=1)
        bedrooms = st.number_input("Số phòng ngủ", min_value=1, max_value=9, value=3, step=1)
        bathrooms = st.number_input("Số phòng tắm", min_value=1, max_value=9, value=3, step=1)
    
    with col2:
        house_direction = st.selectbox(
            "Hướng nhà",
            ["", "Đông - Nam", "Đông - Bắc", "Tây - Nam", "Tây - Bắc", "Nam", "Bắc", "Đông", "Tây"]
        )
        balcony_direction = st.selectbox(
            "Hướng ban công",
            ["", "Đông - Nam", "Đông - Bắc", "Tây - Nam", "Tây - Bắc", "Nam", "Bắc", "Đông", "Tây"]
        )
        legal_status = st.selectbox(
            "Tình trạng pháp lý",
            ["", "Have certificate", "Sale contract"]
        )
        furniture_state = st.selectbox(
            "Tình trạng nội thất",
            ["", "Full", "Basic"]
        )
    
    submitted = st.form_submit_button("Dự đoán giá", use_container_width=True)

if submitted:
    with st.spinner("Đang xử lý và dự đoán..."):
        try:
            input_data = {
                'Area': [area],
                'Frontage': [frontage if frontage > 0 else np.nan],
                'Access Road': [access_road if access_road > 0 else np.nan],
                'House direction': [house_direction if house_direction else np.nan],
                'Balcony direction': [balcony_direction if balcony_direction else np.nan],
                'Floors': [floors if floors > 0 else np.nan],
                'Bedrooms': [bedrooms if bedrooms > 0 else np.nan],
                'Bathrooms': [bathrooms if bathrooms > 0 else np.nan],
                'Legal status': [legal_status if legal_status else np.nan],
                'Furniture state': [furniture_state if furniture_state else np.nan]
            }
            
            df_input = pd.DataFrame(input_data)
            
            df_input = preprocessor.handle_missing_values(df_input)
            
            categorical_cols = df_input.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                df_input = preprocessor.encode_features(df_input, categorical_cols)
            
            if preprocessor.feature_names:
                missing_features = set(preprocessor.feature_names) - set(df_input.columns)
                if missing_features:
                    df_input = df_input.reindex(columns=list(df_input.columns) + list(missing_features), fill_value=0)
                
                extra_features = set(df_input.columns) - set(preprocessor.feature_names)
                if extra_features:
                    df_input = df_input.drop(columns=list(extra_features))
                
                df_input = df_input[preprocessor.feature_names]
            
            X_scaled = preprocessor.scale_features(df_input)
            
            prediction = model.predict(X_scaled)[0]
            
            st.success("Dự đoán thành công!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Giá dự đoán", f"{prediction:.2f} tỷ VNĐ")
            with col2:
                st.metric("Giá dự đoán (USD)", f"${prediction * 40000:,.0f}")
            with col3:
                st.metric("Giá/m²", f"{prediction * 1000 / area:.0f} triệu VNĐ/m²" if area > 0 else "N/A")
            
            if province:
                st.info(f"📍 Vị trí: {province} (Lưu ý: Model hiện tại chưa sử dụng thông tin vị trí trong dự đoán)")
            st.info("⚠️ Lưu ý: Đây chỉ là dự đoán dựa trên mô hình machine learning. Giá thực tế có thể khác do nhiều yếu tố khác.")
            
        except Exception as e:
            st.error(f"Lỗi khi dự đoán: {str(e)}")
            st.exception(e)

st.markdown("---")
st.markdown("### Thông tin về model")
st.json(metadata)

