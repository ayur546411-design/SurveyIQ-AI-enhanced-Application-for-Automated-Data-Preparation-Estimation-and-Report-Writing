# StatiGen AI - Machine Learning Models

This directory contains scripts and trained artifacts for the AI engines powering SurveyIQ (StatiGen AI).

## Available Models

1. **Schema Detector (`schema_detector.pkl`)**
   - **Purpose**: Automatically classify dataset columns into 'categorical', 'numerical', or 'text'. This helps the AI Schema Detection Engine determine how to process, clean, and analyze each feature.
   - **Algorithm**: Random Forest Classifier
   - **Training Script**: `train_schema_detector.py`
   - **Usage**: Load via `joblib.load('schema_detector.pkl')`. Extract features (unique ratio, missing ratio, castability, mean string length) and pass them to `.predict(X)`.

2. **Advanced Imputer (`advanced_imputer.pkl`)**
   - **Purpose**: Perform robust imputation for missing values instead of simple mean/median imputation.
   - **Algorithm**: KNNImputer (Pipeline with StandardScaler)
   - **Training Script**: `train_imputer.py`
   - **Usage**: Load via `joblib.load('advanced_imputer.pkl')`. Use `.fit_transform(X)` on numerical columns during the cleaning pipeline.

## Generating Models

If you make updates to the feature engineering logic or algorithms, simply rerun the scripts:
```bash
python train_schema_detector.py
python train_imputer.py
```
