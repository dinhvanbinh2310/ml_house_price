# Hướng dẫn Setup GitHub Repository

## Bước 1: Tạo Repository trên GitHub

1. Truy cập https://github.com/new
2. Điền thông tin:
   - **Repository name**: `ML_house_price` (hoặc tên bạn muốn)
   - **Description**: "House price prediction app using XGBoost"
   - **Visibility**: Public (để deploy Streamlit Cloud miễn phí)
   - **Không** tích "Initialize with README" (vì đã có code local)
3. Click "Create repository"

## Bước 2: Thêm Remote và Push Code

Sau khi tạo repository, GitHub sẽ hiển thị URL. Copy URL đó và chạy:

```bash
# Thêm remote (thay YOUR_USERNAME và REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Hoặc nếu dùng SSH:
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Kiểm tra remote đã được thêm
git remote -v

# Push code lên GitHub
git push -u origin master
```

## Bước 3: Nếu branch là `main` thay vì `master`

```bash
# Đổi tên branch
git branch -M main

# Push lên main
git push -u origin main
```

## Lưu ý

- Đảm bảo đã commit tất cả files cần thiết
- Model files phải được commit (không ignore)
- File `.gitignore` đã được cấu hình đúng

