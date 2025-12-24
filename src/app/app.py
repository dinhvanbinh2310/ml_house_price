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
            
            if preprocessor.feature_names:
                df_final = pd.DataFrame(0, index=[0], columns=preprocessor.feature_names)
                
                categorical_cols = df_input.select_dtypes(include=['object']).columns.tolist()
                numeric_cols = df_input.select_dtypes(include=[np.number]).columns.tolist()
                
                for col in numeric_cols:
                    if col in df_final.columns:
                        df_final[col] = df_input[col].values[0]
                
                for col in categorical_cols:
                    value = str(df_input[col].values[0]) if pd.notna(df_input[col].values[0]) else 'nan'
                    for feature_name in preprocessor.feature_names:
                        if feature_name.startswith(f'{col}_'):
                            if feature_name.endswith(f'_{value}') or feature_name == f'{col}_{value}':
                                df_final[feature_name] = 1
                                break
                
                X_scaled = preprocessor.scale_features(df_final)
            else:
                categorical_cols = df_input.select_dtypes(include=['object']).columns.tolist()
                if categorical_cols:
                    df_input = preprocessor.encode_features(df_input, categorical_cols)
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

tab1, tab2, tab3 = st.tabs(["📊 Đánh giá Model", "📈 Biểu đồ", "ℹ️ Thông tin Model"])

with tab1:
    st.header("📊 Kết quả đánh giá Model")
    
    eval_dir = project_root / 'src' / 'evaluation'
    metrics_file = eval_dir / 'evaluation_metrics.txt'
    
    if metrics_file.exists():
        with open(metrics_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        metrics_dict = {}
        for line in lines[3:]:
            if ':' in line:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    try:
                        value = float(parts[1].strip())
                        metrics_dict[key] = value
                    except:
                        pass
        
        if metrics_dict:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("RMSE", f"{metrics_dict.get('RMSE', 0):.4f}", 
                         help="Root Mean Squared Error - càng nhỏ càng tốt")
            with col2:
                st.metric("MAE", f"{metrics_dict.get('MAE', 0):.4f}",
                         help="Mean Absolute Error - càng nhỏ càng tốt")
            with col3:
                st.metric("MAPE", f"{metrics_dict.get('MAPE', 0):.2f}%",
                         help="Mean Absolute Percentage Error - càng nhỏ càng tốt")
            with col4:
                st.metric("R²", f"{metrics_dict.get('R2', 0):.4f}",
                         help="R-squared - càng gần 1 càng tốt")
            
            st.markdown("---")
            st.markdown("**Giải thích metrics:**")
            st.markdown("""
            - **RMSE (Root Mean Squared Error)**: Độ lệch trung bình bình phương, đo độ chính xác tổng thể
            - **MAE (Mean Absolute Error)**: Độ lệch trung bình tuyệt đối, dễ hiểu hơn RMSE
            - **MAPE (Mean Absolute Percentage Error)**: Phần trăm lỗi trung bình, cho biết độ chính xác theo %
            - **R² (R-squared)**: Hệ số xác định, cho biết model giải thích được bao nhiêu % phương sai
            """)
        else:
            st.text(metrics_content)
    else:
        st.info("Chưa có file đánh giá metrics")
    
    st.markdown("---")
    st.subheader("Thông tin Model")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Số features", metadata.get('n_features', 'N/A'))
        st.metric("Số mẫu train", metadata.get('n_train_samples', 'N/A'))
    with col2:
        st.metric("Số mẫu test", metadata.get('n_test_samples', 'N/A'))
        if 'best_cv_score' in metadata:
            st.metric("CV Score (MSE)", f"{metadata['best_cv_score']:.4f}")

with tab2:
    st.header("📈 Biểu đồ đánh giá")
    
    eval_dir = project_root / 'src' / 'evaluation'
    
    img1_path = eval_dir / 'predictions_vs_actual.png'
    img2_path = eval_dir / 'residuals.png'
    img3_path = eval_dir / 'feature_importance.png'
    
    if img1_path.exists():
        st.subheader("Predictions vs Actual")
        st.image(str(img1_path), use_container_width=True)
        st.caption("So sánh giá trị dự đoán với giá trị thực tế. Đường chéo đỏ là đường lý tưởng (y=x).")
    else:
        st.info("Chưa có hình ảnh predictions vs actual")
    
    if img2_path.exists():
        st.subheader("Residuals Analysis")
        st.image(str(img2_path), use_container_width=True)
        st.caption("Phân tích phần dư (residuals) để kiểm tra tính ngẫu nhiên của lỗi.")
    else:
        st.info("Chưa có hình ảnh residuals")
    
    if img3_path.exists():
        st.subheader("Feature Importance (Top 20)")
        st.image(str(img3_path), use_container_width=True)
        st.caption("Top 20 features quan trọng nhất trong model.")
    else:
        st.info("Chưa có hình ảnh feature importance")

with tab3:
    st.header("ℹ️ Thông tin về Model")
    
    if 'best_params' in metadata:
        st.subheader("Hyperparameters")
        params = metadata['best_params']
        for key, value in params.items():
            st.text(f"{key}: {value}")
    
    st.subheader("Metadata đầy đủ")
    st.json(metadata)

