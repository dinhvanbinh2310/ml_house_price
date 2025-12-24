import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def calculate_regression_metrics(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'R2': r2
    }

def plot_predictions(y_true, y_pred, output_dir='src/evaluation', title='Predictions'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Giá trị thực tế')
    plt.ylabel('Giá trị dự đoán')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    plt.savefig(output_dir / f'{title.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_residuals(y_true, y_pred, output_dir='src/evaluation'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].scatter(y_pred, residuals, alpha=0.5)
    axes[0].axhline(y=0, color='r', linestyle='--')
    axes[0].set_xlabel('Giá trị dự đoán')
    axes[0].set_ylabel('Residuals')
    axes[0].set_title('Residual Plot')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].hist(residuals, bins=30, edgecolor='black')
    axes[1].set_xlabel('Residuals')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Residual Distribution')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'residuals.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_feature_importance(model, feature_names, output_dir='src/evaluation', top_n=20):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title(f'Top {top_n} Feature Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        plt.savefig(output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()

def save_evaluation_report(metrics, output_dir='src/evaluation'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / 'evaluation_metrics.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH\n")
        f.write("=" * 50 + "\n\n")
        for metric, value in metrics.items():
            f.write(f"{metric}: {value:.4f}\n")
    
    report_md_path = Path('report') / 'evaluation.md'
    report_md_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = "# Đánh giá mô hình\n\n"
    md_content += "## Metrics\n\n"
    md_content += "| Metric | Giá trị |\n"
    md_content += "|--------|----------|\n"
    for metric, value in metrics.items():
        md_content += f"| {metric} | {value:.4f} |\n"
    
    md_content += "\n## Giải thích metrics\n\n"
    md_content += "- **RMSE (Root Mean Squared Error)**: Độ lệch trung bình bình phương, càng nhỏ càng tốt\n"
    md_content += "- **MAE (Mean Absolute Error)**: Độ lệch trung bình tuyệt đối, càng nhỏ càng tốt\n"
    md_content += "- **MAPE (Mean Absolute Percentage Error)**: Phần trăm lỗi trung bình, càng nhỏ càng tốt\n"
    md_content += "- **R2 (R-squared)**: Hệ số xác định, càng gần 1 càng tốt\n"
    
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

