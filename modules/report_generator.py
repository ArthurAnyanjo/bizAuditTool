from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from io import BytesIO
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Comprehensive report generation for SEO audit and content analysis
    """
    
    def __init__(self):
        """Initialize report generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E3440')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#3B4252')
        )
        
        # Section heading
        self.section_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.HexColor('#5E81AC'),
            borderWidth=1,
            borderColor=colors.HexColor('#D8DEE9'),
            borderPadding=10,
            backColor=colors.HexColor('#ECEFF4')
        )
        
        # Score style
        self.score_style = ParagraphStyle(
            'ScoreStyle',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E3440')
        )
        
        # Recommendation style
        self.rec_style = ParagraphStyle(
            'RecommendationStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=5,
            spaceAfter=5,
            leftIndent=20,
            bulletIndent=10,
            bulletFontName='Helvetica-Bold',
            bulletColor=colors.HexColor('#5E81AC')
        )
        
        # Issue style (red)
        self.issue_style = ParagraphStyle(
            'IssueStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=5,
            spaceAfter=5,
            leftIndent=20,
            textColor=colors.HexColor('#BF616A')
        )
        
        # Success style (green)
        self.success_style = ParagraphStyle(
            'SuccessStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=5,
            spaceAfter=5,
            leftIndent=20,
            textColor=colors.HexColor('#A3BE8C')
        )
    
    def generate_report(self, url: str, audit_data: Dict[str, Any], 
                       content_data: Dict[str, Any], format_type: str = 'pdf') -> bytes:
        """
        Generate comprehensive SEO audit report
        
        Args:
            url: Website URL
            audit_data: PageSpeed audit results  
            content_data: Content analysis results
            format_type: Output format ('pdf', 'html', 'json')
            
        Returns:
            Report data as bytes
        """
        try:
            logger.info(f"Generating {format_type.upper()} report for {url}")
            
            if format_type == 'pdf':
                return self._generate_pdf_report(url, audit_data, content_data)
            elif format_type == 'html':
                return self._generate_html_report(url, audit_data, content_data)
            elif format_type == 'json':
                return self._generate_json_report(url, audit_data, content_data)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
                
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise Exception(f"Report generation failed: {str(e)}")
    
    def _generate_pdf_report(self, url: str, audit_data: Dict[str, Any], 
                           content_data: Dict[str, Any]) -> bytes:
        """Generate PDF report"""
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Title page
        story.extend(self._build_title_page(url))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._build_executive_summary(audit_data, content_data))
        story.append(PageBreak())
        
        # Performance analysis
        story.extend(self._build_performance_section(audit_data))
        story.append(PageBreak())
        
        # SEO analysis
        story.extend(self._build_seo_section(audit_data, content_data))
        story.append(PageBreak())
        
        # Content analysis
        story.extend(self._build_content_section(content_data))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._build_recommendations_section(audit_data, content_data))
        story.append(PageBreak())
        
        # Technical details
        story.extend(self._build_technical_section(audit_data, content_data))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _build_title_page(self, url: str) -> List:
        """Build title page elements"""
        elements = []
        
        # Main title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("SEO Audit Report", self.title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # URL
        elements.append(Paragraph(f"<b>Website:</b> {url}", self.subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"<b>Generated:</b> {current_date}", self.styles['Normal']))
        elements.append(Spacer(1, 2*inch))
        
        # Report overview
        overview_text = """
        This comprehensive SEO audit report provides detailed analysis of your website's 
        performance, search engine optimization, content quality, and technical implementation. 
        The report includes actionable recommendations to improve your website's visibility, 
        user experience, and search engine rankings.
        """
        elements.append(Paragraph(overview_text, self.styles['Normal']))
        
        return elements
    
    def _build_executive_summary(self, audit_data: Dict[str, Any], 
                               content_data: Dict[str, Any]) -> List:
        """Build executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.section_style))
        elements.append(Spacer(1, 20))
        
        # Overall scores table
        scores_data = self._extract_summary_scores(audit_data, content_data)
        
        # Create scores table
        table_data = [
            ['Metric', 'Mobile Score', 'Desktop Score', 'Status'],
        ]
        
        for metric, data in scores_data.items():
            mobile_score = data.get('mobile', 'N/A')
            desktop_score = data.get('desktop', 'N/A')
            status = self._get_score_status(mobile_score if mobile_score != 'N/A' else desktop_score)
            
            table_data.append([
                metric,
                f"{mobile_score}" if mobile_score != 'N/A' else 'N/A',
                f"{desktop_score}" if desktop_score != 'N/A' else 'N/A',
                status
            ])
        
        scores_table = Table(table_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5E81AC')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(scores_table)
        elements.append(Spacer(1, 30))
        
        # Key findings
        elements.append(Paragraph("Key Findings", self.subtitle_style))
        
        key_findings = self._generate_key_findings(audit_data, content_data)
        for finding in key_findings:
            elements.append(Paragraph(f"• {finding}", self.styles['Normal']))
            elements.append(Spacer(1, 5))
        
        elements.append(Spacer(1, 20))
        
        # Priority recommendations
        elements.append(Paragraph("Top Priority Recommendations", self.subtitle_style))
        
        priority_recs = self._get_priority_recommendations(audit_data, content_data)
        for i, rec in enumerate(priority_recs[:5], 1):
            elements.append(Paragraph(f"{i}. {rec}", self.rec_style))
        
        return elements
    
    def _build_performance_section(self, audit_data: Dict[str, Any]) -> List:
        """Build performance analysis section"""
        elements = []
        
        elements.append(Paragraph("Performance Analysis", self.section_style))
        elements.append(Spacer(1, 20))
        
        # Core Web Vitals for each device
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                elements.append(Paragraph(f"{device.title()} Performance", self.subtitle_style))
                
                # Performance score
                perf_score = int(data.get('performance_score', 0) * 100)
                score_color = self._get_score_color(perf_score)
                elements.append(Paragraph(
                    f"<font color='{score_color}'>Overall Performance Score: {perf_score}/100</font>",
                    self.score_style
                ))
                elements.append(Spacer(1, 15))
                
                # Core Web Vitals
                vitals = data.get('core_web_vitals', {})
                if vitals:
                    vitals_data = [
                        ['Metric', 'Value', 'Score', 'Status']
                    ]
                    
                    for vital_name, vital_data in vitals.items():
                        if isinstance(vital_data, dict):
                            value = vital_data.get('display_value', vital_data.get('value', 'N/A'))
                            score = int(vital_data.get('score', 0) * 100) if vital_data.get('score') else 'N/A'
                            status = self._get_score_status(score) if score != 'N/A' else 'N/A'
                            
                            vitals_data.append([
                                vital_name.replace('_', ' ').title(),
                                str(value),
                                str(score) if score != 'N/A' else 'N/A',
                                status
                            ])
                    
                    if len(vitals_data) > 1:  # Has data beyond header
                        vitals_table = Table(vitals_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch])
                        vitals_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4C566A')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECEFF4')),
                            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D8DEE9'))
                        ]))
                        elements.append(vitals_table)
                
                # Opportunities
                opportunities = data.get('opportunities', [])[:5]  # Top 5
                if opportunities:
                    elements.append(Spacer(1, 20))
                    elements.append(Paragraph("Top Performance Opportunities", self.subtitle_style))
                    
                    for opp in opportunities:
                        title = opp.get('title', 'Unknown')
                        savings = opp.get('savings_ms', 0)
                        impact = opp.get('impact', 'UNKNOWN')
                        
                        opp_text = f"<b>{title}</b>"
                        if savings > 0:
                            opp_text += f" - Potential savings: {savings:.0f}ms ({impact} impact)"
                        
                        elements.append(Paragraph(f"• {opp_text}", self.styles['Normal']))
                        
                        # Add description if available
                        if opp.get('description'):
                            desc = opp['description'][:200] + '...' if len(opp['description']) > 200 else opp['description']
                            elements.append(Paragraph(f"  {desc}", self.styles['Normal']))
                        
                        elements.append(Spacer(1, 8))
                
                elements.append(Spacer(1, 30))
        
        return elements
    
    def _build_seo_section(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> List:
        """Build SEO analysis section"""
        elements = []
        
        elements.append(Paragraph("SEO Analysis", self.section_style))
        elements.append(Spacer(1, 20))
        
        # Get SEO scores from audit data
        seo_scores = {}
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                seo_scores[device] = int(data.get('seo_score', 0) * 100)
        
        # SEO Score summary
        if seo_scores:
            elements.append(Paragraph("SEO Score Summary", self.subtitle_style))
            
            for device, score in seo_scores.items():
                score_color = self._get_score_color(score)
                elements.append(Paragraph(
                    f"<font color='{score_color}'>{device.title()} SEO Score: {score}/100</font>",
                    self.score_style
                ))
            
            elements.append(Spacer(1, 20))
        
        # Content analysis SEO elements
        seo_analysis = content_data.get('analysis', {}).get('seo_elements', {})
        if seo_analysis:
            # Title analysis
            title_analysis = seo_analysis.get('title_analysis', {})
            if title_analysis:
                elements.append(Paragraph("Title Tag Analysis", self.subtitle_style))
                
                if title_analysis.get('missing_titles', 0) > 0:
                    elements.append(Paragraph(
                        f"• {title_analysis['missing_titles']} pages missing title tags",
                        self.issue_style
                    ))
                
                if title_analysis.get('long_titles', 0) > 0:
                    elements.append(Paragraph(
                        f"• {title_analysis['long_titles']} pages with titles over 60 characters",
                        self.issue_style
                    ))
                
                if title_analysis.get('duplicate_titles', 0) > 0:
                    elements.append(Paragraph(
                        f"• {title_analysis['duplicate_titles']} duplicate title tags found",
                        self.issue_style
                    ))
                
                avg_length = title_analysis.get('avg_title_length', 0)
                elements.append(Paragraph(
                    f"• Average title length: {avg_length:.0f} characters",
                    self.styles['Normal']
                ))
                
                elements.append(Spacer(1, 15))
            
            # Meta description analysis
            meta_analysis = seo_analysis.get('meta_description_analysis', {})
            if meta_analysis:
                elements.append(Paragraph("Meta Description Analysis", self.subtitle_style))
                
                if meta_analysis.get('missing_descriptions', 0) > 0:
                    elements.append(Paragraph(
                        f"• {meta_analysis['missing_descriptions']} pages missing meta descriptions",
                        self.issue_style
                    ))
                
                if meta_analysis.get('long_descriptions', 0) > 0:
                    elements.append(Paragraph(
                        f"• {meta_analysis['long_descriptions']} pages with descriptions over 160 characters",
                        self.issue_style
                    ))
                
                avg_desc_length = meta_analysis.get('avg_description_length', 0)
                elements.append(Paragraph(
                    f"• Average description length: {avg_desc_length:.0f} characters",
                    self.styles['Normal']
                ))
                
                elements.append(Spacer(1, 15))
            
            # Heading analysis
            heading_analysis = seo_analysis.get('heading_analysis', {})
            if heading_analysis:
                elements.append(Paragraph("Heading Structure Analysis", self.subtitle_style))
                
                h1_issues = heading_analysis.get('h1_issues', [])
                if h1_issues:
                    elements.append(Paragraph(
                        f"• {len(h1_issues)} H1 tag issues found",
                        self.issue_style
                    ))
                
                heading_dist = heading_analysis.get('heading_distribution', {})
                if heading_dist:
                    elements.append(Paragraph("• Header distribution:", self.styles['Normal']))
                    for level, count in heading_dist.items():
                        elements.append(Paragraph(
                            f"  {level.upper()}: {count} tags",
                            self.styles['Normal']
                        ))
                
                elements.append(Spacer(1, 15))
            
            # Image SEO analysis
            image_analysis = seo_analysis.get('image_analysis', {})
            if image_analysis:
                elements.append(Paragraph("Image SEO Analysis", self.subtitle_style))
                
                total_images = image_analysis.get('total_images', 0)
                missing_alt = image_analysis.get('images_without_alt', 0)
                
                elements.append(Paragraph(f"• Total images: {total_images}", self.styles['Normal']))
                
                if missing_alt > 0:
                    elements.append(Paragraph(
                        f"• {missing_alt} images missing alt text ({(missing_alt/total_images)*100:.1f}%)",
                        self.issue_style
                    ))
                else:
                    elements.append(Paragraph("• All images have alt text", self.success_style))
                
                elements.append(Spacer(1, 15))
        
        return elements
    
    def _build_content_section(self, content_data: Dict[str, Any]) -> List:
        """Build content analysis section"""
        elements = []
        
        elements.append(Paragraph("Content Analysis", self.section_style))
        elements.append(Spacer(1, 20))
        
        analysis = content_data.get('analysis', {})
        
        # Content overview
        content_structure = analysis.get('content_structure', {})
        if content_structure:
            elements.append(Paragraph("Content Overview", self.subtitle_style))
            
            total_pages = content_structure.get('total_pages', 0)
            elements.append(Paragraph(f"• Total pages analyzed: {total_pages}", self.styles['Normal']))
            
            page_types = content_structure.get('page_types', {})
            if page_types:
                elements.append(Paragraph("• Page types found:", self.styles['Normal']))
                for page_type, count in page_types.items():
                    elements.append(Paragraph(f"  - {page_type.title()}: {count} pages", self.styles['Normal']))
            
            avg_sections = content_structure.get('avg_sections_per_page', 0)
            elements.append(Paragraph(f"• Average sections per page: {avg_sections:.1f}", self.styles['Normal']))
            
            elements.append(Spacer(1, 15))
        
        # Content quality
        content_quality = analysis.get('content_quality', {})
        if content_quality:
            elements.append(Paragraph("Content Quality Metrics", self.subtitle_style))
            
            total_words = content_quality.get('total_word_count', 0)
            avg_words = content_quality.get('avg_word_count_per_page', 0)
            avg_readability = content_quality.get('avg_readability_score', 0)
            quality_score = content_quality.get('overall_quality_score', 0)
            
            elements.append(Paragraph(f"• Total word count: {total_words:,}", self.styles['Normal']))
            elements.append(Paragraph(f"• Average words per page: {avg_words:.0f}", self.styles['Normal']))
            elements.append(Paragraph(f"• Average readability score: {avg_readability:.1f}/100", self.styles['Normal']))
            
            quality_color = self._get_score_color(quality_score)
            elements.append(Paragraph(
                f"• <font color='{quality_color}'>Overall content quality: {quality_score:.1f}/100</font>",
                self.styles['Normal']
            ))
            
            elements.append(Spacer(1, 15))
        
        # Keyword analysis
        keyword_analysis = analysis.get('keyword_analysis', {})
        if keyword_analysis:
            elements.append(Paragraph("Keyword Analysis", self.subtitle_style))
            
            primary_keywords = keyword_analysis.get('primary_keywords', [])[:10]
            if primary_keywords:
                elements.append(Paragraph("• Top content keywords:", self.styles['Normal']))
                keyword_text = ", ".join(primary_keywords)
                elements.append(Paragraph(f"  {keyword_text}", self.styles['Normal']))
            
            total_keywords = keyword_analysis.get('total_unique_keywords', 0)
            elements.append(Paragraph(f"• Total unique keywords: {total_keywords}", self.styles['Normal']))
            
            elements.append(Spacer(1, 15))
        
        # Content gaps
        content_gaps = analysis.get('content_gaps', {})
        if content_gaps:
            elements.append(Paragraph("Content Gap Analysis", self.subtitle_style))
            
            missing_pages = content_gaps.get('missing_pages', [])
            if missing_pages:
                elements.append(Paragraph("• Missing essential pages:", self.issue_style))
                for page in missing_pages:
                    elements.append(Paragraph(f"  - {page['description']}", self.styles['Normal']))
            
            thin_content = content_gaps.get('thin_content_pages', [])
            if thin_content:
                elements.append(Paragraph(
                    f"• {len(thin_content)} pages with thin content (<300 words)",
                    self.issue_style
                ))
            
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _build_recommendations_section(self, audit_data: Dict[str, Any], 
                                     content_data: Dict[str, Any]) -> List:
        """Build recommendations section"""
        elements = []
        
        elements.append(Paragraph("Recommendations", self.section_style))
        elements.append(Spacer(1, 20))
        
        # Get recommendations from content analysis
        recommendations = content_data.get('analysis', {}).get('recommendations', [])
        
        # Priority recommendations
        elements.append(Paragraph("High Priority Recommendations", self.subtitle_style))
        
        high_priority = self._categorize_recommendations(recommendations, 'high')
        for i, rec in enumerate(high_priority[:5], 1):
            elements.append(Paragraph(f"{i}. {rec}", self.rec_style))
        
        elements.append(Spacer(1, 20))
        
        # Medium priority recommendations
        elements.append(Paragraph("Medium Priority Recommendations", self.subtitle_style))
        
        medium_priority = self._categorize_recommendations(recommendations, 'medium')
        for i, rec in enumerate(medium_priority[:5], 1):
            elements.append(Paragraph(f"{i}. {rec}", self.rec_style))
        
        elements.append(Spacer(1, 20))
        
        # Performance-specific recommendations
        perf_recommendations = self._extract_performance_recommendations(audit_data)
        if perf_recommendations:
            elements.append(Paragraph("Performance Optimization", self.subtitle_style))
            for i, rec in enumerate(perf_recommendations[:5], 1):
                elements.append(Paragraph(f"{i}. {rec}", self.rec_style))
        
        return elements
    
    def _build_technical_section(self, audit_data: Dict[str, Any], 
                               content_data: Dict[str, Any]) -> List:
        """Build technical details section"""
        elements = []
        
        elements.append(Paragraph("Technical Analysis", self.section_style))
        elements.append(Spacer(1, 20))
        
        # Technical SEO from content analysis
        technical_seo = content_data.get('analysis', {}).get('technical_seo', {})
        if technical_seo:
            elements.append(Paragraph("Technical SEO", self.subtitle_style))
            
            # URL analysis
            url_analysis = technical_seo.get('url_analysis', {})
            if url_analysis:
                url_issues = url_analysis.get('issues', [])
                avg_length = url_analysis.get('avg_url_length', 0)
                
                elements.append(Paragraph(f"• Average URL length: {avg_length:.0f} characters", self.styles['Normal']))
                
                if url_issues:
                    elements.append(Paragraph("• URL issues found:", self.issue_style))
                    for issue in url_issues[:5]:
                        elements.append(Paragraph(f"  - {issue}", self.styles['Normal']))
                else:
                    elements.append(Paragraph("• No major URL issues found", self.success_style))
            
            # HTTPS analysis
            https_analysis = technical_seo.get('https_analysis', {})
            if https_analysis:
                uses_https = https_analysis.get('uses_https', False)
                if uses_https:
                    elements.append(Paragraph("• Site uses HTTPS", self.success_style))
                else:
                    elements.append(Paragraph("• Site not using HTTPS", self.issue_style))
            
            # Structured data
            structured_data = technical_seo.get('structured_data_analysis', {})
            if structured_data:
                has_schema = structured_data.get('has_structured_data', False)
                if has_schema:
                    schema_count = structured_data.get('count', 0)
                    elements.append(Paragraph(f"• {schema_count} structured data items found", self.success_style))
                else:
                    elements.append(Paragraph("• No structured data found", self.issue_style))
            
            elements.append(Spacer(1, 15))
        
        # Performance metrics details
        elements.append(Paragraph("Performance Metrics Details", self.subtitle_style))
        
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                elements.append(Paragraph(f"{device.title()} Metrics:", self.styles['Normal']))
                
                # Resource summary
                resource_summary = data.get('resource_summary', {})
                if resource_summary:
                    total_size = resource_summary.get('total_byte_weight', 0) / 1024  # Convert to KB
                    total_requests = resource_summary.get('total_requests', 0)
                    
                    elements.append(Paragraph(f"  - Total page size: {total_size:.0f} KB", self.styles['Normal']))
                    elements.append(Paragraph(f"  - Total requests: {total_requests}", self.styles['Normal']))
                    elements.append(Paragraph(f"  - Images: {resource_summary.get('image_count', 0)}", self.styles['Normal']))
                    elements.append(Paragraph(f"  - Scripts: {resource_summary.get('script_count', 0)}", self.styles['Normal']))
                    elements.append(Paragraph(f"  - Stylesheets: {resource_summary.get('stylesheet_count', 0)}", self.styles['Normal']))
                
                elements.append(Spacer(1, 10))
        
        return elements
    
    def _generate_html_report(self, url: str, audit_data: Dict[str, Any], 
                            content_data: Dict[str, Any]) -> bytes:
        """Generate HTML report"""
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SEO Audit Report - {url}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #5E81AC; padding-bottom: 20px; margin-bottom: 30px; }}
                .section {{ margin-bottom: 40px; }}
                .section h2 {{ color: #5E81AC; border-left: 4px solid #5E81AC; padding-left: 15px; }}
                .score-card {{ display: inline-block; margin: 10px; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; }}
                .score-excellent {{ background-color: #A3BE8C; color: white; }}
                .score-good {{ background-color: #EBCB8B; color: white; }}
                .score-poor {{ background-color: #BF616A; color: white; }}
                .recommendation {{ background-color: #ECEFF4; padding: 15px; margin: 10px 0; border-left: 4px solid #5E81AC; }}
                .issue {{ background-color: #FADBD8; padding: 10px; margin: 5px 0; border-left: 4px solid #BF616A; }}
                .success {{ background-color: #D5EDDA; padding: 10px; margin: 5px 0; border-left: 4px solid #A3BE8C; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #5E81AC; color: white; }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SEO Audit Report</h1>
                    <p><strong>Website:</strong> {url}</p>
                    <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                {self._generate_html_summary(audit_data, content_data)}
                {self._generate_html_performance(audit_data)}
                {self._generate_html_seo(audit_data, content_data)}
                {self._generate_html_content(content_data)}
                {self._generate_html_recommendations(audit_data, content_data)}
            </div>
        </body>
        </html>
        """
        
        return html_template.encode('utf-8')
    
    def _generate_html_summary(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> str:
        """Generate HTML summary section"""
        scores = self._extract_summary_scores(audit_data, content_data)
        
        score_cards = ""
        for metric, data in scores.items():
            mobile_score = data.get('mobile', 'N/A')
            desktop_score = data.get('desktop', 'N/A')
            
            # Use mobile score for display if available, otherwise desktop
            display_score = mobile_score if mobile_score != 'N/A' else desktop_score
            score_class = self._get_score_class(display_score)
            
            score_cards += f"""
            <div class="score-card {score_class}">
                <h3>{metric}</h3>
                <p>Mobile: {mobile_score}</p>
                <p>Desktop: {desktop_score}</p>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="metric-grid">
                {score_cards}
            </div>
            <h3>Key Findings</h3>
            {self._generate_html_findings(audit_data, content_data)}
        </div>
        """
    
    def _generate_html_performance(self, audit_data: Dict[str, Any]) -> str:
        """Generate HTML performance section"""
        performance_html = '<div class="section"><h2>Performance Analysis</h2>'
        
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                perf_score = int(data.get('performance_score', 0) * 100)
                score_class = self._get_score_class(perf_score)
                
                performance_html += f"""
                <h3>{device.title()} Performance</h3>
                <div class="score-card {score_class}">
                    <h4>Performance Score</h4>
                    <p>{perf_score}/100</p>
                </div>
                """
                
                # Core Web Vitals
                vitals = data.get('core_web_vitals', {})
                if vitals:
                    performance_html += "<h4>Core Web Vitals</h4><table><tr><th>Metric</th><th>Value</th><th>Score</th></tr>"
                    
                    for vital_name, vital_data in vitals.items():
                        if isinstance(vital_data, dict):
                            value = vital_data.get('display_value', vital_data.get('value', 'N/A'))
                            score = int(vital_data.get('score', 0) * 100) if vital_data.get('score') else 'N/A'
                            
                            performance_html += f"""
                            <tr>
                                <td>{vital_name.replace('_', ' ').title()}</td>
                                <td>{value}</td>
                                <td>{score}</td>
                            </tr>
                            """
                    
                    performance_html += "</table>"
                
                # Top opportunities
                opportunities = data.get('opportunities', [])[:3]
                if opportunities:
                    performance_html += "<h4>Top Opportunities</h4>"
                    for opp in opportunities:
                        performance_html += f'<div class="recommendation">{opp.get("title", "Unknown")}</div>'
        
        performance_html += '</div>'
        return performance_html
    
    def _generate_html_seo(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> str:
        """Generate HTML SEO section"""
        seo_html = '<div class="section"><h2>SEO Analysis</h2>'
        
        # SEO scores
        seo_scores = {}
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                seo_scores[device] = int(data.get('seo_score', 0) * 100)
        
        if seo_scores:
            for device, score in seo_scores.items():
                score_class = self._get_score_class(score)
                seo_html += f"""
                <div class="score-card {score_class}">
                    <h4>{device.title()} SEO</h4>
                    <p>{score}/100</p>
                </div>
                """
        
        # SEO issues from content analysis
        seo_analysis = content_data.get('analysis', {}).get('seo_elements', {})
        if seo_analysis:
            title_analysis = seo_analysis.get('title_analysis', {})
            if title_analysis.get('missing_titles', 0) > 0:
                seo_html += f'<div class="issue">Missing title tags: {title_analysis["missing_titles"]} pages</div>'
            
            meta_analysis = seo_analysis.get('meta_description_analysis', {})
            if meta_analysis.get('missing_descriptions', 0) > 0:
                seo_html += f'<div class="issue">Missing meta descriptions: {meta_analysis["missing_descriptions"]} pages</div>'
        
        seo_html += '</div>'
        return seo_html
    
    def _generate_html_content(self, content_data: Dict[str, Any]) -> str:
        """Generate HTML content section"""
        content_html = '<div class="section"><h2>Content Analysis</h2>'
        
        analysis = content_data.get('analysis', {})
        content_quality = analysis.get('content_quality', {})
        
        if content_quality:
            total_words = content_quality.get('total_word_count', 0)
            avg_words = content_quality.get('avg_word_count_per_page', 0)
            quality_score = content_quality.get('overall_quality_score', 0)
            
            content_html += f"""
            <div class="metric-grid">
                <div class="score-card">
                    <h4>Total Words</h4>
                    <p>{total_words:,}</p>
                </div>
                <div class="score-card">
                    <h4>Avg Words/Page</h4>
                    <p>{avg_words:.0f}</p>
                </div>
                <div class="score-card {self._get_score_class(quality_score)}">
                    <h4>Quality Score</h4>
                    <p>{quality_score:.1f}/100</p>
                </div>
            </div>
            """
        
        content_html += '</div>'
        return content_html
    
    def _generate_html_recommendations(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> str:
        """Generate HTML recommendations section"""
        rec_html = '<div class="section"><h2>Recommendations</h2>'
        
        recommendations = content_data.get('analysis', {}).get('recommendations', [])
        
        for i, rec in enumerate(recommendations[:10], 1):
            rec_html += f'<div class="recommendation"><strong>{i}.</strong> {rec}</div>'
        
        rec_html += '</div>'
        return rec_html
    
    def _generate_html_findings(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> str:
        """Generate HTML key findings"""
        findings = self._generate_key_findings(audit_data, content_data)
        
        findings_html = "<ul>"
        for finding in findings[:5]:
            findings_html += f"<li>{finding}</li>"
        findings_html += "</ul>"
        
        return findings_html
    
    def _generate_json_report(self, url: str, audit_data: Dict[str, Any], 
                            content_data: Dict[str, Any]) -> bytes:
        """Generate JSON report"""
        
        report_data = {
            'url': url,
            'generated_at': datetime.now().isoformat(),
            'audit_data': audit_data,
            'content_analysis': content_data.get('analysis', {}),
            'summary_scores': self._extract_summary_scores(audit_data, content_data),
            'key_findings': self._generate_key_findings(audit_data, content_data),
            'recommendations': content_data.get('analysis', {}).get('recommendations', []),
            'report_metadata': {
                'version': '1.0',
                'generator': 'SEO Audit Tool',
                'pages_analyzed': content_data.get('pages_analyzed', 0)
            }
        }
        
        return json.dumps(report_data, indent=2, default=str).encode('utf-8')
    
    # Helper methods
    
    def _extract_summary_scores(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Extract summary scores for overview"""
        scores = {
            'Performance': {'mobile': 'N/A', 'desktop': 'N/A'},
            'SEO': {'mobile': 'N/A', 'desktop': 'N/A'},
            'Accessibility': {'mobile': 'N/A', 'desktop': 'N/A'},
            'Best Practices': {'mobile': 'N/A', 'desktop': 'N/A'}
        }
        
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                scores['Performance'][device] = int(data.get('performance_score', 0) * 100)
                scores['SEO'][device] = int(data.get('seo_score', 0) * 100)
                scores['Accessibility'][device] = int(data.get('accessibility_score', 0) * 100)
                scores['Best Practices'][device] = int(data.get('best_practices_score', 0) * 100)
        
        return scores
    
    def _generate_key_findings(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> List[str]:
        """Generate key findings"""
        findings = []
        
        # Performance findings
        mobile_perf = audit_data.get('mobile', {}).get('performance_score', 0) * 100
        if mobile_perf < 50:
            findings.append("Mobile performance needs significant improvement")
        elif mobile_perf < 90:
            findings.append("Mobile performance has room for optimization")
        
        # SEO findings
        seo_analysis = content_data.get('analysis', {}).get('seo_elements', {})
        if seo_analysis:
            title_issues = seo_analysis.get('title_analysis', {}).get('missing_titles', 0)
            if title_issues > 0:
                findings.append(f"{title_issues} pages missing title tags")
            
            meta_issues = seo_analysis.get('meta_description_analysis', {}).get('missing_descriptions', 0)
            if meta_issues > 0:
                findings.append(f"{meta_issues} pages missing meta descriptions")
        
        # Content findings
        content_quality = content_data.get('analysis', {}).get('content_quality', {})
        if content_quality:
            avg_words = content_quality.get('avg_word_count_per_page', 0)
            if avg_words < 300:
                findings.append("Content is generally thin - pages need more comprehensive content")
        
        # Content gaps
        content_gaps = content_data.get('analysis', {}).get('content_gaps', {})
        missing_pages = content_gaps.get('missing_pages', [])
        if missing_pages:
            findings.append(f"{len(missing_pages)} essential pages are missing")
        
        return findings[:5]  # Return top 5 findings
    
    def _get_priority_recommendations(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> List[str]:
        """Get priority recommendations"""
        recommendations = content_data.get('analysis', {}).get('recommendations', [])
        return self._categorize_recommendations(recommendations, 'high')
    
    def _categorize_recommendations(self, recommendations: List[str], priority: str) -> List[str]:
        """Categorize recommendations by priority"""
        high_priority_keywords = ['title', 'meta description', 'h1', 'https', 'alt text']
        medium_priority_keywords = ['content', 'structure', 'sections', 'readability']
        
        categorized = []
        
        for rec in recommendations:
            rec_lower = rec.lower()
            
            if priority == 'high' and any(keyword in rec_lower for keyword in high_priority_keywords):
                categorized.append(rec)
            elif priority == 'medium' and any(keyword in rec_lower for keyword in medium_priority_keywords):
                categorized.append(rec)
        
        return categorized
    
    def _extract_performance_recommendations(self, audit_data: Dict[str, Any]) -> List[str]:
        """Extract performance-specific recommendations"""
        recommendations = []
        
        for device, data in audit_data.items():
            if device in ['mobile', 'desktop']:
                opportunities = data.get('opportunities', [])
                
                for opp in opportunities[:3]:  # Top 3 opportunities
                    title = opp.get('title', '')
                    impact = opp.get('impact', 'UNKNOWN')
                    
                    if impact in ['HIGH', 'MEDIUM']:
                        recommendations.append(f"{title} ({device})")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _get_score_status(self, score) -> str:
        """Get status text for score"""
        if score == 'N/A':
            return 'N/A'
        
        score = float(score) if isinstance(score, str) else score
        
        if score >= 90:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 50:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def _get_score_color(self, score) -> str:
        """Get color for score"""
        if score == 'N/A':
            return '#4C566A'
        
        score = float(score) if isinstance(score, str) else score
        
        if score >= 90:
            return colors.HexColor('#A3BE8C')
        elif score >= 70:
            return colors.HexColor('#EBCB8B')
        elif score >= 50:
            return colors.HexColor('#D08770')
        else:
            return colors.HexColor('#BF616A')
    
    def _get_score_class(self, score) -> str:
        """Get CSS class for score"""
        if score == 'N/A':
            return 'score-good'
        
        score = float(score) if isinstance(score, str) else score
        
        if score >= 90:
            return 'score-excellent'
        elif score >= 50:
            return 'score-good'
        else:
            return 'score-poor'