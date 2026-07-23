import os
import base64
from io import BytesIO
import datetime
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import pandas as pd

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False

class ReportBuilder:
    def __init__(self, template_dir=None):
        """
        Initialize the ReportBuilder.
        If template_dir is not provided, defaults to the 'templates' directory in the same folder.
        """
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def _generate_chart_base64(self, df: pd.DataFrame, col_name: str) -> str:
        """
        Generate a histogram for a numeric column and return it as a base64 string.
        """
        plt.figure(figsize=(6, 4))
        df[col_name].plot(kind='hist', bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Distribution of {col_name}')
        plt.xlabel(col_name)
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.read()).decode('utf-8')
        return img_str

    def generate_html_report(self, title: str, df: pd.DataFrame, statistics: dict, categorical_summary: dict = None, summary_text: str = ""):
        """
        Generate an HTML report using the provided data.
        """
        template = self.env.get_template('report_template.html')
        
        # Generate charts for numeric columns
        charts = {}
        for col in statistics.keys():
            if col in df.columns:
                charts[col] = self._generate_chart_base64(df, col)
                
        html_out = template.render(
            title=title,
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary_text=summary_text,
            total_records=len(df),
            total_variables=len(df.columns),
            statistics=statistics,
            categorical_summary=categorical_summary or {},
            charts=charts
        )
        return html_out

    def generate_pdf_report(self, html_content: str, output_path: str):
        """
        Convert HTML content to a PDF file.
        """
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError("WeasyPrint is not available. Please ensure GTK and WeasyPrint are correctly installed.")
            
        HTML(string=html_content).write_pdf(output_path)
        return output_path

    def save_html_report(self, html_content: str, output_path: str):
        """
        Save HTML content to a file.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path
