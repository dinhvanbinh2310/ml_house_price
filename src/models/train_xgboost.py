import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from pathlib import Path
import joblib
import json
from datetime import datetime

def train_xgboost(X_train, y_train, use_grid_search=True, n_iter=50, cv=5, use_gpu=True):
    import subprocess
    gpu_available = False
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        gpu_available = result.returncode == 0
    except:
        pass
    
    gpu_supported = False
    if use_gpu and gpu_available:
        try:
            test_model = xgb.XGBRegressor(tree_method='gpu_hist', device='cuda', n_estimators=1)
            test_X = np.random.rand(10, 5)
            test_y = np.random.rand(10)
            test_model.fit(test_X, test_y)
            gpu_supported = True
        except:
            pass
    
    if gpu_supported:
        model = xgb.XGBRegressor(
            random_state=42,
            tree_method='gpu_hist',
            device='cuda'
        )
        print("Sử dụng GPU để train")
    else:
        model = xgb.XGBRegressor(random_state=42, n_jobs=-1)
        print("Sử dụng CPU để train")
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }
    
    if use_grid_search:
        search = GridSearchCV(
            model, param_grid, cv=cv, scoring='neg_mean_squared_error',
            n_jobs=-1, verbose=1
        )
    else:
        search = RandomizedSearchCV(
            model, param_grid, n_iter=n_iter, cv=cv,
            scoring='neg_mean_squared_error', n_jobs=-1, verbose=1, random_state=42
        )
    
    search.fit(X_train, y_train)
    
    best_model = search.best_estimator_
    
    return best_model, search.best_params_, search.best_score_

def save_model(model, preprocessor, metadata, output_dir='src/models'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_path = output_dir / f'xgboost_model_{timestamp}.pkl'
    preprocessor_path = output_dir / f'preprocessor_{timestamp}.pkl'
    metadata_path = output_dir / f'metadata_{timestamp}.json'
    
    joblib.dump(model, model_path)
    preprocessor.save(preprocessor_path)
    
    metadata['model_path'] = str(model_path)
    metadata['preprocessor_path'] = str(preprocessor_path)
    metadata['timestamp'] = timestamp
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return model_path, preprocessor_path, metadata_path

