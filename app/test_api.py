import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print("Root endpoint:", response.json())
    
    # Setup profile
    profile_data = {
        "name": "John Doe",
        "skills": ["React", "Node.js", "Python", "AI/ML"],
        "experience": "5 years of full-stack development with focus on web applications and AI integrations.",
        "past_projects": [
            "E-commerce platform with React and Node.js",
            "AI chatbot using Python and OpenAI", 
            "Chrome extension for productivity"
        ],
        "rates": "$50-80/hour",
        "bio": "Passionate full-stack developer with AI expertise"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/profile/setup",
        json=profile_data
    )
    print("Profile setup:", response.json())
    
    # Generate proposal
    job_data = {
        "job_posting": "Looking for a React developer to build a Chrome extension that uses AI to help with content writing. Requirements: JavaScript, Chrome APIs, OpenAI integration. Budget: $1000-2000. Timeline: 2-3 weeks.",
        "tone": "professional"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/proposal/generate",
        json=job_data
    )
    print("Proposal generation:", response.json())
    
    # Check history
    response = requests.get(f"{BASE_URL}/api/proposal/history")
    print("History:", response.json())

if __name__ == "__main__":
    test_api()