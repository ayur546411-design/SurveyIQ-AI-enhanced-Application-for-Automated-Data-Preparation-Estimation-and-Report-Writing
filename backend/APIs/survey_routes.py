from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Form, Body
from fastapi.responses import JSONResponse
import pandas as pd
import os
import io
import uuid
import json

# Import our custom modules
from Cleaning.data_cleaner import DataCleaner
from Statistics.statistics_engine import StatisticsEngine
from report_generator.report_builder import ReportBuilder
from weight_engine.weight_engine import WeightEngine
from AI.gemini_service import gemini_service

router = APIRouter()

@router.post("/process")
async def process_survey_data(request: Request, file: UploadFile = File(...), weight_column: str = Form(None)):
    """
    Endpoint to upload survey datasets (CSV/Excel) and process them completely.
    This will clean the data, calculate statistics, optionally apply weights, and generate reports.
    """
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
    
    # 1. Read file into Pandas DataFrame
    contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    # 2. Clean the Data
    try:
        cleaner = DataCleaner(df)
        cleaner.impute_missing_values()
        cleaner.detect_outliers(method='iqr')
        clean_df = cleaner.df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cleaning data: {str(e)}")

    # 3. Calculate Statistics (and apply Weights if provided)
    try:
        stats_engine = StatisticsEngine(clean_df)
        statistics = stats_engine.generate_all_statistics()
        categorical_summary = stats_engine.get_categorical_summary()
        
        weight_summary = None
        if weight_column:
            if weight_column in clean_df.columns:
                we = WeightEngine(clean_df, weight_column=weight_column)
                weight_summary = we.generate_summary()
            else:
                # Silently ignore or we could raise an error. We'll just skip weighting if col not found.
                pass
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

    # 4. Generate Reports
    try:
        report_id = str(uuid.uuid4())
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        
        report_builder = ReportBuilder()
        html_content = report_builder.generate_html_report(
            title=f"Survey Report: {file.filename}",
            df=clean_df,
            statistics=statistics,
            categorical_summary=categorical_summary,
            summary_text="Automated processing completed successfully."
        )
        
        html_filename = f"report_{report_id}.html"
        pdf_filename = f"report_{report_id}.pdf"
        
        html_path = os.path.join(reports_dir, html_filename)
        pdf_path = os.path.join(reports_dir, pdf_filename)
        
        report_builder.save_html_report(html_content, html_path)
        
        pdf_generated = False
        try:
            report_builder.generate_pdf_report(html_content, pdf_path)
            pdf_generated = True
        except Exception as e:
            # pdf generation failed (weasyprint/GTK issue), log it but don't fail the request
            print(f"Failed to generate PDF: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating reports: {str(e)}")

    # Construct the base URL for downloading the reports
    base_url = str(request.base_url).rstrip('/')
    
    response_data = {
        "filename": file.filename,
        "message": "Data processed successfully.",
        "shape": {"rows": clean_df.shape[0], "columns": clean_df.shape[1]},
        "statistics": statistics,
        "categorical_summary": categorical_summary,
        "weight_summary": weight_summary,
        "reports": {
            "html_url": f"{base_url}/reports/{html_filename}",
            "pdf_url": f"{base_url}/reports/{pdf_filename}" if pdf_generated else None
        }
    }
    
    return JSONResponse(content=response_data)

@router.post("/insights")
async def get_insights(data_summary: dict = Body(...)):
    """
    Endpoint to fetch AI-generated insights for a given dataset summary.
    Expects a JSON body with statistics or categorical_summary.
    """
    try:
        prompt = (
            "Analyze the following survey data summary and provide 3-5 key insights, "
            "trends, or areas of concern. Keep it concise.\n\n"
            f"Data Summary: {json.dumps(data_summary)[:2000]}" # Limiting size to avoid huge prompts
        )
        insight_text = gemini_service.generate_insight(prompt)
        return {"insights": insight_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")
