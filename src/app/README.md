# Ứng dụng Demo Dự đoán Giá Nhà

Ứng dụng web demo sử dụng Streamlit để dự đoán giá nhà dựa trên các thông tin đầu vào.

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r environment/requirements.txt
```

Hoặc chỉ cài Streamlit:
```bash
pip install streamlit
```

## Chạy ứng dụng

Từ thư mục gốc của project:

```bash
streamlit run src/app/app.py
```

Hoặc từ thư mục `src/app`:

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tự động trong trình duyệt tại địa chỉ `http://localhost:8501`

## Sử dụng

1. Nhập các thông tin về ngôi nhà:
   - Diện tích (m²)
   - Mặt tiền (m)
   - Đường vào (m)
   - Số tầng
   - Số phòng ngủ
   - Số phòng tắm
   - Hướng nhà
   - Hướng ban công
   - Tình trạng pháp lý
   - Tình trạng nội thất

2. Click nút "Dự đoán giá"

3. Xem kết quả dự đoán

## Lưu ý

- Model sẽ tự động load model mới nhất từ thư mục `src/models/`
- Một số trường có thể để trống (sẽ được xử lý tự động)
- Giá dự đoán chỉ mang tính tham khảo

