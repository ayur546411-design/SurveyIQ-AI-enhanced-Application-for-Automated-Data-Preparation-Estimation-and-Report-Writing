import pandas as pd
import numpy as np
import scipy.stats as stats

class StatisticsEngine:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the StatisticsEngine with a pandas DataFrame.
        """
        self.df = df.copy()

    def get_numeric_columns(self):
        return self.df.select_dtypes(include=[np.number]).columns.tolist()

    def calculate_basic_stats(self, column_name: str, confidence_level: float = 0.95):
        """
        Calculate statistics for a specific column.
        Returns a dictionary with:
        - Mean
        - Median
        - Variance
        - Standard Error
        - Confidence Interval
        - Margin of Error
        """
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame.")
        
        data = self.df[column_name].dropna()
        n = len(data)
        
        if n < 2:
            return {
                "count": n,
                "mean": None,
                "median": None,
                "variance": None,
                "std_error": None,
                "confidence_interval": None,
                "margin_of_error": None
            }

        mean = float(np.mean(data))
        median = float(np.median(data))
        variance = float(np.var(data, ddof=1))
        
        std_error = float(stats.sem(data))
        
        # Calculate Confidence Interval and Margin of Error
        h = std_error * stats.t.ppf((1 + confidence_level) / 2., n-1)
        margin_of_error = float(h)
        ci_lower = mean - h
        ci_upper = mean + h
        confidence_interval = (float(ci_lower), float(ci_upper))

        return {
            "count": n,
            "mean": mean,
            "median": median,
            "variance": variance,
            "std_error": std_error,
            "confidence_interval": confidence_interval,
            "margin_of_error": margin_of_error
        }

    def generate_all_statistics(self, confidence_level: float = 0.95):
        """
        Generate statistics for all numeric columns.
        Returns a dictionary mapping column names to their statistics.
        """
        numeric_cols = self.get_numeric_columns()
        results = {}
        for col in numeric_cols:
            results[col] = self.calculate_basic_stats(col, confidence_level)
        return results

    def get_categorical_summary(self):
        """
        Get value counts for categorical columns.
        """
        cat_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        results = {}
        for col in cat_cols:
            results[col] = self.df[col].value_counts().to_dict()
        return results
