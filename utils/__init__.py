"""
Utility modules for Sales Campaign CRM
"""

from .report_generator import ReportGenerator

__all__ = ['ReportGenerator']



# # Step 1: Docker containers build o start koro
# docker-compose up --build

# # Ekta new terminal kholo, then:

# # Step 2: 10 second wait koro
# sleep 10

# # Step 3: Health check koro
# curl http://localhost:8000/health

# # Dekhbe: {"status":"healthy",...}

# # Step 4: Campaign start koro
# curl -X POST http://localhost:8000/-campaignprocess