import os
from groq import Groq
import json
import re

class LeadProcessor:
    """AI Agent for scoring, enriching, and personalizing leads"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
    
    def process_lead(self, lead: dict) -> dict:
        """
        Process a single lead:
        1. Score and prioritize
        2. Enrich missing details
        3. Generate buyer persona
        4. Draft personalized email
        """
        
        # Extract lead info
        name = lead.get('name', 'Unknown')
        email = lead.get('email', '')
        company = lead.get('company', 'Unknown Company')
        role = lead.get('role', 'Unknown Role')
        industry = lead.get('industry', '')
        
        # Step 1: Score and Enrich Lead
        enrichment_prompt = f"""
You are an AI sales assistant. Analyze this lead and provide:
1. Priority Score (1-10, where 10 is highest priority)
2. Buyer Persona (job level, decision authority, pain points)
3. Suggested talking points for outreach

Lead Information:
- Name: {name}
- Role: {role}
- Company: {company}
- Industry: {industry}

Respond in JSON format:
{{
  "priority_score": <number 1-10>,
  "persona": "<brief persona description>",
  "job_level": "<Junior/Mid/Senior/Executive>",
  "decision_authority": "<Low/Medium/High>",
  "pain_points": ["<pain point 1>", "<pain point 2>"],
  "talking_points": ["<point 1>", "<point 2>"]
}}
"""
        
        enrichment = self._call_llm(enrichment_prompt)
        
        # Step 2: Generate Personalized Email
        email_prompt = f"""
Write a short, personalized sales outreach email (max 150 words) for:

Lead: {name}
Role: {role}
Company: {company}
Persona: {enrichment.get('persona', 'Professional')}
Pain Points: {', '.join(enrichment.get('pain_points', []))}

The email should:
- Be friendly and professional
- Reference their role/company naturally
- Mention 1-2 pain points
- Include a clear call-to-action
- Sign off as "Sales Team"

Write only the email body, no subject line.
"""
        
        email_body = self._call_llm(email_prompt, json_mode=False)
        
        # Combine original lead with enriched data
        enriched_lead = {
            **lead,
            'priority_score': enrichment.get('priority_score', 5),
            'persona': enrichment.get('persona', 'Unknown'),
            'job_level': enrichment.get('job_level', 'Unknown'),
            'decision_authority': enrichment.get('decision_authority', 'Medium'),
            'pain_points': ', '.join(enrichment.get('pain_points', [])),
            'talking_points': ', '.join(enrichment.get('talking_points', [])),
            'personalized_email': email_body.strip(),
            'status': 'Processed'
        }
        
        return enriched_lead
    
    def _call_llm(self, prompt: str, json_mode: bool = True) -> dict:
        """Call Groq LLM API"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI sales assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            if json_mode:
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Fallback defaults
                    return {
                        "priority_score": 5,
                        "persona": "Business Professional",
                        "job_level": "Mid",
                        "decision_authority": "Medium",
                        "pain_points": ["Efficiency", "Growth"],
                        "talking_points": ["Solution benefits", "ROI"]
                    }
            else:
                return content
        
        except Exception as e:
            print(f"Error calling LLM: {e}")
            if json_mode:
                return {
                    "priority_score": 5,
                    "persona": "Business Professional",
                    "job_level": "Mid",
                    "decision_authority": "Medium",
                    "pain_points": ["Efficiency"],
                    "talking_points": ["Product value"]
                }
            else:
                return f"Hi {prompt.split('Lead:')[1].split()[0]},\n\nI hope this email finds you well. I wanted to reach out to discuss how we can help your team achieve better results.\n\nWould you be available for a quick call?\n\nBest regards,\nSales Team"