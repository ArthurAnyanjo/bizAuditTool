import json
import re
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import urlparse
import json
import g4f

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDataProcessor:
    """
    Enhanced data processor with G4F integration for comprehensive website analysis
    """
    
    def __init__(self):
        """Initialize enhanced data processor"""
        
    
    def analyze_website_comprehensive(self, url: str, html_content: str, 
                                   scraping_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive website analysis using G4F AI
        
        Args:
            url: Website URL
            html_content: Raw HTML content
            scraping_results: Results from web scraping
            
        Returns:
            Comprehensive analysis including brand, audience, goals, etc.
        """
        try:
            logger.info(f"Starting comprehensive analysis for {url}")
            
            # Basic analysis from scraping results
            basic_analysis = self._analyze_basic_content(scraping_results)
            
            # AI-powered analysis using G4F
            ai_analysis = self._analyze_with_ai(url, html_content, scraping_results)
            
            # Combine analyses
            comprehensive_analysis = {
                'basic_analysis': basic_analysis,
                'ai_analysis': ai_analysis,
                'combined_insights': self._combine_insights(basic_analysis, ai_analysis),
                'recommendations': self._generate_comprehensive_recommendations(basic_analysis, ai_analysis)
            }
            
            logger.info("Comprehensive analysis completed successfully")
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            raise Exception(f"Comprehensive analysis failed: {str(e)}")
    
    def _analyze_basic_content(self, scraping_results: Dict[str, Any]) -> Dict[str, Any]:
        """Basic content analysis from scraping results"""
        pages_data = scraping_results.get('pages', [])
        
        # Extract basic information
        basic_info = {
            'total_pages': len(pages_data),
            'page_types': list(set(page.get('page_type', 'unknown') for page in pages_data)),
            'total_word_count': sum(page.get('word_count', 0) for page in pages_data),
            'images_count': scraping_results.get('image_count', 0),
            'internal_links': scraping_results.get('internal_links_count', 0),
            'meta_tags': scraping_results.get('meta_tags', {}),
            'structured_data': scraping_results.get('structured_data', [])
        }
        
        # Extract content themes
        all_content = ' '.join(page.get('content', {}).get('text', '') for page in pages_data)
        content_themes = self._identify_content_themes(all_content)
        
        return {
            'basic_info': basic_info,
            'content_themes': content_themes,
            'page_analysis': self._analyze_pages(pages_data)
        }
    
    def _analyze_with_ai(self, url: str, html_content: str, 
                         scraping_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website using G4F AI"""
        
        try:
            # Prepare content for AI analysis
            analysis_content = self._prepare_content_for_ai(url, html_content, scraping_results)
            
            # AI analysis prompts with individual error handling
            ai_analysis = {}
            
            # Brand identity analysis
            try:
                ai_analysis['brand_identity'] = self._analyze_brand_identity(analysis_content)
            except Exception as e:
                logger.error(f"Brand identity analysis failed: {str(e)}")
                ai_analysis['brand_identity'] = self._get_default_brand_identity()
            
            # Industry analysis
            try:
                ai_analysis['industry_analysis'] = self._analyze_industry(analysis_content)
            except Exception as e:
                logger.error(f"Industry analysis failed: {str(e)}")
                ai_analysis['industry_analysis'] = self._get_default_industry()
            
            # Target audience analysis
            try:
                ai_analysis['target_audience'] = self._analyze_target_audience(analysis_content)
            except Exception as e:
                logger.error(f"Target audience analysis failed: {str(e)}")
                ai_analysis['target_audience'] = self._get_default_target_audience()
            
            # Website goals analysis
            try:
                ai_analysis['website_goals'] = self._analyze_website_goals(analysis_content)
            except Exception as e:
                logger.error(f"Website goals analysis failed: {str(e)}")
                ai_analysis['website_goals'] = self._get_default_website_goals()
            
            # Value propositions analysis
            try:
                ai_analysis['value_propositions'] = self._analyze_value_propositions(analysis_content)
            except Exception as e:
                logger.error(f"Value propositions analysis failed: {str(e)}")
                ai_analysis['value_propositions'] = self._get_default_value_propositions()
            
            # Visual style analysis
            try:
                ai_analysis['visual_style'] = self._analyze_visual_style(analysis_content)
            except Exception as e:
                logger.error(f"Visual style analysis failed: {str(e)}")
                ai_analysis['visual_style'] = self._get_default_visual_style()
            
            # Content strategy analysis
            try:
                ai_analysis['content_strategy'] = self._analyze_content_strategy(analysis_content)
            except Exception as e:
                logger.error(f"Content strategy analysis failed: {str(e)}")
                ai_analysis['content_strategy'] = self._get_default_content_strategy()
            
            # Conversion elements analysis
            try:
                ai_analysis['conversion_elements'] = self._analyze_conversion_elements(analysis_content)
            except Exception as e:
                logger.error(f"Conversion elements analysis failed: {str(e)}")
                ai_analysis['conversion_elements'] = self._get_default_conversion_elements()
            
            # Technical insights analysis
            try:
                ai_analysis['technical_insights'] = self._analyze_technical_insights(analysis_content)
            except Exception as e:
                logger.error(f"Technical insights analysis failed: {str(e)}")
                ai_analysis['technical_insights'] = self._get_default_technical_insights()
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return self._get_fallback_analysis()
    
    def _prepare_content_for_ai(self, url: str, html_content: str, 
                               scraping_results: Dict[str, Any]) -> str:
        """Prepare content for AI analysis"""
        pages_data = scraping_results.get('pages', [])
        
        # Extract key content
        content_parts = []
        
        # Add URL and basic info
        content_parts.append(f"Website URL: {url}")
        
        # Add page content
        for page in pages_data:
            page_type = page.get('page_type', 'unknown')
            title = page.get('title', '')
            meta_desc = page.get('meta_description', '')
            content = page.get('content', {}).get('text', '')
            headings = page.get('headings', {})
            
            content_parts.append(f"\n--- {page_type.upper()} PAGE ---")
            content_parts.append(f"Title: {title}")
            content_parts.append(f"Meta Description: {meta_desc}")
            content_parts.append(f"Headings: {json.dumps(headings, indent=2)}")
            content_parts.append(f"Content: {content[:2000]}...")  # Limit content length
        
        # Add meta tags
        meta_tags = scraping_results.get('meta_tags', {})
        if meta_tags:
            content_parts.append(f"\n--- META TAGS ---")
            content_parts.append(json.dumps(meta_tags, indent=2))
        
        return "\n".join(content_parts)
    
    def _analyze_brand_identity(self, content: str) -> Dict[str, Any]:
        """Analyze brand identity using AI"""
        prompt = f"""
Analyze the following website content and provide detailed brand identity insights.

Website Content:
{content}

Please analyze and provide the following information in EXACT JSON format (no additional text, just JSON):

{{
  "colors": ["#color1", "#color2"],
  "tone": "professional/friendly/luxury/etc",
  "personality": "reliable/professional/innovative/etc",
  "values": ["value1", "value2", "value3"],
  "positioning": "how the brand positions itself",
  "visual_style": "clean/modern/classic/etc",
  "messaging": "key brand messages and themes"
}}

Focus on identifying:
1. Brand Colors: Primary and secondary brand colors
2. Brand Tone: Professional, friendly, luxury, etc.
3. Brand Personality: Reliable, professional, innovative, etc.
4. Brand Values: Core values the brand represents
5. Brand Positioning: How the brand positions itself in the market
6. Visual Style: Overall visual aesthetic and style
7. Brand Messaging: Key brand messages and themes

Return ONLY valid JSON with the exact structure shown above.
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'brand_identity')
        except Exception as e:
            logger.error(f"Brand identity analysis failed: {str(e)}")
            return self._get_default_brand_identity()
    
    def _analyze_industry(self, content: str) -> Dict[str, Any]:
        """Analyze industry and market positioning"""
        prompt = f"""
Analyze the following website content to determine the industry and market context.

Website Content:
{content}

Please provide the following information in EXACT JSON format (no additional text, just JSON):

{{
  "primary_industry": "main industry name",
  "sub_industry": "specific niche or sub-industry",
  "market_position": "how business positions itself",
  "competitors": "type of competitors",
  "trends": "relevant industry trends",
  "target_market": "market segment served",
  "challenges": "common industry challenges"
}}

Focus on identifying:
1. Primary Industry: Main industry this business operates in
2. Sub-industry: Specific niche or sub-industry
3. Market Position: How this business positions itself in the market
4. Competitors: Type of competitors this business might have
5. Industry Trends: Relevant trends in this industry
6. Target Market: Market segment this business serves
7. Industry Challenges: Common challenges in this industry

Return ONLY valid JSON with the exact structure shown above.
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'industry')
        except Exception as e:
            logger.error(f"Industry analysis failed: {str(e)}")
            return self._get_default_industry()
    
    def _analyze_target_audience(self, content: str) -> Dict[str, Any]:
        """Analyze target audience and demographics"""
        prompt = f"""
Analyze the following website content to identify the target audience:

{content}

Please provide:
1. Primary Audience: Who is the main target audience?
2. Demographics: Age range, gender, income level, education
3. Psychographics: Values, interests, lifestyle, personality traits
4. Pain Points: What problems does this audience face?
5. Motivations: What motivates this audience to take action?
6. Decision Makers: Who makes the purchasing decisions?
7. User Personas: Create 2-3 detailed user personas

Provide your analysis in JSON format with these keys: primary_audience, demographics, psychographics, pain_points, motivations, decision_makers, user_personas
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'target_audience')
        except Exception as e:
            logger.error(f"Target audience analysis failed: {str(e)}")
            return self._get_default_target_audience()
    
    def _analyze_website_goals(self, content: str) -> Dict[str, Any]:
        """Analyze website goals and conversion objectives"""
        prompt = f"""
