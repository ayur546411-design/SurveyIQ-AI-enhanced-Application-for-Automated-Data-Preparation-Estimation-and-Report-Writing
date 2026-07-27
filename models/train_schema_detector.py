import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def extract_features(series: pd.Series) -> dict:
    """Extract statistical features from a pandas Series to predict its data type."""
    total_count = len(series)
    if total_count == 0:
        return {'unique_ratio': 0, 'missing_ratio': 1, 'is_numeric_castable': 0, 'mean_str_len': 0}
        
    num_unique = series.nunique(dropna=True)
    num_missing = series.isnull().sum()
    
    # Try casting to numeric
    numeric_series = pd.to_numeric(series, errors='coerce')
    numeric_valid_count = numeric_series.notnull().sum()
    is_numeric_castable = numeric_valid_count / total_count if total_count > 0 else 0
    
    # Text length stats
    if series.dtype == 'object':
        str_series = series.dropna().astype(str)
        mean_len = str_series.str.len().mean() if not str_series.empty else 0
    else:
        mean_len = 0
        
    return {
        'unique_ratio': num_unique / total_count,
        'missing_ratio': num_missing / total_count,
        'is_numeric_castable': is_numeric_castable,
        'mean_str_len': mean_len
    }

def generate_synthetic_data(num_samples=1000):
    """Generate synthetic columns and their features for training."""
    data = []
    labels = []
    
    for _ in range(num_samples):
        col_type = np.random.choice(['categorical', 'numerical', 'text'])
        n_rows = np.random.randint(50, 1000)
        
        if col_type == 'categorical':
            # Low unique ratio
            n_categories = np.random.randint(2, 15)
            series = pd.Series(np.random.choice([f'Cat_{i}' for i in range(n_categories)], size=n_rows))
        elif col_type == 'numerical':
            # High unique ratio, fully castable
            series = pd.Series(np.random.normal(0, 1, size=n_rows))
        else: # text
            # High unique ratio, not castable to numeric, long string length
            series = pd.Series([' '.join(np.random.choice(['foo', 'bar', 'baz', 'qux'], size=np.random.randint(5, 20))) for _ in range(n_rows)])
            
        # Add random missing values
        missing_mask = np.random.rand(n_rows) < np.random.uniform(0.01, 0.2)
        series[missing_mask] = np.nan
        
        features = extract_features(series)
        data.append(features)
        labels.append(col_type)
        
    return pd.DataFrame(data), np.array(labels)

def train_and_save_model():
    print("Generating synthetic data for schema detector...")
    X, y = generate_synthetic_data(num_samples=2000)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    print("Evaluating Model:")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), 'schema_detector.pkl')
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_and_save_model()
