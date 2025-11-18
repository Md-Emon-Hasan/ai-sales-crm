# Swiftme Mini - Smart Job Proposal Generator

A simplified version of Swiftme bid writing assistant that uses LangChain and RAG to generate personalized job proposals.

## Features

- **RAG System**: Stores freelancer profiles and retrieves relevant experience using ChromaDB
- **Job Analysis**: Automatically extracts key requirements from job postings using LLM
- **Smart Proposal Generation**: Creates personalized proposals using Groq LLM
- **Confidence Scoring**: Provides match confidence for each proposal
- **REST API**: FastAPI endpoints for easy integration
- **Proposal History**: Tracks last 5 generated proposals

## Project Structure

```
swiftme-mini/
├── app/                            # Main application package
│   ├── __init__.py                 # Python package initialization
│   ├── main.py                     # FastAPI application entry point
│   ├── models.py                   # Pydantic data models
│   ├── database.py                 # Vector database
│   ├── rag_system.py               # RAG system implementation
│   ├── chains.py                   # LangChain workflows and chains
│   └── test_api.py                 # API testing script
├── chroma_db/                      # Vector database storage
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── NOTES.md                        # Technical decisions & architecture notes
```
## Tech Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: LangChain, Groq API
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Authentication**: API Key based

## Installation

### Prerequisites
- Python 3.8+
- Groq API Key ([Get it here](https://console.groq.com/))

### Step-by-Step Setup

1. **Clone and setup environment**:
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

2. **Configure environment variables**:
```bash
# Create .env file and add your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

3. **Run the application with Test file**:
Run the test script:
```bash
python app/test_api.py
```

4. **Run the Application**
```bash
uvicorn app.main:app --reload --port 8000
```

4. **Access the API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## API Endpoints

### 1. Setup Freelancer Profile
```http
POST /api/profile/setup
Content-Type: application/json

{
  "name": "John Doe",
  "skills": ["React", "Node.js", "Python", "AI/ML"],
  "experience": "5 years full-stack development...",
  "past_projects": ["E-commerce platform", "AI chatbot"],
  "rates": "$50-80/hour",
  "bio": "Experienced developer..."
}
```

### 2. Generate Proposal
```http
POST /api/proposal/generate
Content-Type: application/json

{
  "job_posting": "Looking for React developer...",
  "tone": "professional"
}
```

### 3. Get Proposal History
```http
GET /api/proposal/history
```

### 4. Health Check
```http
GET /api/health
```

## Example Usage

### Using curl:
```bash
# Setup profile
curl -X POST "http://localhost:8000/api/profile/setup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "skills": ["React", "Node.js", "Python"],
    "experience": "5 years experience...",
    "past_projects": ["E-commerce platform", "AI chatbot"],
    "rates": "$50-80/hour"
  }'

# Generate proposal
curl -X POST "http://localhost:8000/api/proposal/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "job_posting": "Need React developer for Chrome extension...",
    "tone": "professional"
  }'
```

### Using Python:
```python
import requests

BASE_URL = "http://localhost:8000"

# Setup profile
profile_data = {
    "name": "John Doe",
    "skills": ["React", "Node.js", "Python"],
    "experience": "5 years full-stack development",
    "past_projects": ["E-commerce platform", "AI chatbot"],
    "rates": "$50-80/hour"
}

response = requests.post(f"{BASE_URL}/api/profile/setup", json=profile_data)
print(response.json())

# Generate proposal
job_data = {
    "job_posting": "Looking for React developer...",
    "tone": "professional"
}

response = requests.post(f"{BASE_URL}/api/proposal/generate", json=job_data)
print(response.json())
```

## Architecture

```
Job Posting → LangChain → RAG System → LLM → Proposal
     ↓              ↓           ↓        ↓       ↓
  Analysis     Extraction   Vector DB  Groq   Response
```

### Workflow:
1. **Profile Storage**: Freelancer data stored in ChromaDB vector store
2. **Job Analysis**: LLM extracts skills, requirements, budget from job posting
3. **Semantic Search**: Find relevant experience using vector similarity
4. **Proposal Generation**: LLM creates personalized proposal with context
5. **Confidence Scoring**: Calculate match score based on relevance

## Configuration

### Environment Variables:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Model Settings:
- **LLM**: Groq Llama 3.1 8B Instant
- **Embeddings**: HuggingFace all-MiniLM-L6-v2
- **Vector DB**: ChromaDB (local persistence)
- **Temperature**: 0.7 (balanced creativity)

## Deployment

### Local Development:
```bash
uvicorn app.main:app --reload --port 8000
```

### Production:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```


## Testing

Run the test script:
```bash
python app/test_api.py
```

Or use the interactive docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## **Developed By**

**Md Emon Hasan**  
🔗 **Email:** emon.mlengineer@gmail.com  
🔗 **Portfolio:** [Md Hasan Imon](https://md-emon-hasan.github.io/My-Resume/)
🔗 **WhatsApp:** [+8801834363533](https://wa.me/8801834363533)  
🔗 **GitHub:** [Md-Emon-Hasan](https://github.com/Md-Emon-Hasan)  
🔗 **LinkedIn:** [Md Emon Hasan](https://www.linkedin.com/in/md-emon-hasan-695483237/)  
🔗 **Facebook:** [Md Emon Hasan](https://www.facebook.com/mdemon.hasan2001/)


## License

MIT License - see LICENSE file for details

---