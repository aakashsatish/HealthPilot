import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@healthpilot.com")
        
    def send_report_email(self, to_email: str, report_data: dict, user_name: str = "User") -> bool:
        """Send lab report analysis via email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = f"Your Lab Report Analysis - {report_data.get('original_filename', 'Report')}"
            
            # Create HTML content
            html_content = self._create_report_html(report_data, user_name)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            if self.smtp_username and self.smtp_password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                server.quit()
                logger.info(f"Report email sent to {to_email}")
                return True
            else:
                logger.warning("SMTP credentials not configured, email not sent")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _create_report_html(self, report_data: dict, user_name: str) -> str:
        """Create HTML content for the email"""
        
        # Get analysis data
        analysis_result = report_data.get('analysis_result', {})
        results = analysis_result.get('results', [])
        summary = analysis_result.get('summary', '')
        risk_assessment = analysis_result.get('risk_assessment', {})
        recommendations = analysis_result.get('recommendations', [])
        early_warnings = analysis_result.get('early_warnings', [])
        
        # Create results table HTML
        results_table = ""
        if results:
            results_table = """
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Test</th>
                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Value</th>
                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Reference Range</th>
                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6;">Status</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for i, result in enumerate(results):
                bg_color = "#f8f9fa" if i % 2 == 0 else "#ffffff"
                status_color = self._get_status_color(result.get('classification', ''))
                
                results_table += f"""
                    <tr style="background-color: {bg_color};">
                        <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{result.get('original_name', '')}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{result.get('value', '')} {result.get('unit', '')}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">{result.get('reference_range', '')}</td>
                        <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">
                            <span style="padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; {status_color}">
                                {result.get('classification', '')}
                            </span>
                        </td>
                    </tr>
                """
            
            results_table += """
                </tbody>
            </table>
            """
        
        # Create recommendations HTML
        recommendations_html = ""
        if recommendations:
            recommendations_html = """
            <h3 style="color: #28a745; margin-top: 30px;">Recommendations</h3>
            <ul style="margin: 15px 0; padding-left: 20px;">
            """
            for rec in recommendations:
                recommendations_html += f'<li style="margin: 8px 0;">{rec}</li>'
            recommendations_html += "</ul>"
        
        # Create warnings HTML
        warnings_html = ""
        if early_warnings:
            warnings_html = """
            <h3 style="color: #dc3545; margin-top: 30px;">⚠️ Early Warning Signals</h3>
            """
            for warning in early_warnings:
                severity_color = "#dc3545" if warning.get('severity') == 'HIGH' else "#ffc107"
                warnings_html += f"""
                <div style="border-left: 4px solid {severity_color}; padding-left: 15px; margin: 15px 0;">
                    <p style="margin: 5px 0;"><strong>{warning.get('type', '')} - {warning.get('severity', '')}</strong></p>
                    <p style="margin: 5px 0;">{warning.get('message', '')}</p>
                    <p style="margin: 5px 0; color: #6c757d;"><strong>Action:</strong> {warning.get('action', '')}</p>
                </div>
                """
        
        # Create risk assessment HTML
        risk_html = ""
        if risk_assessment:
            risk_level = risk_assessment.get('risk_level', 'UNKNOWN')
            risk_color = self._get_risk_color(risk_level)
            risk_html = f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Risk Assessment</h3>
                <p><strong>Risk Level:</strong> <span style="padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; {risk_color}">{risk_level}</span></p>
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Lab Report Analysis</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 28px;">HealthPilot</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Your AI-Powered Health Analysis</p>
            </div>
            
            <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                Lab Report Analysis
            </h2>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Report Summary</h3>
                <p><strong>File:</strong> {report_data.get('original_filename', 'Unknown')}</p>
                <p><strong>Date:</strong> {datetime.fromisoformat(report_data.get('created_at', '')).strftime('%B %d, %Y')}</p>
                <p><strong>Summary:</strong> {summary}</p>
            </div>
            
            {risk_html}
            
            <h3 style="color: #2c3e50; margin-top: 30px;">Lab Results</h3>
            {results_table}
            
            {recommendations_html}
            
            {warnings_html}
            
            <div style="background-color: #e9ecef; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: center;">
                <p style="margin: 0; color: #6c757d;">
                    <strong>Important:</strong> This analysis is for informational purposes only and should not replace professional medical advice. 
                    Always consult with your healthcare provider for medical decisions.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <p style="color: #6c757d; font-size: 14px;">
                    Generated by HealthPilot on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _get_status_color(self, classification: str) -> str:
        """Get CSS color for test status"""
        if classification == 'NORMAL':
            return "background-color: #d4edda; color: #155724;"
        elif classification in ['HIGH', 'LOW']:
            return "background-color: #fff3cd; color: #856404;"
        else:
            return "background-color: #f8d7da; color: #721c24;"
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get CSS color for risk level"""
        if risk_level == 'LOW':
            return "background-color: #d4edda; color: #155724;"
        elif risk_level == 'MODERATE':
            return "background-color: #fff3cd; color: #856404;"
        elif risk_level == 'HIGH':
            return "background-color: #f8d7da; color: #721c24;"
        else:
            return "background-color: #e2e3e5; color: #383d41;" 