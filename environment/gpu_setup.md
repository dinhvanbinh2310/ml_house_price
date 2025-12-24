# Hướng dẫn cài đặt XGBoost với GPU Support

## Yêu cầu
- GPU: NVIDIA GeForce (đã có ✓)
- CUDA: 11.6 (đã có ✓)
- Python: 3.x (đã có trong venv)

## Cách 1: Dùng Conda (Khuyến nghị - Dễ nhất)

### Bước 1: Cài Miniconda hoặc Anaconda
Tải từ: https://docs.conda.io/en/latest/miniconda.html

### Bước 2: Tạo môi trường conda mới
```bash
conda create -n ml_house_price python=3.13
conda activate ml_house_price
```

### Bước 3: Cài XGBoost với GPU support
```bash
conda install -c conda-forge py-xgboost-gpu
conda install pandas numpy scikit-learn matplotlib seaborn joblib jupyter notebook ipykernel tabulate
```

### Bước 4: Đăng ký kernel cho Jupyter
```bash
python -m ipykernel install --user --name=ml_house_price_gpu --display-name="Python (conda GPU)"
```

## Cách 2: Build XGBoost từ source với CUDA trong venv (Phức tạp)

### Bước 1: Cài CUDA Toolkit (nếu chưa có đầy đủ)
Tải CUDA Toolkit 11.6 từ: https://developer.nvidia.com/cuda-11-6-0-download-archive

### Bước 2: Cài CMake và Visual Studio Build Tools
- CMake: https://cmake.org/download/
- Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
  - Chọn "Desktop development with C++" và "CUDA" components

### Bước 3: Kích hoạt venv và cài dependencies
```bash
venv\Scripts\activate
pip install numpy scipy wheel setuptools
```

### Bước 4: Clone và build XGBoost
```bash
git clone --recursive https://github.com/dmlc/xgboost
cd xgboost
mkdir build
cd build
cmake .. -DUSE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES="75;80;86" -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

### Bước 5: Cài XGBoost đã build vào venv
```bash
cd ../python-package
python setup.py install
```

**Lưu ý:** Cách này phức tạp và có thể gặp lỗi. Conda vẫn là cách đơn giản nhất.

## Cách 3: Dùng pip với wheel có sẵn (Nếu có)

Một số wheel có sẵn GPU support, nhưng thường không có cho Windows.

## Kiểm tra GPU support

Sau khi cài, chạy script này để kiểm tra:

```python
import xgboost as xgb
import numpy as np

X = np.random.rand(100, 10)
y = np.random.rand(100)

try:
    model = xgb.XGBRegressor(tree_method='gpu_hist', device='cuda', n_estimators=10)
    model.fit(X, y)
    print("✓ GPU support hoạt động!")
except Exception as e:
    print(f"✗ GPU support không hoạt động: {e}")
```

## Lưu ý

- Cách 1 (Conda) là dễ nhất và khuyến nghị
- Nếu dùng conda, bạn có thể tạo môi trường mới hoặc migrate từ venv hiện tại
- Code trong `train_xgboost.py` đã tự động phát hiện và dùng GPU nếu có

