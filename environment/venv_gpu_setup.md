# Hướng dẫn cài XGBoost GPU trong venv

## Tóm tắt

Có thể dùng venv, nhưng cần build XGBoost từ source với CUDA. Quá trình này phức tạp và yêu cầu:

1. **CUDA Toolkit 11.6** (đã có driver, cần toolkit đầy đủ)
2. **CMake** (build system)
3. **Visual Studio Build Tools** (compiler C++)
4. **Git** (để clone source code)

## So sánh các cách

| Cách | Độ khó | Thời gian | Khuyến nghị |
|------|--------|-----------|-------------|
| Conda | ⭐ Dễ | 5-10 phút | ✅ Khuyến nghị |
| Build từ source | ⭐⭐⭐⭐ Khó | 30-60 phút | ⚠️ Nếu muốn dùng venv |

## Khuyến nghị

**Nếu muốn dùng GPU nhanh:** Dùng Conda (Cách 1 trong `gpu_setup.md`)

**Nếu bắt buộc dùng venv:** Build từ source (Cách 2 trong `gpu_setup.md`)

**Nếu không cần GPU ngay:** Tiếp tục dùng CPU với `n_jobs=-1` (đã nhanh với dataset này)

## Kiểm tra sau khi cài

Chạy: `python test_gpu_xgboost.py`

