"""
PDF Export functionality for leads
"""

import logging
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class PDFExporter:
    """Export leads to professional PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='LeadTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=10
        ))
    
    def export_leads(self, leads: List[Dict], filename: str = None) -> str:
        """
        Export leads to PDF
        
        Args:
            leads: List of lead dictionaries
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated PDF file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/exports/leads_export_{timestamp}.pdf"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("RagsPro Lead Generation Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        summary_text = f"""
        <b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        <b>Total Leads:</b> {len(leads)}<br/>
        <b>Average Quality:</b> {sum(l.get('quality_score', 0) for l in leads) / len(leads):.1f}/100
        """
        summary = Paragraph(summary_text, self.styles['Normal'])
        story.append(summary)
        story.append(Spacer(1, 0.3*inch))
        
        # Leads table
        for i, lead in enumerate(leads, 1):
            # Lead header
            lead_title = Paragraph(f"{i}. {lead.get('title', 'Unknown')}", self.styles['LeadTitle'])
            story.append(lead_title)
            
            # Lead details table
            data = [
                ['Type:', lead.get('type', 'N/A')],
                ['Location:', lead.get('address', 'N/A')],
                ['Rating:', f"{lead.get('rating', 0)}★ ({lead.get('reviews', 0)} reviews)"],
                ['Quality Score:', f"{lead.get('quality_score', 0)}/100"],
                ['Phone:', lead.get('phone', 'N/A')],
                ['Website:', lead.get('website', 'N/A')],
            ]
            
            table = Table(data, colWidths=[1.5*inch, 4.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.2*inch))
            
            # Page break every 3 leads
            if i % 3 == 0 and i < len(leads):
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF exported: {filename}")
        
        return filename
    
    def export_single_lead(self, lead: Dict, filename: str = None) -> str:
        """Export single lead with detailed information"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = lead.get('title', 'lead').replace(' ', '_')[:30]
            filename = f"data/exports/{safe_name}_{timestamp}.pdf"
        
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(f"Lead Profile: {lead.get('title', 'Unknown')}", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Detailed information
        sections = [
            ('Business Information', [
                ('Name', lead.get('title', 'N/A')),
                ('Type', lead.get('type', 'N/A')),
                ('Address', lead.get('address', 'N/A')),
                ('City', lead.get('city', 'N/A')),
            ]),
            ('Contact Details', [
                ('Phone', lead.get('phone', 'N/A')),
                ('Website', lead.get('website', 'N/A')),
                ('Email', lead.get('email', 'N/A')),
            ]),
            ('Performance Metrics', [
                ('Rating', f"{lead.get('rating', 0)}★"),
                ('Reviews', str(lead.get('reviews', 0))),
                ('Quality Score', f"{lead.get('quality_score', 0)}/100"),
            ]),
        ]
        
        for section_title, section_data in sections:
            # Section header
            header = Paragraph(section_title, self.styles['Heading2'])
            story.append(header)
            story.append(Spacer(1, 0.1*inch))
            
            # Section table
            table = Table(section_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.3*inch))
        
        # AI Content if available
        if 'ai_content' in lead:
            story.append(Paragraph("AI-Generated Content", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            ai_content = lead['ai_content']
            for content_type in ['email', 'whatsapp', 'call_script']:
                if content_type in ai_content:
                    story.append(Paragraph(f"<b>{content_type.title()}:</b>", self.styles['Normal']))
                    story.append(Paragraph(ai_content[content_type], self.styles['Normal']))
                    story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        logger.info(f"Single lead PDF exported: {filename}")
        
        return filename


def create_pdf_exporter():
    """Factory function"""
    return PDFExporter()
