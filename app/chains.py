from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_groq import ChatGroq
from typing import List, Dict, Any
import os
import json
from dotenv import load_dotenv

load_dotenv()

class ProposalGenerator:
    def __init__(self):
        # Use Groq API 
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        self._setup_chains()
    
    def _setup_chains(self):
        """Setup LangChain chains for different tasks"""
        # Job Analysis Chain
        self.job_analysis_prompt = ChatPromptTemplate.from_template("""
        Analyze the following job posting and extract key information in JSON format.
        
        Job Posting:
        {job_posting}
        
        Extract:
        1. Required skills and technologies
        2. Project scope and main requirements
        3. Budget and timeline information (if mentioned)
        4. Key priorities and goals
        
        Return ONLY valid JSON with this structure:
        {{
            "required_skills": ["skill1", "skill2"],
            "project_scope": "description",
            "budget": "budget info",
            "timeline": "timeline info",
            "key_priorities": ["priority1", "priority2"]
        }}
        """)
        
        self.job_analysis_chain = self.job_analysis_prompt | self.llm | StrOutputParser()
        
        # Proposal Generation Chain
        self.proposal_prompt = ChatPromptTemplate.from_template("""
        You are a professional freelancer writing a job proposal. Generate a compelling proposal based on the job requirements and your relevant experience.
        
        Job Requirements:
        {job_analysis}
        
        Your Relevant Experience:
        {relevant_experience}
        
        Tone: {tone}
        
        Generate a professional proposal that includes:
        1. Professional greeting
        2. Show understanding of the project requirements
        3. Highlight relevant experience and skills that match the job
        4. Proposed approach/solution
        5. Timeline and next steps
        6. Professional closing
        
        Keep it concise but compelling (300-500 words). Focus on how your specific experience makes you the right fit.
        
        Proposal:
        """)
    
    def analyze_job_posting(self, job_posting: str) -> Dict[str, Any]:
        """Extract key information from job posting"""
        try:
            analysis_text = self.job_analysis_chain.invoke({"job_posting": job_posting})
            # Cresponse and parse JSON
            analysis_text = analysis_text.strip()
            if analysis_text.startswith("```json"):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith("```"):
                analysis_text = analysis_text[:-3]
            
            return json.loads(analysis_text)
        except Exception as e:
            # Fallback analysis
            return {
                "required_skills": [],
                "project_scope": job_posting[:200] + "...",
                "budget": "Not specified",
                "timeline": "Not specified",
                "key_priorities": ["Complete project requirements"]
            }
    
    def generate_proposal(self, job_analysis: Dict[str, Any], relevant_experience: List[Dict[str, Any]], tone: str = "professional") -> str:
        """Generate proposal using LLM"""
        
        # Format relevant experience
        exp_text = "\n\n".join([
            f"Experience {i+1} (Relevance: {exp['relevance_score']:.2f}):\n{exp['content']}"
            for i, exp in enumerate(relevant_experience)
        ])
        
        # Create the proposal chain
        proposal_chain = (
            {
                "job_analysis": RunnablePassthrough(),
                "relevant_experience": RunnablePassthrough(),
                "tone": RunnablePassthrough()
            }
            | self.proposal_prompt
            | self.llm
            | StrOutputParser()
        )
        
        proposal = proposal_chain.invoke({
            "job_analysis": json.dumps(job_analysis, indent=2),
            "relevant_experience": exp_text,
            "tone": tone
        })
        
        return proposal
    
    def calculate_confidence_score(self, job_analysis: Dict[str, Any], relevant_experience: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on skill matching and relevance"""
        if not relevant_experience:
            return 0.0
        
        # Average relevance score from vector search
        avg_relevance = sum(exp['relevance_score'] for exp in relevant_experience) / len(relevant_experience)
        
        # Simple skill matching boost
        required_skills = job_analysis.get('required_skills', [])
        if required_skills:
            # If we have skills mentioned, assume some match
            skill_boost = min(0.3, len(required_skills) * 0.1)
        else:
            skill_boost = 0.1
        
        confidence = min(1.0, avg_relevance + skill_boost)
        return confidence