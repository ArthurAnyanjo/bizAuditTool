import json
import re
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptGenerator:
    """
    AI Prompt Generator for website redesign
    Creates comprehensive prompts for AI page builders based on audit and content analysis
    """
    
    def __init__(self):
        """Initialize prompt generator"""
        pass
    
    def generate_prompt(self, url: str, audit_data: Dict[str, Any], 
                       content_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive AI prompt for page building
        
        Args:
            url: Website URL
            audit_data: PageSpeed audit results
            content_data: Enhanced content analysis results
            
        Returns:
            Comprehensive AI prompt string
        """
        try:
            logger.info(f"Generating AI prompt for {url}")
            
            # Extract enhanced analysis data
            enhanced_analysis = content_data.get('analysis', {})
            ai_analysis = enhanced_analysis.get('ai_analysis', {})
            basic_analysis = enhanced_analysis.get('basic_analysis', {})
            
            # Generate the comprehensive prompt
            prompt = self._create_enhanced_prompt(url, audit_data, ai_analysis, basic_analysis)
            
            logger.info("AI prompt generation completed successfully")
            return prompt
            
        except Exception as e:
            logger.error(f"Error generating AI prompt: {str(e)}")
            raise Exception(f"AI prompt generation failed: {str(e)}")
    
    def _create_enhanced_prompt(self, url: str, audit_data: Dict[str, Any], 
                               ai_analysis: Dict[str, Any], basic_analysis: Dict[str, Any]) -> str:
        """Create enhanced AI prompt using comprehensive analysis"""
        
        # Extract key information from AI analysis
        brand_identity = ai_analysis.get('brand_identity', {}) or {}
        industry_analysis = ai_analysis.get('industry_analysis', {}) or {}
        target_audience = ai_analysis.get('target_audience', {}) or {}
        website_goals = ai_analysis.get('website_goals', {}) or {}
        value_propositions = ai_analysis.get('value_propositions', {}) or {}
        visual_style = ai_analysis.get('visual_style', {}) or {}
        content_strategy = ai_analysis.get('content_strategy', {}) or {}
        conversion_elements = ai_analysis.get('conversion_elements', {}) or {}
        technical_insights = ai_analysis.get('technical_insights', {}) or {}
        
        # Extract performance issues
        performance_issues = self._extract_performance_issues(audit_data)
        
        # Safely extract brand colors
        brand_colors = brand_identity.get('colors', [])
        if isinstance(brand_colors, list):
            # Filter out non-string items and ensure they're strings
            brand_colors = [str(color) for color in brand_colors if color]
        
        # Safely extract target audience data
        pain_points = target_audience.get('pain_points', [])
        if isinstance(pain_points, list):
            pain_points = [str(point) for point in pain_points if point]
        else:
            pain_points = ['Need reliable professional services']
        
        motivations = target_audience.get('motivations', [])
        if isinstance(motivations, list):
            motivations = [str(motivation) for motivation in motivations if motivation]
        else:
            motivations = ['Business growth and success']
        
        # Safely extract conversion elements
        primary_ctas = conversion_elements.get('primary_ctas', [])
        if isinstance(primary_ctas, list):
            primary_ctas = [str(cta) for cta in primary_ctas if cta]
        else:
            primary_ctas = ['Contact Us', 'Get Quote']
        
        trust_elements = conversion_elements.get('trust_elements', [])
        if isinstance(trust_elements, list):
            trust_elements = [str(element) for element in trust_elements if element]
        else:
            trust_elements = ['Testimonials', 'Certifications']
        
        # Safely extract value propositions
        benefits = value_propositions.get('benefits', [])
        if isinstance(benefits, list):
            benefits = [str(benefit) for benefit in benefits if benefit]
        else:
            benefits = ['Quality service', 'Professional results']
        
        # Safely extract content strategy
        key_messages = content_strategy.get('key_messages', [])
        if isinstance(key_messages, list):
            key_messages = [str(message) for message in key_messages if message]
        else:
            key_messages = ['Professional service', 'Quality results']
        
        content_themes = content_strategy.get('content_themes', [])
        if isinstance(content_themes, list):
            content_themes = [str(theme) for theme in content_themes if theme]
        else:
            content_themes = ['Professional expertise', 'Quality service']
        
        # Safely extract technical insights
        essential_features = technical_insights.get('essential_features', [])
        if isinstance(essential_features, list):
            essential_features = [str(feature) for feature in essential_features if feature]
        else:
            essential_features = ['Contact forms', 'Our Services', 'About page']
        
        performance_requirements = technical_insights.get('performance_requirements', [])
        if isinstance(performance_requirements, list):
            performance_requirements = [str(req) for req in performance_requirements if req]
        else:
            performance_requirements = ['Fast loading', 'Mobile responsive']
        
        seo_requirements = technical_insights.get('seo_requirements', [])
        if isinstance(seo_requirements, list):
            seo_requirements = [str(req) for req in seo_requirements if req]
        else:
            seo_requirements = ['Meta tags', 'Structured data']
        
        # Build the comprehensive prompt
        prompt = f"""# Website Redesign AI Prompt

## Website Analysis: {url}

### Brand Identity & Visual Style
**Brand Tone:** {brand_identity.get('tone', 'Professional and trustworthy')}
**Brand Personality:** {brand_identity.get('personality', 'Reliable and professional')}
**Visual Style:** {visual_style.get('design_style', 'Modern and professional')}
**Brand Colors:** {', '.join(brand_colors)}
**Typography:** {visual_style.get('typography', 'Professional sans-serif fonts')}

### Industry & Market Context
**Primary Industry:** {industry_analysis.get('primary_industry', 'Professional Services')}
**Market Position:** {industry_analysis.get('market_position', 'Professional service provider')}
**Target Market:** {industry_analysis.get('target_market', 'Businesses seeking professional services')}

### Target Audience
**Primary Audience:** {target_audience.get('primary_audience', 'Business owners and decision makers')}
**Demographics:** {target_audience.get('demographics', 'Adults 25-65, business professionals')}
**Pain Points:** {', '.join(pain_points)}
**Motivations:** {', '.join(motivations)}

### Website Goals & Conversion Strategy
**Primary Goal:** {website_goals.get('primary_goal', 'Lead generation')}
**Conversion Actions:** {', '.join(website_goals.get('conversion_actions', ['Contact form submission', 'Phone call']))}
**Primary CTAs:** {', '.join(primary_ctas)}
**Trust Elements:** {', '.join(trust_elements)}

### Value Propositions & Messaging
**Primary Value Proposition:** {value_propositions.get('primary_vp', 'Professional and reliable service')}
**Unique Selling Point:** {value_propositions.get('usp', 'Professional expertise and reliability')}
**Key Benefits:** {', '.join(benefits)}
**Key Messages:** {', '.join(key_messages)}

### Content Strategy
**Content Themes:** {', '.join(content_themes)}
**Tone of Voice:** {content_strategy.get('tone_of_voice', 'Professional and helpful')}
**Content Types:** {', '.join(content_strategy.get('content_types', ['Service pages', 'About page', 'Contact information']))}

### Technical Requirements
**Essential Features:** {', '.join(essential_features)}
**Performance Requirements:** {', '.join(performance_requirements)}
**SEO Requirements:** {', '.join(seo_requirements)}

### Performance Issues to Address
{self._format_performance_issues(performance_issues)}

## AI Page Builder Instructions

Create a modern, high-performing website that:

### Design & Visual Elements
- Use the specified brand colors: {', '.join(brand_colors)}
- Apply {visual_style.get('design_style', 'modern and professional')} design style
- Use {visual_style.get('typography', 'professional sans-serif fonts')}
- Implement {visual_style.get('layout_style', 'clean and organized')} layout
- Ensure brand consistency across all pages

### Target Audience Focus
- Design for {target_audience.get('primary_audience', 'business owners and decision makers')}
- Address pain points: {', '.join(pain_points)}
- Appeal to motivations: {', '.join(motivations)}

### Conversion Optimization
- Primary goal: {website_goals.get('primary_goal', 'Lead generation')}
- Main CTAs: {', '.join(primary_ctas)}
- Include trust elements: {', '.join(trust_elements)}
- Implement conversion funnel: {', '.join(website_goals.get('conversion_funnel', ['Landing page', 'Service pages', 'Contact form']))}

### Content Strategy
- Primary value proposition: {value_propositions.get('primary_vp', 'Professional and reliable service')}
- Key messages: {', '.join(key_messages)}
- Content themes: {', '.join(content_themes)}
- Tone: {content_strategy.get('tone_of_voice', 'Professional and helpful')}

### Technical Excellence
- Essential features: {', '.join(essential_features)}
- Performance: {', '.join(performance_requirements)}
- SEO: {', '.join(seo_requirements)}
- Accessibility: {', '.join(technical_insights.get('accessibility', ['Alt text', 'Keyboard navigation']))}

### Required Sections
1. **Hero Section** - Highlight {value_propositions.get('primary_vp', 'primary value proposition')}
2. **About Section** - Build trust and credibility
3. **Services/Products** - Detail offerings clearly
4. **Value Propositions** - Emphasize {', '.join(benefits)}
5. **Social Proof** - Include {', '.join(trust_elements)}
6. **Contact Section** - Clear {', '.join(website_goals.get('call_to_actions', ['call-to-actions']))}

### Success Criteria
The website should:
- Convert visitors into {website_goals.get('primary_goal', 'leads')} effectively
- Rank well in search engines for target keywords
- Provide exceptional user experience across all devices
- Load quickly and perform optimally
- Represent the brand professionally and build trust
- Address the specific needs of {target_audience.get('primary_audience', 'the target audience')}

Create a website that combines beautiful design with strategic functionality, optimized for both search engines and user conversions in the {industry_analysis.get('primary_industry', 'professional services')} industry."""

        return prompt
    
    def _analyze_current_website(self, audit_data: Dict[str, Any], 
                                content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current website state"""
        
        analysis = {
            'performance': {},
            'seo': {},
            'content': {},
            'technical': {},
            'issues': [],
            'strengths': []
        }
        
        # Performance analysis
        if audit_data:
            mobile_perf = audit_data.get('mobile', {}).get('performance_score', 0) * 100
            desktop_perf = audit_data.get('desktop', {}).get('performance_score', 0) * 100
            
            analysis['performance'] = {
                'mobile_score': mobile_perf,
                'desktop_score': desktop_perf,
                'avg_score': (mobile_perf + desktop_perf) / 2
            }
            
            if mobile_perf < 70:
                analysis['issues'].append(f"Poor mobile performance ({mobile_perf:.0f}/100)")
            if desktop_perf < 70:
                analysis['issues'].append(f"Poor desktop performance ({desktop_perf:.0f}/100)")
        
        # SEO analysis
        if content_data and 'analysis' in content_data:
            seo_elements = content_data['analysis'].get('seo_elements', {})
            if seo_elements:
                analysis['seo'] = {
                    'score': seo_elements.get('seo_score', 0),
                    'issues': seo_elements.get('issues', []),
                    'strengths': seo_elements.get('strengths', [])
                }
                analysis['issues'].extend(seo_elements.get('issues', []))
                analysis['strengths'].extend(seo_elements.get('strengths', []))
        
        # Content analysis
        if content_data and 'analysis' in content_data:
            content_analysis = content_data['analysis'].get('content_quality', {})
            if content_analysis:
                analysis['content'] = {
                    'overall_score': content_analysis.get('overall_quality_score', 0),
                    'avg_word_count': content_analysis.get('avg_word_count_per_page', 0),
                    'readability_score': content_analysis.get('avg_readability_score', 0)
                }
        
        # Technical analysis
        if content_data and 'analysis' in content_data:
            technical_analysis = content_data['analysis'].get('technical_seo', {})
            if technical_analysis:
                analysis['technical'] = {
                    'score': technical_analysis.get('technical_score', 0),
                    'https_analysis': technical_analysis.get('https_analysis', {}),
                    'structured_data': technical_analysis.get('structured_data_analysis', {})
                }
        
        return analysis
    
    def _create_comprehensive_prompt(self, url: str, current_analysis: Dict[str, Any],
                                   audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> str:
        """Create comprehensive AI prompt for page building"""
        
        # Extract key information
        website_info = self._extract_website_info(content_data)
        performance_issues = self._extract_performance_issues(audit_data)
        seo_issues = self._extract_seo_issues(content_data)
        content_insights = self._extract_content_insights(content_data)
        technical_requirements = self._extract_technical_requirements(audit_data, content_data)
        
        # Build the comprehensive prompt
        prompt = f"""# Website Redesign AI Prompt

## Current Website Analysis: {url}

### Website Overview
{self._format_website_overview(website_info)}

### Performance Analysis
{self._format_performance_analysis(performance_issues, current_analysis.get('performance', {}))}

### SEO Analysis
{self._format_seo_analysis(seo_issues, current_analysis.get('seo', {}))}

### Content Analysis
{self._format_content_analysis(content_insights, current_analysis.get('content', {}))}

### Technical Requirements
{self._format_technical_requirements(technical_requirements)}

### Key Issues to Address
{self._format_key_issues(current_analysis.get('issues', []))}

### Strengths to Maintain
{self._format_strengths(current_analysis.get('strengths', []))}

## AI Page Builder Instructions

Based on the above analysis, create a modern, high-performing website that addresses the identified issues while maintaining the website's core strengths. Focus on:

1. **Performance Optimization**: Implement fast loading times, optimize images, and use efficient code
2. **SEO Best Practices**: Ensure proper meta tags, heading structure, and semantic HTML
3. **Content Strategy**: Create engaging, well-structured content that serves user intent
4. **Technical Excellence**: Use modern web standards, responsive design, and accessibility features
5. **User Experience**: Design intuitive navigation and clear information architecture

The new website should be:
- Mobile-first and responsive
- Fast-loading (target 90+ PageSpeed scores)
- SEO-optimized with proper meta tags and structure
- Accessible and user-friendly
- Modern in design and functionality
- Content-rich with clear value propositions

Use the insights from the current website analysis to inform design decisions, content strategy, and technical implementation."""

        return prompt
    
    def _extract_website_info(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic website information"""
        info = {
            'pages_analyzed': 0,
            'total_word_count': 0,
            'page_types': [],
            'top_keywords': [],
            'content_themes': []
        }
        
        if content_data:
            info['pages_analyzed'] = content_data.get('pages_analyzed', 0)
            info['total_word_count'] = content_data.get('total_word_count', 0)
            info['page_types'] = content_data.get('page_types_found', [])
            
            # Extract content themes
            content_themes = content_data.get('content_themes', {})
            if content_themes:
                info['top_keywords'] = content_themes.get('top_keywords', [])
        
        return info
    
    def _extract_performance_issues(self, audit_data: Dict[str, Any]) -> List[str]:
        """Extract performance issues from audit data"""
        issues = []
        
        if not audit_data:
            return issues
        
        # Mobile performance
        mobile_data = audit_data.get('mobile', {})
        if mobile_data:
            mobile_score = mobile_data.get('performance_score', 0) * 100
            if mobile_score < 70:
                issues.append(f"Mobile performance score: {mobile_score:.0f}/100 (needs improvement)")
            
            # Core Web Vitals
            vitals = mobile_data.get('core_web_vitals', {})
            if vitals:
                lcp = vitals.get('largest_contentful_paint', {})
                if isinstance(lcp, dict):
                    lcp_value = lcp.get('value', 0)
                    if lcp_value > 2.5:
                        issues.append(f"Largest Contentful Paint: {lcp_value:.2f}s (should be <2.5s)")
                elif isinstance(lcp, (int, float)) and lcp > 2.5:
                    issues.append(f"Largest Contentful Paint: {lcp:.2f}s (should be <2.5s)")
                
                fid = vitals.get('first_input_delay', {})
                if isinstance(fid, dict):
                    fid_value = fid.get('value', 0)
                    if fid_value > 100:
                        issues.append(f"First Input Delay: {fid_value:.0f}ms (should be <100ms)")
                elif isinstance(fid, (int, float)) and fid > 100:
                    issues.append(f"First Input Delay: {fid:.0f}ms (should be <100ms)")
                
                cls = vitals.get('cumulative_layout_shift', {})
                if isinstance(cls, dict):
                    cls_value = cls.get('value', 0)
                    if cls_value > 0.1:
                        issues.append(f"Cumulative Layout Shift: {cls_value:.3f} (should be <0.1)")
                elif isinstance(cls, (int, float)) and cls > 0.1:
                    issues.append(f"Cumulative Layout Shift: {cls:.3f} (should be <0.1)")
        
        # Desktop performance
        desktop_data = audit_data.get('desktop', {})
        if desktop_data:
            desktop_score = desktop_data.get('performance_score', 0) * 100
            if desktop_score < 70:
                issues.append(f"Desktop performance score: {desktop_score:.0f}/100 (needs improvement)")
        
        return issues
    
    def _format_performance_issues(self, issues: List[str]) -> str:
        """Format performance issues for the prompt"""
        if not issues:
            return "No major performance issues identified."
        
        formatted_issues = []
        for issue in issues:
            formatted_issues.append(f"- {issue}")
        
        return "\n".join(formatted_issues)
    
    def _extract_seo_issues(self, content_data: Dict[str, Any]) -> List[str]:
        """Extract SEO issues from content analysis"""
        issues = []
        
        if not content_data or 'analysis' not in content_data:
            return issues
        
        analysis = content_data['analysis']
        seo_elements = analysis.get('seo_elements', {})
        
        if seo_elements:
            # Title analysis
            title_analysis = seo_elements.get('title_analysis', {})
            if title_analysis:
                missing_titles = title_analysis.get('missing_titles', 0)
                if missing_titles > 0:
                    issues.append(f"{missing_titles} pages missing title tags")
                
                long_titles = title_analysis.get('long_titles', 0)
                if long_titles > 0:
                    issues.append(f"{long_titles} pages have overly long titles")
            
            # Meta description analysis
            meta_analysis = seo_elements.get('meta_description_analysis', {})
            if meta_analysis:
                missing_descriptions = meta_analysis.get('missing_descriptions', 0)
                if missing_descriptions > 0:
                    issues.append(f"{missing_descriptions} pages missing meta descriptions")
            
            # Heading analysis
            heading_analysis = seo_elements.get('heading_analysis', {})
            if heading_analysis:
                h1_issues = heading_analysis.get('h1_issues', [])
                if h1_issues:
                    issues.append(f"Heading structure issues: {len(h1_issues)} problems found")
            
            # Image analysis
            image_analysis = seo_elements.get('image_analysis', {})
            if image_analysis:
                images_without_alt = image_analysis.get('images_without_alt', 0)
                if images_without_alt > 0:
                    issues.append(f"{images_without_alt} images missing alt text")
        
        return issues
    
    def _extract_content_insights(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content insights from analysis"""
        insights = {
            'quality_score': 0,
            'avg_word_count': 0,
            'readability_score': 0,
            'content_gaps': [],
            'keyword_opportunities': []
        }
        
        if not content_data or 'analysis' not in content_data:
            return insights
        
        analysis = content_data['analysis']
        
        # Content quality
        content_quality = analysis.get('content_quality', {})
        if content_quality:
            insights['quality_score'] = content_quality.get('overall_quality_score', 0)
            insights['avg_word_count'] = content_quality.get('avg_word_count_per_page', 0)
            insights['readability_score'] = content_quality.get('avg_readability_score', 0)
        
        # Content gaps
        content_gaps = analysis.get('content_gaps', {})
        if content_gaps:
            missing_pages = content_gaps.get('missing_pages', [])
            insights['content_gaps'] = [page['description'] for page in missing_pages[:3]]
        
        # Keyword analysis
        keyword_analysis = analysis.get('keyword_analysis', {})
        if keyword_analysis:
            opportunities = keyword_analysis.get('keyword_opportunities', [])
            insights['keyword_opportunities'] = opportunities[:5]
        
        return insights
    
    def _extract_technical_requirements(self, audit_data: Dict[str, Any], content_data: Dict[str, Any]) -> List[str]:
        """Extract technical requirements"""
        requirements = []
        
        # Performance requirements
        if audit_data:
            requirements.append("Implement fast loading times (target 90+ PageSpeed scores)")
            requirements.append("Optimize Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)")
            requirements.append("Use efficient image formats and compression")
        
        # SEO requirements
        if content_data:
            requirements.append("Implement proper meta tags and structured data")
            requirements.append("Use semantic HTML and proper heading hierarchy")
            requirements.append("Ensure all images have descriptive alt text")
        
        # General technical requirements
        requirements.extend([
            "Use responsive design (mobile-first approach)",
            "Implement HTTPS for security",
            "Ensure accessibility compliance (WCAG guidelines)",
            "Use modern web standards and best practices",
            "Optimize for search engines and user experience"
        ])
        
        return requirements
    
    def _format_website_overview(self, website_info: Dict[str, Any]) -> str:
        """Format website overview section"""
        return f"""- Pages analyzed: {website_info['pages_analyzed']}
- Total word count: {website_info['total_word_count']:,}
- Page types found: {', '.join(website_info['page_types']) if website_info['page_types'] else 'None identified'}
- Top keywords: {', '.join(website_info['top_keywords'][:5]) if website_info['top_keywords'] else 'None identified'}"""
    
    def _format_performance_analysis(self, issues: List[str], performance: Dict[str, Any]) -> str:
        """Format performance analysis section"""
        if not issues and not performance:
            return "No performance data available."
        
        result = []
        if performance:
            result.append(f"- Mobile performance: {performance.get('mobile_score', 0):.0f}/100")
            result.append(f"- Desktop performance: {performance.get('desktop_score', 0):.0f}/100")
            result.append(f"- Average performance: {performance.get('avg_score', 0):.0f}/100")
        
        if issues:
            result.append("\nPerformance Issues:")
            for issue in issues:
                result.append(f"- {issue}")
        
        return "\n".join(result)
    
    def _format_seo_analysis(self, issues: List[str], seo: Dict[str, Any]) -> str:
        """Format SEO analysis section"""
        if not issues and not seo:
            return "No SEO data available."
        
        result = []
        if seo:
            result.append(f"- SEO score: {seo.get('score', 0)}/100")
        
        if issues:
            result.append("\nSEO Issues:")
            for issue in issues:
                result.append(f"- {issue}")
        
        return "\n".join(result)
    
    def _format_content_analysis(self, insights: Dict[str, Any], content: Dict[str, Any]) -> str:
        """Format content analysis section"""
        result = []
        
        if content:
            result.append(f"- Content quality score: {content.get('overall_score', 0):.0f}/100")
            result.append(f"- Average words per page: {content.get('avg_word_count', 0):.0f}")
            result.append(f"- Readability score: {content.get('readability_score', 0):.0f}/100")
        
        if insights:
            if insights.get('content_gaps'):
                result.append(f"\nContent Gaps:")
                for gap in insights['content_gaps']:
                    result.append(f"- Missing: {gap}")
            
            if insights.get('keyword_opportunities'):
                result.append(f"\nKeyword Opportunities:")
                for opportunity in insights['keyword_opportunities'][:3]:
                    result.append(f"- {opportunity}")
        
        return "\n".join(result) if result else "No content analysis available."
    
    def _format_technical_requirements(self, requirements: List[str]) -> str:
        """Format technical requirements section"""
        if not requirements:
            return "No specific technical requirements identified."
        
        return "\n".join([f"- {req}" for req in requirements])
    
    def _format_key_issues(self, issues: List[str]) -> str:
        """Format key issues section"""
        if not issues:
            return "No major issues identified."
        
        return "\n".join([f"- {issue}" for issue in issues])
    
    def _format_strengths(self, strengths: List[str]) -> str:
        """Format strengths section"""
        if not strengths:
            return "No specific strengths identified."
        
        return "\n".join([f"- {strength}" for strength in strengths])
    
    def export_prompt(self, prompt: str, format_type: str = 'txt') -> bytes:
        """Export prompt in specified format"""
        if format_type == 'txt':
            return prompt.encode('utf-8')
        elif format_type == 'json':
            import json
            return json.dumps({'prompt': prompt, 'generated_at': datetime.now().isoformat()}, indent=2).encode('utf-8')
        else:
            raise ValueError(f"Unsupported export format: {format_type}") 