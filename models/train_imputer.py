import os
import joblib
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def create_and_save_imputer():
    print("Configuring Advanced KNN Imputation pipeline...")
    
    # We create a pipeline that first scales the data, then imputes using KNN, 
    # since KNN is distance-based and requires scaled data.
    imputer_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn_imputer', KNNImputer(n_neighbors=5, weights='distance'))
    ])
    
    # Since this is an unsupervised step and depends on the dataset, we won't 'fit' it here.
    # Instead, we just save the configured pipeline so the backend can load it and fit_transform on new datasets.
    
    model_path = os.path.join(os.path.dirname(__file__), 'advanced_imputer.pkl')
    joblib.dump(imputer_pipeline, model_path)
    
    print(f"Advanced Imputer pipeline saved to {model_path}")

if __name__ == '__main__':
    create_and_save_imputer()