Analyze the following website content to identify the website's primary goals:

{content}

Please provide:
1. Primary Goal: What is the main conversion goal (lead generation, sales, awareness, etc.)?
2. Secondary Goals: What are secondary objectives?
3. Conversion Actions: What specific actions should visitors take?
4. Success Metrics: How would success be measured?
5. User Journey: What is the ideal user journey?
6. Call-to-Actions: What types of CTAs would be most effective?
7. Conversion Funnel: Describe the conversion funnel stages

Provide your analysis in JSON format with these keys: primary_goal, secondary_goals, conversion_actions, success_metrics, user_journey, call_to_actions, conversion_funnel
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'website_goals')
        except Exception as e:
            logger.error(f"Website goals analysis failed: {str(e)}")
            return self._get_default_website_goals()
    
    def _analyze_value_propositions(self, content: str) -> Dict[str, Any]:
        """Analyze value propositions and unique selling points"""
        prompt = f"""
Analyze the following website content to identify value propositions:

{content}

Please provide:
1. Primary Value Proposition: What is the main value proposition?
2. Secondary Value Props: What are additional value propositions?
3. Unique Selling Points: What makes this business unique?
4. Benefits: What benefits do customers receive?
5. Competitive Advantages: What advantages over competitors?
6. Trust Signals: What builds trust and credibility?
7. Proof Points: What evidence supports the value propositions?

Provide your analysis in JSON format with these keys: primary_vp, secondary_vps, usp, benefits, competitive_advantages, trust_signals, proof_points
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'value_propositions')
        except Exception as e:
            logger.error(f"Value propositions analysis failed: {str(e)}")
            return self._get_default_value_propositions()
    
    def _analyze_visual_style(self, content: str) -> Dict[str, Any]:
        """Analyze visual style and design preferences"""
        prompt = f"""
