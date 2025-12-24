import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from pathlib import Path
import joblib

class DataPreprocessor:
    def __init__(self, missing_strategy='mean', outlier_method='iqr', 
                 encoding_method='onehot', scaling_method='standard'):
        self.missing_strategy = missing_strategy
        self.outlier_method = outlier_method
        self.encoding_method = encoding_method
        self.scaling_method = scaling_method
        
        self.scaler = None
        self.encoders = {}
        self.feature_names = None
        
    def handle_missing_values(self, df):
        df = df.copy()
        
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if df[col].dtype in ['int64', 'float64']:
                    if self.missing_strategy == 'mean':
                        df[col].fillna(df[col].mean(), inplace=True)
                    elif self.missing_strategy == 'median':
                        df[col].fillna(df[col].median(), inplace=True)
                    elif self.missing_strategy == 'interpolation':
                        df[col].interpolate(method='linear', inplace=True)
                    else:
                        df[col].fillna(df[col].median(), inplace=True)
                else:
                    mode_val = df[col].mode()
                    fill_value = mode_val[0] if len(mode_val) > 0 else 'Unknown'
                    df[col].fillna(fill_value, inplace=True)
        
        return df
    
    def handle_outliers(self, df, target_col=None):
        df = df.copy()
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if target_col and target_col in numeric_cols:
            numeric_cols = numeric_cols.drop(target_col)
        
        for col in numeric_cols:
            if self.outlier_method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            elif self.outlier_method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < 3]
        
        return df.reset_index(drop=True)
    
    def encode_features(self, df, categorical_cols):
        df = df.copy()
        
        if self.encoding_method == 'onehot':
            df_encoded = pd.get_dummies(df, columns=categorical_cols, prefix=categorical_cols)
            self.feature_names = df_encoded.columns.tolist()
        elif self.encoding_method == 'label':
            for col in categorical_cols:
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                    df[col] = self.encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.encoders[col].transform(df[col].astype(str))
            df_encoded = df
            self.feature_names = df.columns.tolist()
        
        return df_encoded
    
    def scale_features(self, X_train, X_test=None):
        if self.scaler is None:
            if self.scaling_method == 'standard':
                self.scaler = StandardScaler()
            elif self.scaling_method == 'minmax':
                self.scaler = MinMaxScaler()
        
        if isinstance(X_train, pd.DataFrame):
            feature_names = X_train.columns.tolist()
            X_train_scaled = pd.DataFrame(
                self.scaler.fit_transform(X_train),
                columns=feature_names,
                index=X_train.index
            )
        else:
            X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            if isinstance(X_test, pd.DataFrame):
                feature_names = X_test.columns.tolist()
                X_test_scaled = pd.DataFrame(
                    self.scaler.transform(X_test),
                    columns=feature_names,
                    index=X_test.index
                )
            else:
                X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def preprocess(self, df, target_col, test_size=0.2, random_state=42):
        df = self.handle_missing_values(df)
        df = self.handle_outliers(df, target_col)
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if target_col in categorical_cols:
            categorical_cols.remove(target_col)
        
        if categorical_cols:
            df = self.encode_features(df, categorical_cols)
        
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X_train.columns.tolist()
    
    def save(self, filepath):
        joblib.dump({
            'scaler': self.scaler,
            'encoders': self.encoders,
            'feature_names': self.feature_names,
            'missing_strategy': self.missing_strategy,
            'outlier_method': self.outlier_method,
            'encoding_method': self.encoding_method,
            'scaling_method': self.scaling_method
        }, filepath)
    
    @classmethod
    def load(cls, filepath):
        data = joblib.load(filepath)
        preprocessor = cls(
            missing_strategy=data['missing_strategy'],
            outlier_method=data['outlier_method'],
            encoding_method=data['encoding_method'],
            scaling_method=data['scaling_method']
        )
        preprocessor.scaler = data['scaler']
        preprocessor.encoders = data['encoders']
        preprocessor.feature_names = data['feature_names']
        return preprocessor

