import chromadb
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import uuid
import os

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        
        # Use HuggingFace embeddings / OpenAI embeddings
        try:
            self.embeddings = OpenAIEmbeddings()
        except:
            # Fallback to local embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("freelancer_profiles")
        
        # LangChain Chroma instance for similarity search
        self.vector_store = Chroma(
            collection_name="freelancer_profiles",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
    
    def store_profile(self, profile_data: Dict[str, Any]) -> str:
        """Store freelancer profile in vector database"""
        profile_id = str(uuid.uuid4())
        
        # Create document from profile data
        profile_text = self._format_profile_text(profile_data)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        documents = text_splitter.create_documents([profile_text])
        
        # Add metadata and store
        for i, doc in enumerate(documents):
            doc.metadata = {
                "profile_id": profile_id,
                "name": profile_data.get("name", ""),
                "skills": ", ".join(profile_data.get("skills", [])),
                "chunk_id": i
            }
        
        self.vector_store.add_documents(documents)
        return profile_id
    
    def _format_profile_text(self, profile_data: Dict[str, Any]) -> str:
        """Format profile data into searchable text"""
        skills_text = ", ".join(profile_data.get("skills", []))
        projects_text = "\n".join([f"- {project}" for project in profile_data.get("past_projects", [])])
        
        return f"""
        Name: {profile_data.get('name', '')}
        Skills: {skills_text}
        Experience: {profile_data.get('experience', '')}
        Past Projects:
        {projects_text}
        Rates: {profile_data.get('rates', 'Not specified')}
        Bio: {profile_data.get('bio', '')}
        """
    
    def search_relevant_experience(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant experience based on job requirements"""
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": float(1 - score)  # Convert to similarity score
            })
        
        return formatted_results
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all stored profiles"""
        return self.collection.get()