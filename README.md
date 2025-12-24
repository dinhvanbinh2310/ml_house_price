# Đồ án Khai thác Dữ liệu - Dự đoán Giá Nhà Việt Nam

## Mô tả
Dự án sử dụng XGBoost để dự đoán giá nhà ở Việt Nam dựa trên dataset từ Kaggle.

## Dataset
- Nguồn: https://www.kaggle.com/datasets/nguyentiennhan/vietnam-housing-dataset-2024
- Lưu tại: `data/raw/`

## Cấu trúc dự án
```
data/raw/              - Dữ liệu gốc
data/processed/        - Dữ liệu đã xử lý
src/preprocess/        - Script tiền xử lý
src/models/            - Model và metadata
src/evaluation/        - Kết quả đánh giá
src/utils/             - Utility functions
src/main.ipynb         - Notebook chính
report/                - Báo cáo
slides/                - Slides thuyết trình
```

## Cài đặt
Xem `environment/install.md`

## Sử dụng

### Chạy local
1. Tải dataset vào `data/raw/`
2. Chạy `src/main.ipynb` để thực hiện toàn bộ pipeline
3. Chạy app Streamlit:
```bash
streamlit run src/app/app.py
```

### Deploy lên Streamlit Community Cloud
Xem hướng dẫn chi tiết trong [DEPLOY.md](DEPLOY.md)

Tóm tắt:
1. Push code lên GitHub
2. Đăng ký tại https://share.streamlit.io/
3. Connect repository và deploy
4. App sẽ tự động deploy tại URL: `https://<app-name>.streamlit.app`

