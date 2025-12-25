# AI-Enhanced Sales Campaign CRM (MVP)

A production-ready AI-powered CRM system that automates lead scoring, enrichment, and personalized outreach using Groq LLM API.

## Features

- **AI Lead Processing**: Automatic scoring, enrichment, and persona generation using Groq's LLaMA 3.1
- **Automated Email Outreach**: Personalized emails sent via SMTP (MailHog for testing)
- **Smart Campaign Reports**: AI-generated markdown reports with insights and statistics
- **Docker-Ready**: Complete containerized setup with `docker-compose`
- **FastAPI Backend**: Modern, async Python API with clean architecture

---

## Architecture

```
┌─────────────┐
│   FastAPI   │  ← Main Application
└──────┬──────┘
       │
       ├─→ LeadProcessor (AI Agent)
       │   └─→ Groq LLM API
       │
       ├─→ EmailSender (SMTP Agent)
       │   └─→ MailHog
       │
       └─→ ReportGenerator
           └─→ Groq LLM API
```

---

## Prerequisites

- **Docker & Docker Compose** (required)
- **Groq API Key** (free at [console.groq.com](https://console.groq.com/keys))
- **Git** (for cloning)

---

## Quick Start

### 1. Clone & Setup

```bash
# Clone the repository
git clone ai-sales-crm
cd ai-sales-crm
```

### 2. Add Your Groq API Key(Already exist in .env.example File)

Get a free API key from [Groq Console](https://console.groq.com/keys) and add it to `.env`:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 3. Start the System

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

### 4. Run the Campaign(Must open another bash/terminal then paste it)

```bash
# Trigger the campaign processing
curl -X POST http://localhost:8000/process-campaign
```

### 5. View Results

- **MailHog UI**: http://localhost:8025 (see all sent emails)
- **API Docs**: http://localhost:8000/docs (FastAPI Swagger UI)
- **Enriched CSV**: Check `data/leads_enriched.csv`
- **Campaign Report**: Check `reports/campaign_report_*.md`

---

## Project Structure

```
ai-sales-crm/
├── main.py                    # FastAPI application
├── agents/
│   ├── __init__.py
│   ├── lead_processor.py      # AI lead enrichment agent
│   └── email_sender.py        # Email outreach agent
├── utils/
│   ├── __init__.py
│   └── report_generator.py    # AI report generator
├── data/
│   ├── leads.csv              # Input leads (25 samples)
│   └── leads_enriched.csv     # Output (generated)
├── reports/                   # Generated reports (auto-created)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Application container
├── docker-compose.yml         # Full stack setup
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## AI Capabilities

### Lead Processing Agent
- **Priority Scoring**: 1-10 scale based on role, industry, and potential
- **Persona Generation**: Job level, decision authority, pain points
- **Enrichment**: Missing details filled using LLM reasoning
- **Talking Points**: AI-suggested topics for outreach

### Email Generation Agent
- **Personalization**: Customized per lead's role and company
- **Context-Aware**: References specific pain points
- **Professional Tone**: Balanced, friendly, and action-oriented
- **Short & Effective**: ~150 words per email

### Report Generation Agent
- **Statistical Analysis**: Lead distribution, success rates
- **AI Insights**: Actionable recommendations
- **Segmentation**: By priority, job level, authority
- **Next Steps**: Smart suggestions for follow-up

---

## Sample Output

### Enriched Lead Data
```csv
name,email,company,role,industry,priority_score,persona,job_level,personalized_email,email_sent
John Smith,john.smith@techcorp.com,TechCorp Solutions,VP of Engineering,Technology,9,Senior Technical Leader,Senior,"Hi John, ...",true
```

### Campaign Report
```markdown
# Sales Campaign Report

**Generated:** 2024-01-15 10:30:00

## Campaign Overview

| Metric | Value |
|--------|-------|
| Total Leads Processed | 25 |
| Emails Successfully Sent | 25 |
| Success Rate | 100.0% |
| Average Priority Score | 7.2/10 |

[... full report with insights ...]
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | - | Your Groq API key (required) |
| `SMTP_HOST` | mailhog | SMTP server hostname |
| `SMTP_PORT` | 1025 | SMTP server port |
| `FROM_EMAIL` | sales@crm.local | Sender email address |
| `FROM_NAME` | Sales Team | Sender display name |

### Customization

**Change LLM Model:**
Edit `agents/lead_processor.py`:
```python
self.model = "llama-3.1-70b-versatile"
```

**Adjust Email Length:**
Edit the prompt in `lead_processor.py`:
```python
email_prompt = f"Write a short email (max 100 words)..."
```

**Modify Lead Criteria:**
Edit scoring logic in `lead_processor.py`

---

## Performance

- **Processing Speed**: ~3-5 seconds per lead
- **25 Leads**: ~2 minutes total
- **Concurrent Processing**: Can be parallelized (not implemented for simplicity)

---

## Resources

- [Groq API Docs](https://console.groq.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MailHog GitHub](https://github.com/mailhog/MailHog)
- [Docker Compose Guide](https://docs.docker.com/compose/)

---

## What This Demonstrates

**Clean Architecture**: Separation of concerns (agents, utils, main)  
**AI Integration**: Practical LLM usage for business automation  
**Production Patterns**: Docker, env vars, error handling  
**End-to-End Solution**: From CSV input to email output to reports  
**Scalable Design**: Easy to extend with new features  
**Demo-Ready**: Works out of the box with sample data  

---

## Author

**Md Hasan Imon** 
* **Developer:** Md Emon Hasan
* **GitHub:** [Md-Emon-Hasan](https://github.com/Md-Emon-Hasan)
* **LinkedIn:** [Md Emon Hasan](https://www.linkedin.com/in/md-emon-hasan-695483237/)
* **Email:** [emon.mlengineer@gmail.com](mailto:emon.mlengineer@gmail.com)
* **WhatsApp:** [+8801834363533](https://wa.me/8801834363533)

---

## License

This project is for assessment purposes. Not for production use without proper security review.

---
