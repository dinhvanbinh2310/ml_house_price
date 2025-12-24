# Các bước Deploy lên Streamlit Community Cloud

## Bước 1: Đảm bảo code đã push lên GitHub

Kiểm tra:
```bash
git status
# Nếu có thay đổi chưa commit, commit và push:
git add .
git commit -m "Add deployment files"
git push origin main
```

## Bước 2: Đăng ký/Đăng nhập Streamlit Community Cloud

1. Truy cập: https://share.streamlit.io/
2. Click "Sign in" hoặc "Get started"
3. Chọn "Continue with GitHub"
4. Authorize Streamlit để truy cập GitHub repositories

## Bước 3: Deploy App

1. Sau khi đăng nhập, click **"New app"** (góc trên bên phải)

2. Điền thông tin:
   - **Repository**: Chọn `dinhvanbinh2310/ml_house_price`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Tên bạn muốn (ví dụ: `vietnam-house-price` hoặc `ml-house-price`)
     - URL sẽ là: `https://vietnam-house-price.streamlit.app`

3. Click **"Deploy"**

## Bước 4: Chờ Deploy

- Streamlit sẽ tự động:
  - Cài đặt dependencies từ `requirements.txt`
  - Chạy `streamlit_app.py`
  - Deploy app

- Thời gian: Khoảng 2-5 phút

## Bước 5: Kiểm tra Logs

Nếu có lỗi:
1. Click vào app vừa deploy
2. Click menu (☰) góc trên bên phải
3. Chọn "Manage app"
4. Xem "Logs" để debug

## Lưu ý quan trọng

✅ **Đảm bảo model files đã được commit:**
```bash
git ls-files src/models/
# Phải thấy: *.pkl, *.json files
```

✅ **Kiểm tra requirements.txt ở root:**
```bash
ls requirements.txt
```

✅ **Kiểm tra streamlit_app.py ở root:**
```bash
ls streamlit_app.py
```

## Troubleshooting

**Lỗi: ModuleNotFoundError**
- Kiểm tra `requirements.txt` có đầy đủ packages
- Xem logs để biết package nào thiếu

**Lỗi: FileNotFoundError - Model not found**
- Đảm bảo model files đã được commit:
```bash
git add src/models/*.pkl src/models/*.json
git commit -m "Add model files"
git push origin main
```

**Lỗi: Memory limit**
- Model quá lớn có thể gây vấn đề
- Cân nhắc giảm số features hoặc sử dụng model nhẹ hơn

## Sau khi deploy thành công

App sẽ có URL dạng:
`https://<app-name>.streamlit.app`

Bạn có thể:
- Share URL này với người khác
- Embed vào website
- Update code và app sẽ tự động redeploy

