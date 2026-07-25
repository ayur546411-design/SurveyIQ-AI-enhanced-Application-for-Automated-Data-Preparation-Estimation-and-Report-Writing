import requests
import pandas as pd
import numpy as np
import os
import json

def run_test():
    # Create dummy csv
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 70, size=100),
        'income': np.random.normal(50000, 15000, size=100),
        'satisfaction_score': np.random.randint(1, 6, size=100)
    })
    
    csv_path = 'dummy_survey.csv'
    df.to_csv(csv_path, index=False)
    
    url = "http://127.0.0.1:8000/api/process"
    
    with open(csv_path, 'rb') as f:
        files = {'file': (csv_path, f, 'text/csv')}
        print(f"Sending POST request to {url}...")
        response = requests.post(url, files=files)
        
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response message:", data.get("message"))
        print("Reports generated:")
        print(json.dumps(data.get("reports"), indent=2))
    else:
        print("Response:", response.text)

if __name__ == '__main__':
    run_test()
