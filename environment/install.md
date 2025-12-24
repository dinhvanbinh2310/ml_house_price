# Hướng dẫn cài đặt môi trường

## Yêu cầu
- Python >= 3.8
- pip

## Cài đặt

```bash
pip install -r environment/requirements.txt
```

## Cấu hình Kaggle API

1. Tải file kaggle.json từ https://www.kaggle.com/settings
2. Đặt file vào `~/.kaggle/kaggle.json` (Linux/Mac) hoặc `C:\Users\<username>\.kaggle\kaggle.json` (Windows)
3. Tải dataset:
```bash
kaggle datasets download -d nguyentiennhan/vietnam-housing-dataset-2024 -p data/raw/
unzip data/raw/vietnam-housing-dataset-2024.zip -d data/raw/
```

