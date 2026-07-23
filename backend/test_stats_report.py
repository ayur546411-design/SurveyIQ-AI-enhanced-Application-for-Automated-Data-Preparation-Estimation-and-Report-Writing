import sys
import os
import pandas as pd
import numpy as np

# Add the backend folder to sys.path to easily import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Statistics.statistics_engine import StatisticsEngine
from report_generator.report_builder import ReportBuilder
from Cleaning.data_cleaner import DataCleaner

def run_test():
    # 1. Create a dummy dataset
    np.random.seed(42)
    df = pd.DataFrame({
        'age': np.random.randint(18, 70, size=100),
        'income': np.random.normal(50000, 15000, size=100),
        'satisfaction_score': np.random.randint(1, 6, size=100),
        'department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing'], size=100)
    })
    
    # Add some missing values and outliers to test DataCleaner if needed
    df.loc[0, 'income'] = np.nan
    df.loc[1, 'income'] = 200000 # outlier

    print("Original Data Shape:", df.shape)

    # 2. Clean the data
    cleaner = DataCleaner(df)
    cleaner.impute_missing_values()
    cleaner.detect_outliers(method='iqr')
    clean_df = cleaner.df
    print("Clean Data Shape:", clean_df.shape)

    # 3. Generate Statistics
    stats_engine = StatisticsEngine(clean_df)
    statistics = stats_engine.generate_all_statistics()
    categorical_summary = stats_engine.get_categorical_summary()
    
    print("Generated Statistics for:", list(statistics.keys()))
    
    # 4. Generate Report
    report_builder = ReportBuilder()
    html_content = report_builder.generate_html_report(
        title="Test Survey Report",
        df=clean_df,
        statistics=statistics,
        categorical_summary=categorical_summary,
        summary_text="This is an automated test report showing descriptive statistics and visualizations."
    )
    
    html_path = os.path.join(os.path.dirname(__file__), 'test_report.html')
    pdf_path = os.path.join(os.path.dirname(__file__), 'test_report.pdf')
    
    report_builder.save_html_report(html_content, html_path)
    print(f"HTML report saved to {html_path}")
    
    try:
        report_builder.generate_pdf_report(html_content, pdf_path)
        print(f"PDF report saved to {pdf_path}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == '__main__':
    run_test()
