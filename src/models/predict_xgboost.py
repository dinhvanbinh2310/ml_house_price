import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from preprocess.preprocess import DataPreprocessor

def load_model(model_path, preprocessor_path):
    model = joblib.load(model_path)
    preprocessor = DataPreprocessor.load(preprocessor_path)
    return model, preprocessor

def predict(model, preprocessor, X):
    if isinstance(X, pd.DataFrame):
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        if categorical_cols:
            X = preprocessor.encode_features(X, categorical_cols)
        X = X[preprocessor.feature_names] if preprocessor.feature_names else X
        X_scaled = preprocessor.scale_features(X)
    else:
        X_scaled = X
    
    predictions = model.predict(X_scaled)
    return predictions

def load_latest_model(models_dir='src/models'):
    models_dir = Path(models_dir)
    metadata_files = sorted(models_dir.glob('metadata_*.json'), reverse=True)
    
    if not metadata_files:
        raise FileNotFoundError("Không tìm thấy model nào")
    
    metadata_file = metadata_files[0]
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    model_path_str = metadata['model_path'].replace('\\', '/')
    preprocessor_path_str = metadata['preprocessor_path'].replace('\\', '/')
    
    model_path = Path(model_path_str)
    preprocessor_path = Path(preprocessor_path_str)
    
    if not model_path.is_absolute():
        model_path = models_dir / model_path.name
    if not preprocessor_path.is_absolute():
        preprocessor_path = models_dir / preprocessor_path.name
    
    if not model_path.exists():
        raise FileNotFoundError(f"Không tìm thấy model file: {model_path}")
    if not preprocessor_path.exists():
        raise FileNotFoundError(f"Không tìm thấy preprocessor file: {preprocessor_path}")
    
    model = joblib.load(model_path)
    preprocessor = DataPreprocessor.load(preprocessor_path)
    
    return model, preprocessor, metadata

