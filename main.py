from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

from agents.lead_processor import LeadProcessor
from agents.email_sender import EmailSender
from utils.report_generator import ReportGenerator

app = FastAPI(title="AI Sales Campaign CRM")

# Ensure directories exist
Path("data").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

INPUT_CSV = "data/leads.csv"
OUTPUT_CSV = "data/leads_enriched.csv"

@app.get("/")
async def root():
    return {
        "message": "AI Sales Campaign CRM API",
        "endpoints": {
            "/process-campaign": "Start processing campaign",
            "/status": "Check campaign status",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/process-campaign")
async def process_campaign(background_tasks: BackgroundTasks):
    """
    Main endpoint to process the entire campaign:
    1. Read leads from CSV
    2. Score and enrich leads with AI
    3. Send personalized outreach emails
    4. Update CSV with results
    5. Generate campaign report
    """
    
    if not os.path.exists(INPUT_CSV):
        return JSONResponse(
            status_code=404,
            content={"error": f"Input file {INPUT_CSV} not found"}
        )
    
    # Start processing in background
    background_tasks.add_task(run_campaign_pipeline)
    
    return {
        "status": "Campaign processing started",
        "message": "Check /status endpoint for updates",
        "timestamp": datetime.now().isoformat()
    }

async def run_campaign_pipeline():
    """Execute the complete campaign pipeline"""
    
    print("Starting Campaign Pipeline...")
    
    # Step 1: Read leads
    print("Reading leads from CSV...")
    df = pd.read_csv(INPUT_CSV)
    total_leads = len(df)
    print(f"Loaded {total_leads} leads")
    
    # Step 2: Process leads with AI
    print("Processing leads with AI...")
    processor = LeadProcessor()
    enriched_leads = []
    
    for idx, row in df.iterrows():
        print(f"Processing lead {idx + 1}/{total_leads}: {row.get('name', 'Unknown')}")
        enriched_lead = processor.process_lead(row.to_dict())
        enriched_leads.append(enriched_lead)
    
    enriched_df = pd.DataFrame(enriched_leads)
    print(f"Enriched {len(enriched_leads)} leads")
    
    # Step 3: Send outreach emails
    print("Sending outreach emails...")
    email_sender = EmailSender()
    
    for idx, lead in enumerate(enriched_leads):
        print(f"Sending email {idx + 1}/{total_leads} to {lead.get('email', 'Unknown')}")
        sent = email_sender.send_outreach(lead)
        enriched_leads[idx]['email_sent'] = sent
        enriched_leads[idx]['sent_at'] = datetime.now().isoformat() if sent else None
    
    enriched_df = pd.DataFrame(enriched_leads)
    print(f"Sent {sum(1 for l in enriched_leads if l.get('email_sent'))} emails")
    
    # Step 4: Save enriched data
    print("Saving enriched data...")
    enriched_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved to {OUTPUT_CSV}")
    
    # Step 5: Generate report
    print("Generating campaign report...")
    report_gen = ReportGenerator()
    report_path = report_gen.generate_report(enriched_df)
    print(f"Report generated: {report_path}")
    
    print("Campaign Pipeline Complete!")

@app.get("/status")
async def get_status():
    """Check the status of the campaign"""
    
    status_info = {
        "input_file_exists": os.path.exists(INPUT_CSV),
        "output_file_exists": os.path.exists(OUTPUT_CSV),
        "timestamp": datetime.now().isoformat()
    }
    
    if os.path.exists(INPUT_CSV):
        df_input = pd.read_csv(INPUT_CSV)
        status_info["total_leads"] = len(df_input)
    
    if os.path.exists(OUTPUT_CSV):
        df_output = pd.read_csv(OUTPUT_CSV)
        status_info["processed_leads"] = len(df_output)
        status_info["emails_sent"] = df_output['email_sent'].sum() if 'email_sent' in df_output.columns else 0
    
    # Check for reports
    reports_dir = Path("reports")
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.md"))
        status_info["reports_generated"] = len(reports)
        if reports:
            status_info["latest_report"] = str(reports[-1])
    
    return status_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)