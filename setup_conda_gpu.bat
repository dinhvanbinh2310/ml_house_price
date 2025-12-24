@echo off
echo ========================================
echo Cai dat Conda va XGBoost GPU
echo ========================================
echo.

echo Buoc 1: Kiem tra Conda...
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Conda chua duoc cai dat!
    echo.
    echo Vui long:
    echo 1. Tai Miniconda tu: https://docs.conda.io/en/latest/miniconda.html
    echo 2. Cai dat va CHON "Add Miniconda3 to PATH"
    echo 3. Chay lai script nay
    pause
    exit /b 1
)

echo [OK] Conda da duoc cai dat
conda --version
echo.

echo Buoc 2: Tao moi truong conda...
conda create -n ml_house_price_gpu python=3.11 -y
if %errorlevel% neq 0 (
    echo [ERROR] Khong the tao moi truong
    pause
    exit /b 1
)
echo [OK] Da tao moi truong ml_house_price_gpu
echo.

echo Buoc 3: Cai XGBoost GPU...
call conda activate ml_house_price_gpu
conda install -c conda-forge py-xgboost-gpu -y
if %errorlevel% neq 0 (
    echo [WARNING] Co the khong cai duoc XGBoost GPU, thu lai...
    conda install -c conda-forge xgboost -y
)
echo.

echo Buoc 4: Cai cac package khac...
conda install pandas numpy scikit-learn matplotlib seaborn joblib jupyter notebook ipykernel tabulate -y
echo.

echo Buoc 5: Dang ky kernel cho Jupyter...
python -m ipykernel install --user --name=ml_house_price_gpu --display-name="Python (Conda GPU)"
echo.

echo ========================================
echo [HOAN TAT] Cai dat thanh cong!
echo ========================================
echo.
echo De su dung:
echo 1. Kich hoat moi truong: conda activate ml_house_price_gpu
echo 2. Mo Jupyter: jupyter notebook
echo 3. Chon kernel: Python (Conda GPU)
echo.
pause

