# Hướng dẫn cài đặt Conda và XGBoost GPU

## Bước 1: Tải và cài Miniconda

1. Truy cập: https://docs.conda.io/en/latest/miniconda.html
2. Tải **Miniconda3 Windows 64-bit** (Python 3.x)
3. Chạy file `.exe` đã tải
4. Trong quá trình cài:
   - ✅ Chọn "Add Miniconda3 to PATH" (quan trọng!)
   - ✅ Chọn "Register Miniconda3 as the system Python"
5. Hoàn tất cài đặt

## Bước 2: Mở terminal mới và kiểm tra

```bash
conda --version
```

Nếu hiển thị version (ví dụ: `conda 24.x.x`) là thành công.

## Bước 3: Tạo môi trường conda với XGBoost GPU

Chạy các lệnh sau:

```bash
conda create -n ml_house_price_gpu python=3.11 -y
conda activate ml_house_price_gpu
conda install -c conda-forge py-xgboost-gpu -y
conda install pandas numpy scikit-learn matplotlib seaborn joblib jupyter notebook ipykernel tabulate -y
```

## Bước 4: Đăng ký kernel cho Jupyter

```bash
python -m ipykernel install --user --name=ml_house_price_gpu --display-name="Python (Conda GPU)"
```

## Bước 5: Sử dụng trong Jupyter

1. Mở Jupyter Notebook
2. Chọn kernel: **Kernel → Change Kernel → Python (Conda GPU)**
3. Chạy lại notebook

## Kiểm tra GPU

Chạy trong notebook:
```python
import xgboost as xgb
import numpy as np

X = np.random.rand(100, 10)
y = np.random.rand(100)

model = xgb.XGBRegressor(tree_method='gpu_hist', device='cuda', n_estimators=10)
model.fit(X, y)
print("GPU hoạt động!")
```