Analyze the following website content to determine visual style preferences.

Website Content:
{content}

Please provide the following information in EXACT JSON format (no additional text, just JSON):

{{
  "color_palette": ["#color1", "#color2", "#color3"],
  "typography": "font style description",
  "layout_style": "layout approach description",
  "visual_elements": "types of images and graphics",
  "design_style": "modern/classic/minimalist/bold/etc",
  "brand_consistency": "how to maintain visual consistency",
  "visual_hierarchy": "how to organize visual elements"
}}

Focus on identifying:
1. Color Palette: What colors would work best for this brand
2. Typography: What font styles would be appropriate
3. Layout Style: What layout approach would work best
4. Visual Elements: What types of images and graphics
5. Design Style: Modern, classic, minimalist, bold, etc.
6. Brand Consistency: How to maintain visual consistency
7. Visual Hierarchy: How to organize visual elements

Return ONLY valid JSON with the exact structure shown above.
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'visual_style')
        except Exception as e:
            logger.error(f"Visual style analysis failed: {str(e)}")
            return self._get_default_visual_style()
    
    def _analyze_content_strategy(self, content: str) -> Dict[str, Any]:
        """Analyze content strategy and messaging"""
        prompt = f"""
Analyze the following website content to develop a content strategy.

Website Content:
{content}

Please provide the following information in EXACT JSON format (no additional text, just JSON):

{{
  "key_messages": ["message1", "message2", "message3"],
  "content_themes": ["theme1", "theme2", "theme3"],
  "content_types": ["type1", "type2", "type3"],
  "tone_of_voice": "how the content should sound",
  "content_structure": "how content should be organized",
  "call_to_actions": ["cta1", "cta2", "cta3"],
  "content_gaps": ["gap1", "gap2", "gap3"]
}}

Focus on identifying:
1. Key Messages: Main messages to communicate
2. Content Themes: Themes the content should focus on
3. Content Types: Types of content that would be most effective
4. Tone of Voice: How the content should sound
5. Content Structure: How content should be organized
6. Call-to-Actions: CTAs that would be most effective
7. Content Gaps: Content that is missing or needs improvement

Return ONLY valid JSON with the exact structure shown above.
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'content_strategy')
        except Exception as e:
            logger.error(f"Content strategy analysis failed: {str(e)}")
            return self._get_default_content_strategy()
    
    def _analyze_conversion_elements(self, content: str) -> Dict[str, Any]:
        """Analyze conversion optimization elements"""
        prompt = f"""
