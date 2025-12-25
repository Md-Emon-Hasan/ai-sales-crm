import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailSender:
    """Agent for sending personalized outreach emails via SMTP"""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "mailhog")
        self.smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        self.from_email = os.getenv("FROM_EMAIL", "sales@crm.local")
        self.from_name = os.getenv("FROM_NAME", "Sales Team")
    
    def send_outreach(self, lead: dict) -> bool:
        """
        Send personalized outreach email to a lead
        
        Args:
            lead: Dictionary containing lead information including personalized_email
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        to_email = lead.get('email')
        to_name = lead.get('name', 'there')
        email_body = lead.get('personalized_email', '')
        company = lead.get('company', 'your company')
        
        if not to_email or not email_body:
            print(f"  Missing email or body for {to_name}")
            return False
        
        # Create email subject
        subject = f"Quick question about {company}'s growth"
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = f"{to_name} <{to_email}>"
            
            # Create plain text version
            text_content = f"""
Hi {to_name},

{email_body}

Best regards,
{self.from_name}

---
This is an automated outreach email from AI Sales CRM
"""
            
            # Create HTML version
            html_content = f"""
<html>
  <head></head>
  <body>
    <p>Hi {to_name},</p>
    {email_body.replace(chr(10), '<br>')}
    <p>Best regards,<br>
    {self.from_name}</p>
    <hr>
    <p style="color: #666; font-size: 12px;">
      This is an automated outreach email from AI Sales CRM
    </p>
  </body>
</html>
"""
            
            # Attach both versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                # MailHog doesn't require authentication
                server.send_message(msg)
            
            print(f" Email sent to {to_name} ({to_email})")
            return True
        
        except Exception as e:
            print(f" Failed to send email to {to_name}: {e}")
            return False
    
    def send_batch(self, leads: list) -> dict:
        """
        Send emails to multiple leads
        
        Returns:
            dict: Statistics about sent emails
        """
        
        sent = 0
        failed = 0
        
        for lead in leads:
            if self.send_outreach(lead):
                sent += 1
            else:
                failed += 1
        
        return {
            "total": len(leads),
            "sent": sent,
            "failed": failed,
            "success_rate": f"{(sent/len(leads)*100):.1f}%" if leads else "0%"
        }