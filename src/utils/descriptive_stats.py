import pandas as pd
import numpy as np
from pathlib import Path

def generate_descriptive_stats(df, output_dir='report'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    stats = []
    
    for col in df.columns:
        col_stats = {'Column': col, 'Type': str(df[col].dtype)}
        
        if df[col].dtype in ['int64', 'float64']:
            col_stats['Min'] = df[col].min()
            col_stats['Max'] = df[col].max()
            col_stats['Mean'] = df[col].mean()
            col_stats['Median'] = df[col].median()
            col_stats['Std'] = df[col].std()
            col_stats['Missing_Rate'] = df[col].isna().sum() / len(df)
        else:
            col_stats['Unique_Count'] = df[col].nunique()
            col_stats['Most_Frequent'] = df[col].mode()[0] if len(df[col].mode()) > 0 else None
            col_stats['Missing_Rate'] = df[col].isna().sum() / len(df)
        
        stats.append(col_stats)
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv(output_dir / 'descriptive_stats.csv', index=False)
    
    md_content = "# Thống kê mô tả dữ liệu\n\n"
    md_content += f"Tổng số dòng: {len(df)}\n"
    md_content += f"Tổng số cột: {len(df.columns)}\n\n"
    md_content += "## Chi tiết từng cột\n\n"
    md_content += stats_df.to_markdown(index=False)
    
    with open(output_dir / 'descriptive_stats.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return stats_df