Analyze the following website content to identify conversion optimization opportunities:

{content}

Please provide:
1. Primary CTAs: What should be the main call-to-action buttons?
2. Secondary CTAs: What additional CTAs would be helpful?
3. Trust Elements: What trust signals should be included?
4. Social Proof: What social proof elements would work?
5. Urgency Elements: What urgency or scarcity elements?
6. Lead Magnets: What lead magnets would be effective?
7. Conversion Funnel: How to optimize the conversion funnel?

Provide your analysis in JSON format with these keys: primary_ctas, secondary_ctas, trust_elements, social_proof, urgency_elements, lead_magnets, conversion_funnel
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'conversion_elements')
        except Exception as e:
            logger.error(f"Conversion elements analysis failed: {str(e)}")
            return self._get_default_conversion_elements()
    
    def _analyze_technical_insights(self, content: str) -> Dict[str, Any]:
        """Analyze technical requirements and insights"""
        prompt = f"""
Analyze the following website content to identify technical requirements:

{content}

Please provide:
1. Essential Features: What features are essential for this website?
2. Integration Needs: What integrations might be needed?
3. Performance Requirements: What performance standards are needed?
4. SEO Requirements: What SEO elements are important?
5. Accessibility: What accessibility features are needed?
6. Mobile Requirements: What mobile-specific features?
7. Security Needs: What security measures are important?

Provide your analysis in JSON format with these keys: essential_features, integration_needs, performance_requirements, seo_requirements, accessibility, mobile_requirements, security_needs
"""
        
        try:
            response = self._get_ai_response(prompt)
            return self._parse_ai_response(response, 'technical_insights')
        except Exception as e:
            logger.error(f"Technical insights analysis failed: {str(e)}")
            return self._get_default_technical_insights()
    
    def _get_ai_response(self, prompt: str) -> str:
        """Get response from G4F AI"""
        
        try:
            # Use G4F to get AI response
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4_1,
                messages=[{"role": "user", "content": prompt}],
            )
            
            if response and isinstance(response, str):
                return response.strip()
            else:
                logger.warning("Empty or invalid AI response received")
                return None
                
        except Exception as e:
            logger.error(f"G4F API call failed: {str(e)}")
            return None
    
    def _parse_ai_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        if not response:
            logger.warning(f"No AI response received for {analysis_type}")
            return self._get_default_analysis(analysis_type)
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                # Clean up common JSON issues
                json_str = json_str.replace('\n', ' ').replace('\r', ' ')
                json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
                json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
                
                # Additional cleaning for specific issues
                json_str = re.sub(r'//.*?(?=\n|$)', '', json_str)  # Remove comments
                json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)  # Remove block comments
                json_str = re.sub(r'"[^"]*":\s*\[[^\]]*$', '', json_str)  # Remove incomplete arrays
                json_str = re.sub(r'"[^"]*":\s*\{[^}]*$', '', json_str)  # Remove incomplete objects
                
                # Fix missing quotes in array values
                json_str = re.sub(r'\[([^"]*?),\s*([^",\]]+?)(?=,|\])', r'[\1, "\2"', json_str)
                json_str = re.sub(r'\[([^"]*?),\s*([^",\]]+?)(?=,|\])', r'[\1, "\2"', json_str)  # Run twice to catch multiple instances
                
                # Try to fix common JSON syntax errors
                json_str = re.sub(r'(["\w])\s*:\s*(["\w])', r'\1: \2', json_str)  # Fix missing quotes
                
                return json.loads(json_str)
            else:
                # If no JSON found, create structured response
                return self._structure_text_response(response, analysis_type)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {analysis_type}: {str(e)}")
            logger.debug(f"Raw response: {response}")
        except Exception as e:
            logger.error(f"Failed to parse AI response for {analysis_type}: {str(e)}")
            return self._get_default_analysis(analysis_type)
    
    def _extract_partial_json(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Extract partial data from malformed JSON"""
        try:
            # Try to extract key-value pairs from the response
            structured_data = {}
            
            # Look for patterns like "key": "value" or "key": ["value1", "value2"]
            patterns = [
                r'"([^"]+)":\s*"([^"]*)"',  # "key": "value"
                r'"([^"]+)":\s*\[([^\]]*)\]',  # "key": ["value1", "value2"]
                r'"([^"]+)":\s*(\d+)',  # "key": 123
                r'"([^"]+)":\s*([^,}\]]+)',  # "key": value
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response)
                for key, value in matches:
                    key = key.strip()
                    value = value.strip()
                    if key and value:
                        # Clean up the value
                        value = value.strip('"').strip()
                        if value.startswith('[') and value.endswith(']'):
                            # Handle array values
                            try:
                                array_content = value[1:-1]
                                if array_content:
                                    # Split by comma and clean each item
                                    array_items = array_content.split(',')
                                    cleaned_items = []
                                    for item in array_items:
                                        item = item.strip().strip('"').strip("'")
                                        if item:  # Only add non-empty items
                                            cleaned_items.append(item)
                                    structured_data[key] = cleaned_items
                                else:
                                    structured_data[key] = []
                            except:
                                structured_data[key] = value
                        else:
                            structured_data[key] = value
            
            if structured_data:
                logger.info(f"Extracted partial data for {analysis_type}: {len(structured_data)} items")
                return structured_data
            else:
                return self._get_default_analysis(analysis_type)
        except Exception as e:
            logger.error(f"Failed to extract partial JSON for {analysis_type}: {str(e)}")
            return self._get_default_analysis(analysis_type)
    
    def _structure_text_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Structure text response into organized data"""
        if not response:
            return self._get_default_analysis(analysis_type)
        
        # This is a fallback method to structure text responses
        lines = response.split('\n')
        structured_data = {}
        
        # Try to extract key-value pairs from the response
        for line in lines:
            line = line.strip()
            if ':' in line and len(line) > 3:
                try:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_').replace('-', '_')
                    value = value.strip()
                    if value and len(key) > 2:
                        structured_data[key] = value
                except:
                    continue
        
        # If we couldn't extract much, use default values
        if len(structured_data) < 2:
            logger.warning(f"Could not extract meaningful data from AI response for {analysis_type}")
            return self._get_default_analysis(analysis_type)
        
        return structured_data
    
    def _combine_insights(self, basic_analysis: Dict[str, Any], 
                         ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Combine basic and AI analysis insights"""
        return {
            'website_overview': {
                'url': basic_analysis.get('basic_info', {}).get('url', ''),
                'total_pages': basic_analysis.get('basic_info', {}).get('total_pages', 0),
                'industry': ai_analysis.get('industry_analysis', {}).get('primary_industry', 'Unknown'),
                'primary_goal': ai_analysis.get('website_goals', {}).get('primary_goal', 'Unknown'),
                'target_audience': ai_analysis.get('target_audience', {}).get('primary_audience', 'Unknown')
            },
            'brand_identity': ai_analysis.get('brand_identity', {}),
            'content_strategy': ai_analysis.get('content_strategy', {}),
            'conversion_strategy': ai_analysis.get('conversion_elements', {}),
            'technical_requirements': ai_analysis.get('technical_insights', {}),
            'value_propositions': ai_analysis.get('value_propositions', {}),
            'visual_design': ai_analysis.get('visual_style', {})
        }
    
    def _generate_comprehensive_recommendations(self, basic_analysis: Dict[str, Any], 
                                             ai_analysis: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Add recommendations based on analysis
        if ai_analysis.get('brand_identity'):
            recommendations.append("Implement consistent brand identity across all pages")
        
        if ai_analysis.get('website_goals', {}).get('primary_goal'):
            goal = ai_analysis['website_goals']['primary_goal']
            recommendations.append(f"Optimize website for primary goal: {goal}")
        
        if ai_analysis.get('target_audience'):
            recommendations.append("Create content tailored to identified target audience")
        
        if ai_analysis.get('value_propositions'):
            recommendations.append("Prominently display value propositions on homepage")
        
        if ai_analysis.get('conversion_elements'):
            recommendations.append("Implement strategic call-to-action buttons")
        
        return recommendations
    
    # Fallback methods for when AI analysis fails
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Get fallback analysis when AI is not available"""
        return {
            'brand_identity': self._get_default_brand_identity(),
            'industry_analysis': self._get_default_industry(),
            'target_audience': self._get_default_target_audience(),
            'website_goals': self._get_default_website_goals(),
            'value_propositions': self._get_default_value_propositions(),
            'visual_style': self._get_default_visual_style(),
            'content_strategy': self._get_default_content_strategy(),
            'conversion_elements': self._get_default_conversion_elements(),
            'technical_insights': self._get_default_technical_insights()
        }
    
    def _get_default_brand_identity(self) -> Dict[str, Any]:
        return {
            'colors': ['#667eea', '#764ba2'],
            'tone': 'Professional and trustworthy',
            'personality': 'Reliable and professional',
            'values': ['Quality', 'Trust', 'Professionalism'],
            'positioning': 'Professional service provider',
            'visual_style': 'Clean and modern',
            'messaging': 'Professional and solution-focused'
        }
    
    def _get_default_industry(self) -> Dict[str, Any]:
        return {
            'primary_industry': 'Professional Services',
            'sub_industry': 'Consulting',
            'market_position': 'Professional service provider',
            'competitors': 'Other service providers in the industry',
            'trends': 'Digital transformation and online presence',
            'target_market': 'Businesses seeking professional services',
            'challenges': 'Standing out in a competitive market'
        }
    
    def _get_default_target_audience(self) -> Dict[str, Any]:
        return {
            'primary_audience': 'Business owners and decision makers',
            'demographics': 'Adults 25-65, business professionals',
            'psychographics': 'Value quality and professionalism',
            'pain_points': 'Need reliable professional services',
            'motivations': 'Business growth and success',
            'decision_makers': 'Business owners and managers',
            'user_personas': ['Business Owner Sarah', 'Manager Mike']
        }
    
    def _get_default_website_goals(self) -> Dict[str, Any]:
        return {
            'primary_goal': 'Lead generation',
            'secondary_goals': ['Brand awareness', 'Information sharing'],
            'conversion_actions': ['Contact form submission', 'Phone call'],
            'success_metrics': ['Lead generation rate', 'Contact form submissions'],
            'user_journey': 'Awareness → Interest → Consideration → Contact',
            'call_to_actions': ['Contact Us', 'Get Quote', 'Learn More'],
            'conversion_funnel': ['Landing page', 'Service pages', 'Contact page']
        }
    
    def _get_default_value_propositions(self) -> Dict[str, Any]:
        return {
            'primary_vp': 'Professional and reliable service',
            'secondary_vps': ['Quality work', 'Customer satisfaction'],
            'usp': 'Professional expertise and reliability',
            'benefits': ['Quality service', 'Professional results'],
            'competitive_advantages': ['Experience', 'Professionalism'],
            'trust_signals': ['Testimonials', 'Certifications'],
            'proof_points': ['Customer testimonials', 'Case studies']
        }
    
    def _get_default_visual_style(self) -> Dict[str, Any]:
        return {
            'color_palette': ['#667eea', '#764ba2', '#ffffff', '#f8f9fa'],
            'typography': 'Professional sans-serif fonts',
            'layout_style': 'Clean and organized',
            'visual_elements': 'Professional images and icons',
            'design_style': 'Modern and professional',
            'brand_consistency': 'Consistent color scheme and typography',
            'visual_hierarchy': 'Clear information hierarchy'
        }
    
    def _get_default_content_strategy(self) -> Dict[str, Any]:
        return {
            'key_messages': ['Professional service', 'Quality results'],
            'content_themes': ['Professional expertise', 'Quality service'],
            'content_types': ['Service pages', 'About page', 'Contact information'],
            'tone_of_voice': 'Professional and helpful',
            'content_structure': 'Clear sections with headings',
            'call_to_actions': ['Contact Us', 'Learn More'],
            'content_gaps': ['More detailed service information', 'Case studies']
        }
    
    def _get_default_conversion_elements(self) -> Dict[str, Any]:
        return {
            'primary_ctas': ['Contact Us', 'Get Quote'],
            'secondary_ctas': ['Learn More', 'Download Brochure'],
            'trust_elements': ['Testimonials', 'Certifications'],
            'social_proof': ['Customer reviews', 'Success stories'],
            'urgency_elements': ['Limited availability', 'Special offers'],
            'lead_magnets': ['Free consultation', 'Service guide'],
            'conversion_funnel': ['Landing page', 'Service pages', 'Contact form']
        }
    
    def _get_default_technical_insights(self) -> Dict[str, Any]:
        return {
            'essential_features': ['Contact forms', 'Service pages', 'About page'],
            'integration_needs': ['Email marketing', 'Analytics'],
            'performance_requirements': ['Fast loading', 'Mobile responsive'],
            'seo_requirements': ['Meta tags', 'Structured data'],
            'accessibility': ['Alt text', 'Keyboard navigation'],
            'mobile_requirements': ['Responsive design', 'Touch-friendly'],
            'security_needs': ['HTTPS', 'Form security']
        }
    
    def _get_default_analysis(self, analysis_type: str) -> Dict[str, Any]:
        """Get default analysis for any type"""
        defaults = {
            'brand_identity': self._get_default_brand_identity(),
            'industry': self._get_default_industry(),
            'target_audience': self._get_default_target_audience(),
            'website_goals': self._get_default_website_goals(),
            'value_propositions': self._get_default_value_propositions(),
            'visual_style': self._get_default_visual_style(),
            'content_strategy': self._get_default_content_strategy(),
            'conversion_elements': self._get_default_conversion_elements(),
            'technical_insights': self._get_default_technical_insights()
        }
        return defaults.get(analysis_type, {})
    
    def _identify_content_themes(self, content: str) -> Dict[str, List[str]]:
        """Identify content themes from text"""
        themes = {
            'services': ['service', 'services', 'consulting', 'solution'],
            'business': ['business', 'professional', 'company', 'enterprise'],
            'quality': ['quality', 'expertise', 'professional', 'reliable'],
            'contact': ['contact', 'phone', 'email', 'address'],
            'about': ['about', 'team', 'experience', 'history']
        }
        
        identified_themes = {}
        content_lower = content.lower()
        
        for theme, keywords in themes.items():
            found_keywords = [kw for kw in keywords if kw in content_lower]
            if found_keywords:
                identified_themes[theme] = found_keywords
        
        return identified_themes
    
    def _analyze_pages(self, pages_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze individual pages"""
        page_analysis = {}
        
        for page in pages_data:
            page_type = page.get('page_type', 'unknown')
            word_count = page.get('word_count', 0)
            title = page.get('title', '')
            
            if page_type not in page_analysis:
                page_analysis[page_type] = {
                    'count': 0,
                    'total_words': 0,
                    'titles': []
                }
            
            page_analysis[page_type]['count'] += 1
            page_analysis[page_type]['total_words'] += word_count
            if title:
                page_analysis[page_type]['titles'].append(title)
        
        return page_analysis 