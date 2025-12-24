# Checklist trước khi Deploy

## ✅ Files cần thiết

- [x] `requirements.txt` ở root directory
- [x] `streamlit_app.py` ở root directory  
- [x] `.streamlit/config.toml` (optional, đã tạo)
- [x] Model files trong `src/models/` (phải commit vào git)

## ✅ Kiểm tra Git

- [ ] Đã init git repository
- [ ] Đã commit tất cả files cần thiết
- [ ] Model files (`.pkl`, `.json`) đã được commit
- [ ] Đã push lên GitHub

**Lưu ý:** Kiểm tra `.gitignore` không ignore model files:
```bash
git check-ignore src/models/*.pkl
# Nếu có output, cần sửa .gitignore
```

## ✅ Kiểm tra Dependencies

- [ ] `requirements.txt` có đầy đủ packages
- [ ] Không có conflicts về version
- [ ] `protobuf<=3.20.3` (quan trọng cho Streamlit)

## ✅ Kiểm tra Code

- [ ] App chạy được local: `streamlit run streamlit_app.py`
- [ ] Model load được thành công
- [ ] Predict hoạt động đúng
- [ ] Không có lỗi import

## ✅ Kiểm tra Paths

- [ ] Tất cả paths trong code dùng relative paths
- [ ] Không có hardcoded absolute paths
- [ ] Model paths đúng với cấu trúc thư mục

## ✅ Test Local

Trước khi deploy, test với:
```bash
streamlit run streamlit_app.py
```

Đảm bảo:
- [ ] App load được
- [ ] Model load được
- [ ] Predict hoạt động
- [ ] UI hiển thị đúng

## 📝 Thông tin Deploy

Sau khi deploy, lưu lại:
- [ ] GitHub repository URL: `_________________`
- [ ] Streamlit app URL: `_________________`
- [ ] Deploy status: `_________________`

## 🐛 Nếu có lỗi

Xem [DEPLOY.md](DEPLOY.md) phần Troubleshooting

