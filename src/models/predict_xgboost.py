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
    
    with open(metadata_files[0], 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    model = joblib.load(metadata['model_path'])
    preprocessor = DataPreprocessor.load(metadata['preprocessor_path'])
    
    return model, preprocessor, metadata

