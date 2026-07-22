import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataCleaner with a pandas DataFrame.
        """
        self.df = df.copy()

    def impute_missing_values(self):
        """
        Impute missing values:
        - Numerical columns: Median
        - Categorical columns: Mode
        """
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                else:
                    self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
        return self.df

    def remove_duplicates(self):
        """
        Remove exact duplicate rows from the dataset.
        """
        self.df.drop_duplicates(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def detect_outliers(self, method='iqr', threshold=1.5):
        """
        Detect and handle outliers in numerical columns.
        Supported methods: 'iqr' (Interquartile Range) or 'zscore'.
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                # Cap the outliers
                self.df[col] = np.where(self.df[col] < lower_bound, lower_bound, self.df[col])
                self.df[col] = np.where(self.df[col] > upper_bound, upper_bound, self.df[col])
            
            elif method == 'zscore':
                # Simplified z-score implementation capping
                col_mean = self.df[col].mean()
                col_std = self.df[col].std()
                if col_std > 0:
                    z_scores = (self.df[col] - col_mean) / col_std
                    
                    # Cap based on z-score threshold (commonly 3)
                    self.df[col] = np.where(z_scores > 3, col_mean + 3 * col_std, self.df[col])
                    self.df[col] = np.where(z_scores < -3, col_mean - 3 * col_std, self.df[col])
        
        return self.df

    def validate_data_types(self, type_mapping=None):
        """
        Validate and cast data types based on a provided mapping.
        type_mapping: dict mapping column names to target types (e.g. {'age': 'int'})
        """
        if not type_mapping:
            return self.df
            
        for col, target_type in type_mapping.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(target_type)
                except ValueError as e:
                    print(f"Warning: Could not cast column {col} to {target_type}. Error: {e}")
        return self.df

    def consistency_checks(self, rules=None):
        """
        Apply rule-based consistency checks.
        rules: A list of callables that take a DataFrame and return a DataFrame.
        """
        if not rules:
            return self.df
            
        for rule in rules:
            self.df = rule(self.df)
        return self.df

    def clean_all(self):
        """
        Run a standard automated cleaning pipeline.
        """
        self.remove_duplicates()
        self.impute_missing_values()
        self.detect_outliers(method='iqr')
        return self.df
