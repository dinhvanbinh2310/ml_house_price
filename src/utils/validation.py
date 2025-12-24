from pathlib import Path
import pandas as pd

def validate_project_structure():
    required_dirs = [
        'data/raw',
        'data/processed',
        'src/preprocess',
        'src/models',
        'src/evaluation',
        'src/utils',
        'report/draft',
        'report/final',
        'slides',
        'environment'
    ]
    
    required_files = [
        'src/main.ipynb',
        'environment/requirements.txt',
        'environment/install.md',
        'README.md'
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    return missing_dirs, missing_files

def validate_dataset(data_path='data/raw'):
    data_path = Path(data_path)
    csv_files = list(data_path.glob('*.csv'))
    
    if not csv_files:
        return False, "Không tìm thấy file CSV"
    
    try:
        df = pd.read_csv(csv_files[0])
        n_rows = len(df)
        n_cols = len(df.columns)
        
        if n_rows < 500:
            return False, f"Dataset có {n_rows} dòng, cần >= 500"
        
        if n_cols < 5:
            return False, f"Dataset có {n_cols} cột, cần >= 5"
        
        return True, f"Dataset hợp lệ: {n_rows} dòng, {n_cols} cột"
    except Exception as e:
        return False, f"Lỗi khi đọc dataset: {str(e)}"

def generate_validation_report():
    missing_dirs, missing_files = validate_project_structure()
    dataset_valid, dataset_msg = validate_dataset()
    
    report = []
    report.append("BÁO CÁO KIỂM TRA DỰ ÁN")
    report.append("=" * 50)
    report.append("")
    
    report.append("1. CẤU TRÚC THƯ MỤC")
    report.append("-" * 30)
    if missing_dirs:
        report.append("❌ Thiếu thư mục:")
        for dir_path in missing_dirs:
            report.append(f"   - {dir_path}")
    else:
        report.append("✅ Tất cả thư mục đã có")
    report.append("")
    
    report.append("2. FILE CẦN THIẾT")
    report.append("-" * 30)
    if missing_files:
        report.append("❌ Thiếu file:")
        for file_path in missing_files:
            report.append(f"   - {file_path}")
    else:
        report.append("✅ Tất cả file đã có")
    report.append("")
    
    report.append("3. DATASET")
    report.append("-" * 30)
    if dataset_valid:
        report.append(f"✅ {dataset_msg}")
    else:
        report.append(f"❌ {dataset_msg}")
    report.append("")
    
    report.append("4. KIỂM TRA KHÁC")
    report.append("-" * 30)
    
    processed_files = list(Path('data/processed').glob('*.csv'))
    if processed_files:
        report.append(f"✅ Có {len(processed_files)} file dữ liệu đã xử lý")
    else:
        report.append("⚠️  Chưa có dữ liệu đã xử lý")
    
    model_files = list(Path('src/models').glob('*.pkl'))
    if model_files:
        report.append(f"✅ Có {len(model_files)} file model")
    else:
        report.append("⚠️  Chưa có model được lưu")
    
    eval_files = list(Path('src/evaluation').glob('*.png'))
    if eval_files:
        report.append(f"✅ Có {len(eval_files)} hình ảnh đánh giá")
    else:
        report.append("⚠️  Chưa có hình ảnh đánh giá")
    
    report.append("")
    report.append("=" * 50)
    
    report_text = "\n".join(report)
    
    with open('validation_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    return report_text

