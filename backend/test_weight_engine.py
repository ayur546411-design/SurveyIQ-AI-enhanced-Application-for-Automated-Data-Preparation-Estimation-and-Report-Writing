import sys
import os
import pandas as pd
import numpy as np
import json

# Add the backend folder to sys.path to easily import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weight_engine.weight_engine import WeightEngine

def run_test():
    # 1. Create a dummy dataset
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 70, size=10),
        'income': np.random.normal(50000, 15000, size=10),
        'satisfaction': np.random.choice(['Low', 'Medium', 'High'], size=10),
        'base_weight': [1.0, 1.2, 0.8, 2.5, 0.5, 1.0, 1.5, 3.0, 0.9, 1.1],
        'non_response_adj': [1.0, 1.1, 1.0, 1.2, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    })
    
    print("Dummy Data Sample:")
    print(df[['age', 'income', 'satisfaction', 'base_weight']].head())
    print("\n-----------------------\n")
    
    # 2. Initialize WeightEngine
    engine = WeightEngine(df)
    
    # Apply design weights
    df_weighted = engine.apply_design_weights(base_weight_col='base_weight', non_response_col='non_response_adj', new_weight_name='final_weight')
    
    print("Weights applied. New weight column 'final_weight' created.")
    print(df_weighted[['base_weight', 'non_response_adj', 'final_weight']].head())
    print("\n-----------------------\n")
    
    # 3. Generate Summaries
    summary = engine.generate_summary(numeric_cols=['age', 'income'], categorical_cols=['satisfaction'])
    
    print("Summary (Weighted vs Unweighted):")
    print(json.dumps(summary, indent=2))
    print("\n-----------------------\n")

if __name__ == '__main__':
    run_test()
