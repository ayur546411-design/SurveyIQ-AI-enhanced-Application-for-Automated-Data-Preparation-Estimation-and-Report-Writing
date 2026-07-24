import pandas as pd
import numpy as np

class WeightEngine:
    def __init__(self, df: pd.DataFrame, weight_column: str = None):
        """
        Initialize the WeightEngine with a pandas DataFrame and an optional weight column.
        """
        self.df = df.copy()
        if weight_column and weight_column not in self.df.columns:
            raise ValueError(f"Weight column '{weight_column}' not found in DataFrame.")
        self.weight_column = weight_column

    def set_weight_column(self, weight_column: str):
        """
        Set or update the column to use for weights.
        """
        if weight_column not in self.df.columns:
            raise ValueError(f"Weight column '{weight_column}' not found in DataFrame.")
        self.weight_column = weight_column

    def apply_design_weights(self, base_weight_col: str, non_response_col: str = None, new_weight_name: str = 'final_weight'):
        """
        Calculate a final design weight.
        If non_response_col is provided, final weight = base_weight * non_response_adjustment
        """
        if base_weight_col not in self.df.columns:
            raise ValueError(f"Base weight column '{base_weight_col}' not found.")
            
        if non_response_col:
            if non_response_col not in self.df.columns:
                raise ValueError(f"Non-response adjustment column '{non_response_col}' not found.")
            self.df[new_weight_name] = self.df[base_weight_col] * self.df[non_response_col]
        else:
            self.df[new_weight_name] = self.df[base_weight_col]
            
        self.weight_column = new_weight_name
        return self.df

    def get_weighted_mean(self, column_name: str):
        """
        Calculate the weighted mean of a numeric column.
        """
        if not self.weight_column:
            return self.df[column_name].mean()
            
        data = self.df[[column_name, self.weight_column]].dropna()
        weights = data[self.weight_column]
        values = data[column_name]
        
        if weights.sum() == 0:
            return np.nan
            
        return np.average(values, weights=weights)

    def get_weighted_variance(self, column_name: str):
        """
        Calculate the weighted variance of a numeric column.
        """
        if not self.weight_column:
            return self.df[column_name].var()
            
        data = self.df[[column_name, self.weight_column]].dropna()
        weights = data[self.weight_column]
        values = data[column_name]
        
        if weights.sum() == 0:
            return np.nan
            
        weighted_mean = np.average(values, weights=weights)
        variance = np.average((values - weighted_mean)**2, weights=weights)
        
        # Apply Bessel's correction equivalent for weighted variance
        sum_weights = weights.sum()
        sum_weights_sq = (weights**2).sum()
        
        if sum_weights**2 == sum_weights_sq:
            return variance
            
        correction = sum_weights**2 / (sum_weights**2 - sum_weights_sq)
        return variance * correction

    def get_weighted_frequencies(self, column_name: str):
        """
        Calculate weighted frequencies for a categorical column.
        """
        if not self.weight_column:
            return self.df[column_name].value_counts().to_dict()
            
        data = self.df[[column_name, self.weight_column]].dropna()
        
        # Group by the categorical column and sum the weights
        weighted_counts = data.groupby(column_name)[self.weight_column].sum()
        return weighted_counts.to_dict()

    def generate_summary(self, numeric_cols: list = None, categorical_cols: list = None):
        """
        Generate a summary comparing unweighted and weighted statistics.
        """
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            if self.weight_column in numeric_cols:
                numeric_cols.remove(self.weight_column)
                
        if categorical_cols is None:
            categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()

        summary = {
            "numeric": {},
            "categorical": {}
        }

        for col in numeric_cols:
            summary["numeric"][col] = {
                "unweighted_mean": self.df[col].mean(),
                "weighted_mean": self.get_weighted_mean(col),
                "unweighted_variance": self.df[col].var(),
                "weighted_variance": self.get_weighted_variance(col)
            }

        for col in categorical_cols:
            summary["categorical"][col] = {
                "unweighted_frequencies": self.df[col].value_counts().to_dict(),
                "weighted_frequencies": self.get_weighted_frequencies(col)
            }

        return summary
