# Hướng dẫn Deploy App lên Streamlit Community Cloud

## Yêu cầu

1. Tài khoản GitHub
2. Tài khoản Streamlit Community Cloud (đăng ký tại https://share.streamlit.io/)

## Các bước deploy

### 1. Chuẩn bị repository GitHub

Đảm bảo project đã được push lên GitHub:

```bash
git init
git add .
git commit -m "Initial commit - House price prediction app"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

**Lưu ý quan trọng:**
- Model files (`.pkl`, `.joblib`) trong `src/models/` phải được commit vào repo
- File `requirements.txt` phải ở root directory
- File `streamlit_app.py` phải ở root directory

### 2. Deploy lên Streamlit Community Cloud

1. Truy cập https://share.streamlit.io/
2. Đăng nhập bằng tài khoản GitHub
3. Click "New app"
4. Điền thông tin:
   - **Repository**: Chọn repository của bạn
   - **Branch**: `main` (hoặc branch chứa code)
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Tên app (ví dụ: `house-price-prediction`)
5. Click "Deploy"

### 3. Cấu trúc file cần thiết

```
project/
├── requirements.txt          # Dependencies (ở root)
├── streamlit_app.py          # Entry point (ở root)
├── .streamlit/
│   └── config.toml           # Streamlit config
├── src/
│   ├── app/
│   │   └── app.py            # Main app code
│   ├── models/
│   │   ├── *.pkl             # Model files (phải có trong repo)
│   │   └── *.json            # Metadata files
│   ├── preprocess/
│   │   └── preprocess.py
│   └── utils/
└── README.md
```

### 4. Kiểm tra sau khi deploy

Sau khi deploy thành công, kiểm tra:

- App có load được model không?
- Các dependencies có được cài đặt đúng không?
- App có chạy được không?

### 5. Troubleshooting

**Lỗi: ModuleNotFoundError**
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Kiểm tra import paths trong code

**Lỗi: FileNotFoundError - Model not found**
- Đảm bảo model files (`.pkl`, `.json`) đã được commit vào repo
- Kiểm tra path trong `load_latest_model()`

**Lỗi: Memory limit exceeded**
- Model quá lớn (>1GB) có thể gây vấn đề
- Cân nhắc giảm số features hoặc sử dụng model nhẹ hơn

**Lỗi: Timeout**
- Tối ưu code với `@st.cache_resource` (đã có trong app)
- Giảm thời gian xử lý

### 6. Cập nhật app

Sau khi thay đổi code:

1. Commit và push lên GitHub
2. Streamlit Cloud sẽ tự động redeploy
3. Hoặc vào dashboard và click "Reboot app"

## Lưu ý

- Streamlit Community Cloud miễn phí nhưng có giới hạn:
  - CPU và RAM hạn chế
  - App sẽ sleep sau 7 ngày không dùng
  - Public apps only

- Để deploy private apps hoặc có nhiều resources hơn, sử dụng Snowflake hoặc tự host.

## Tham khảo

- [Streamlit Community Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Deploying Streamlit Apps](https://docs.streamlit.io/deploy)

