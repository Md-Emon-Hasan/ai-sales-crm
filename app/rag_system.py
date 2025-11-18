from .database import VectorStore
from .chains import ProposalGenerator
from .models import FreelancerProfile, JobPosting, ProposalResponse
from typing import List, Dict, Any
import uuid
from datetime import datetime

class SmartProposalSystem:
    def __init__(self):
        self.vector_store = VectorStore()
        self.proposal_generator = ProposalGenerator()
        self.proposal_history = []
    
    def setup_profile(self, profile_data: Dict[str, Any]) -> str:
        """Setup freelancer profile in the system"""
        return self.vector_store.store_profile(profile_data)
    
    def generate_proposal(self, job_posting: str, tone: str = "professional") -> ProposalResponse:
        """Generate proposal for job posting"""
        
        # Step 1: Analyze job posting
        job_analysis = self.proposal_generator.analyze_job_posting(job_posting)
        
        # Step 2: Search for relevant experience
        query = self._create_search_query(job_analysis)
        relevant_experience = self.vector_store.search_relevant_experience(query)
        
        # Step 3: Generate proposal
        proposal = self.proposal_generator.generate_proposal(job_analysis, relevant_experience, tone)
        
        # Step 4: Calculate confidence score
        confidence = self.proposal_generator.calculate_confidence_score(job_analysis, relevant_experience)
        
        # Step 5: Extract matched skills
        matched_skills = self._extract_matched_skills(job_analysis, relevant_experience)
        
        # Store in history
        proposal_data = {
            "id": str(uuid.uuid4()),
            "job_posting": job_posting,
            "proposal": proposal,
            "confidence_score": confidence,
            "generated_at": datetime.now(),
            "matched_skills": matched_skills
        }
        self.proposal_history.append(proposal_data)
        
        # Keep only last 5 proposals
        if len(self.proposal_history) > 5:
            self.proposal_history = self.proposal_history[-5:]
        
        return ProposalResponse(
            proposal=proposal,
            confidence_score=confidence,
            matched_skills=matched_skills,
            generated_at=datetime.now()
        )
    
    def _create_search_query(self, job_analysis: Dict[str, Any]) -> str:
        """Create search query from job analysis"""
        skills_query = " ".join(job_analysis.get('required_skills', []))
        scope_query = job_analysis.get('project_scope', '')
        priorities_query = " ".join(job_analysis.get('key_priorities', []))
        
        return f"{skills_query} {scope_query} {priorities_query}"
    
    def _extract_matched_skills(self, job_analysis: Dict[str, Any], relevant_experience: List[Dict[str, Any]]) -> List[str]:
        """Extract skills that matched from the search"""
        required_skills = job_analysis.get('required_skills', [])
        if not required_skills or not relevant_experience:
            return ["General experience match"]
        
        # Simple matching - in real implementation, use more sophisticated matching
        return required_skills[:3]
    
    def get_proposal_history(self) -> List[Dict[str, Any]]:
        """Get proposal generation history"""
        return self.proposal_history