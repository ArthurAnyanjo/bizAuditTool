import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime

# Import custom modules
from modules.pagespeed_api import PageSpeedAnalyzer
from modules.web_scraper import WebScraper
from modules.report_generator import ReportGenerator
from modules.prompt_generator import PromptGenerator
from modules.enhanced_data_processor import EnhancedDataProcessor

# Page configuration
st.set_page_config(
    page_title="Website Audit & AI Prompt Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .score-excellent { border-left-color: #22c55e !important; }
    .score-good { border-left-color: #eab308 !important; }
    .score-poor { border-left-color: #ef4444 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; padding-left: 20px; padding-right: 20px; }
    .prompt-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        max-height: 600px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

class WebsiteAuditApp:
    def __init__(self):
        self.pagespeed_analyzer = PageSpeedAnalyzer()
        self.web_scraper = WebScraper()
        self.report_generator = ReportGenerator()
        self.prompt_generator = PromptGenerator()
        self.data_processor = EnhancedDataProcessor()
        
    def run(self):
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Website Audit & AI Prompt Generator</h1>
            <p>Analyze websites and generate comprehensive AI prompts for page builders</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        if st.session_state.current_page == 'audit':
            self.render_audit_page()
        elif st.session_state.current_page == 'analysis':
            self.render_analysis_page()
        elif st.session_state.current_page == 'prompt':
            self.render_prompt_page()
    
    def render_sidebar(self):
        st.sidebar.title("Navigation")
        
        # Initialize session state if not exists
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'audit'
        
        # Page selection
        page_mapping = {'audit': 'Performance Audit', 'analysis': 'Content Analysis', 'prompt': 'AI Prompt Generator'}
        current_page_display = page_mapping.get(st.session_state.current_page, 'Performance Audit')
        
        page = st.sidebar.selectbox(
            "Choose a section:",
            ['Performance Audit', 'Content Analysis', 'AI Prompt Generator'],
            index=['Performance Audit', 'Content Analysis', 'AI Prompt Generator'].index(current_page_display)
        )
        
        page_mapping = {
            'Performance Audit': 'audit',
            'Content Analysis': 'analysis', 
            'AI Prompt Generator': 'prompt'
        }
        st.session_state.current_page = page_mapping[page]
        
        # Store results in session state
        if 'audit_results' not in st.session_state:
            st.session_state.audit_results = None
        if 'content_results' not in st.session_state:
            st.session_state.content_results = None
        if 'generated_prompt' not in st.session_state:
            st.session_state.generated_prompt = None
    
    def render_audit_page(self):
        """Render the performance audit page"""
        st.header("📊 Performance Audit")
        st.write("Analyze website performance using Google PageSpeed Insights")
        
        # URL input
        url = st.text_input("Enter website URL:", placeholder="https://example.com")
        
        if st.button("Run Performance Audit", type="primary"):
            if url:
                with st.spinner("Running performance audit..."):
                    self.run_performance_audit(url)
            else:
                st.error("Please enter a valid URL")
        
        # Display results
        if st.session_state.audit_results:
            self.display_audit_results()
    
    def run_performance_audit(self, url: str):
        """Run performance audit for the given URL"""
        try:
            # Run PageSpeed analysis
            audit_results = self.pagespeed_analyzer.analyze_url(url)
            
            if audit_results and (audit_results.get('mobile') or audit_results.get('desktop')):
                st.session_state.audit_results = audit_results
                st.success("Performance audit completed successfully!")
            else:
                st.error("No performance data received. Please check the URL and try again.")
                
        except Exception as e:
            st.error(f"Error running performance audit: {str(e)}")
            st.info("Please ensure the URL is accessible and try again.")
    
    def display_audit_results(self):
        """Display performance audit results"""
        results = st.session_state.audit_results
        
        if not results:
            st.warning("No audit results available. Please run a performance audit first.")
            return
        
        # Overall scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mobile_score = results.get('mobile', {}).get('performance_score', 0) * 100
            self.render_score_card("Mobile Performance", mobile_score, "📱")
        
        with col2:
            desktop_score = results.get('desktop', {}).get('performance_score', 0) * 100
            self.render_score_card("Desktop Performance", desktop_score, "💻")
        
        with col3:
            avg_score = (mobile_score + desktop_score) / 2
            self.render_score_card("Average Performance", avg_score, "📊")
        
        # Detailed metrics
        st.subheader("Detailed Performance Metrics")
        
        tab1, tab2, tab3 = st.tabs(["Mobile Metrics", "Desktop Metrics", "Comparison"])
        
        with tab1:
            if 'mobile' in results:
                self.render_device_metrics("Mobile", results['mobile'])
            else:
                st.warning("No mobile data available")
        
        with tab2:
            if 'desktop' in results:
                self.render_device_metrics("Desktop", results['desktop'])
            else:
                st.warning("No desktop data available")
        
        with tab3:
            self.render_device_comparison(results)
    
    def render_device_metrics(self, device, data):
        """Render metrics for a specific device"""
        if not data:
            st.warning(f"No {device.lower()} data available")
            return
        
        # Core Web Vitals
        vitals = data.get('core_web_vitals', {})
        if vitals:
            st.subheader("Core Web Vitals")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                lcp = vitals.get('largest_contentful_paint', {})
                if isinstance(lcp, dict):
                    lcpValue = lcp.get('display_value', 'N/A')
                else:
                    lcpValue = str(lcp) if lcp else 'N/A'
                st.metric("Largest Contentful Paint", f"{lcpValue}")
            
            with col2:
                fid = vitals.get('first_input_delay', {})
                if isinstance(fid, dict):
                    fidValue = fid.get('display_value', 'N/A')
                else:
                    fidValue = str(fid) if fid else 'N/A'
                st.metric("First Input Delay", f"{fidValue}")
            
            with col3:
                cls = vitals.get('cumulative_layout_shift', {})
                if isinstance(cls, dict):
                    clsValue = cls.get('display_value', 'N/A')
                else:
                    clsValue = str(cls) if cls else 'N/A'
                st.metric("Cumulative Layout Shift", f"{clsValue}")
        
        # Performance metrics
        performance = data.get('performance_metrics', {})
        if performance:
            st.subheader("Performance Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fcp = performance.get('first_contentful_paint', {})
                if isinstance(fcp, dict):
                    fcpValue = fcp.get('display_value', 'N/A')
                else:
                    fcpValue = str(fcp) if fcp else 'N/A'
                st.metric("First Contentful Paint", f"{fcpValue}")
            
            with col2:
                lcp = performance.get('largest_contentful_paint', {})
                if isinstance(lcp, dict):
                    lcpValue = lcp.get('display_value', 'N/A')
                else:
                    lcpValue = str(lcp) if lcp else 'N/A'
                st.metric("Largest Contentful Paint", f"{lcpValue}")
            
            with col3:
                si = performance.get('speed_index', {})
                if isinstance(si, dict):
                    siValue = si.get('display_value', 'N/A')
                else:
                    siValue = str(si) if si else 'N/A'
                st.metric("Speed Index", f"{siValue}")
    
    
    def render_score_card(self, title, score, icon):
        """Render a score card with color coding"""
        # Determine score category and color
        if score >= 90:
            category = "Excellent"
            color_class = "score-excellent"
        elif score >= 70:
            category = "Good"
            color_class = "score-good"
        else:
            category = "Poor"
            color_class = "score-poor"
        
        st.markdown(f"""
        <div class="metric-card {color_class}">
            <h3>{icon} {title}</h3>
            <h2>{score:.0f}/100</h2>
            <p>{category}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_core_web_vitals(self, vitals):
        """Render Core Web Vitals metrics"""
        if not vitals:
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lcp = vitals.get('largest_contentful_paint', {})
            lcp_display = lcp.get('display_value', 'N/A') if isinstance(lcp, dict) else str(lcp)
            st.metric("LCP", lcp_display, help="Largest Contentful Paint")
        
        with col2:
            fid = vitals.get('max_potential_fid', {})
            fid_display = fid.get('display_value', 'N/A') if isinstance(fid, dict) else str(fid)
            st.metric("FID", fid_display, help="First Input Delay")
        
        with col3:
            cls = vitals.get('cumulative_layout_shift', {})
            cls_display = cls.get('display_value', 'N/A') if isinstance(cls, dict) else str(cls)
            st.metric("CLS", cls_display, help="Cumulative Layout Shift")
    
    def render_device_comparison(self, results):
        """Render comparison between mobile and desktop"""
        if 'mobile' not in results or 'desktop' not in results:
            st.warning("No comparison data available")
            return
        
        
        
        mobile_score = results['mobile'].get('performance_score', 0) * 100
        desktop_score = results['desktop'].get('performance_score', 0) * 100
        
        # Create comparison chart
        fig = go.Figure(data=[
            go.Bar(name='Mobile', x=['Performance Score'], y=[mobile_score], marker_color='#667eea'),
            go.Bar(name='Desktop', x=['Performance Score'], y=[desktop_score], marker_color='#764ba2')
        ])
        
        fig.update_layout(
            title="Mobile vs Desktop Performance",
            yaxis_title="Score",
            yaxis_range=[0, 100],
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_analysis_page(self):
        """Render the content analysis page"""
        st.header("📝 Content Analysis")
        st.write("Analyze website content and structure")
        
        # URL input
        url = st.text_input("Enter website URL for content analysis:", placeholder="https://example.com")
        
        if st.button("Run Content Analysis", type="primary"):
            if url:
                with st.spinner("Analyzing website content..."):
                    self.run_content_analysis(url)
            else:
                st.error("Please enter a valid URL")
        
        # Display results
        if st.session_state.content_results:
            self.display_content_analysis()
    
    def run_content_analysis(self, url: str):
        """Run content analysis for the given URL"""
        try:
            # Scrape website content
            scraped_data = self.web_scraper.scrape_website(url)
            
            if scraped_data and scraped_data.get('pages'):
                # Get HTML content for AI analysis
                html_content = scraped_data.get('raw_html', '')
                
                # Process the scraped data with enhanced analysis
                content_results = self.data_processor.analyze_website_comprehensive(
                    url, html_content, scraped_data
                )
                
                st.session_state.content_results = {
                    'scraped_data': scraped_data,
                    'analysis': content_results
                }
                st.success("Content analysis completed successfully!")
            else:
                st.error("No content data received. Please check the URL and try again.")
                
        except Exception as e:
            st.error(f"Error running content analysis: {str(e)}")
            st.info("Please ensure the URL is accessible and try again.")
    
    def display_content_analysis(self):
        """Display content analysis results"""
        results = st.session_state.content_results
        
        if not results:
            st.warning("No content analysis results available. Please run a content analysis first.")
            return
        
        analysis = results.get('analysis', {})
        scraped_data = results.get('scraped_data', {})
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pages Analyzed", scraped_data.get('pages_analyzed', 0))
        
        with col2:
            st.metric("Total Word Count", f"{scraped_data.get('total_word_count', 0):,}")
        
        with col3:
            st.metric("Images Found", scraped_data.get('image_count', 0))
        
        with col4:
            st.metric("Internal Links", scraped_data.get('internal_links_count', 0))
        
        # Enhanced analysis results
        st.subheader("🤖 AI-Powered Analysis")
        
        # Brand Identity
        brand_identity = analysis.get('ai_analysis', {}).get('brand_identity', {})
        if brand_identity:
            st.markdown("#### 🎨 Brand Identity")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Brand Tone:** {brand_identity.get('tone', 'N/A')}")
                st.markdown(f"**Visual Style:** {brand_identity.get('visual_style', 'N/A')}")
                st.markdown(f"**Brand Personality:** {brand_identity.get('personality', 'N/A')}")
            
            with col2:
                colors = brand_identity.get('colors', [])
                if colors:
                    st.markdown("**Brand Colors:**")
                    for color in colors[:3]:  # Show first 3 colors
                        st.markdown(f"• {color}")
        
        # Industry Analysis
        industry_analysis = analysis.get('ai_analysis', {}).get('industry_analysis', {})
        if industry_analysis:
            st.markdown("#### 🏭 Industry Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Primary Industry:** {industry_analysis.get('primary_industry', 'N/A')}")
                st.markdown(f"**Market Position:** {industry_analysis.get('market_position', 'N/A')}")
            
            with col2:
                st.markdown(f"**Target Market:** {industry_analysis.get('target_market', 'N/A')}")
                challenges = industry_analysis.get('challenges', [])
                if challenges:
                    st.markdown("**Industry Challenges:**")
                    for challenge in challenges[:2]:
                        st.markdown(f"• {challenge}")
        
        # Target Audience
        target_audience = analysis.get('ai_analysis', {}).get('target_audience', {})
        if target_audience:
            st.markdown("#### 👥 Target Audience")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Primary Audience:** {target_audience.get('primary_audience', 'N/A')}")
                st.markdown(f"**Demographics:** {target_audience.get('demographics', 'N/A')}")
            
            with col2:
                pain_points = target_audience.get('pain_points', [])
                if pain_points:
                    st.markdown("**Pain Points:**")
                    for point in pain_points[:3]:
                        st.markdown(f"• {point}")
        
        # Website Goals
        website_goals = analysis.get('ai_analysis', {}).get('website_goals', {})
        if website_goals:
            st.markdown("#### 🎯 Website Goals")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Primary Goal:** {website_goals.get('primary_goal', 'N/A')}")
                conversion_actions = website_goals.get('conversion_actions', [])
                if conversion_actions:
                    st.markdown("**Conversion Actions:**")
                    for action in conversion_actions[:3]:
                        st.markdown(f"• {action}")
            
            with col2:
                ctas = website_goals.get('call_to_actions', [])
                if ctas:
                    st.markdown("**Recommended CTAs:**")
                    for cta in ctas[:3]:
                        st.markdown(f"• {cta}")
        
        # Value Propositions
        value_props = analysis.get('ai_analysis', {}).get('value_propositions', {})
        if value_props:
            st.markdown("#### 💎 Value Propositions")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Primary VP:** {value_props.get('primary_vp', 'N/A')}")
                usp = value_props.get('usp', 'N/A')
                st.markdown(f"**Unique Selling Point:** {usp}")
            
            with col2:
                benefits = value_props.get('benefits', [])
                if benefits:
                    st.markdown("**Key Benefits:**")
                    for benefit in benefits[:3]:
                        st.markdown(f"• {benefit}")
        
        # Content Strategy
        content_strategy = analysis.get('ai_analysis', {}).get('content_strategy', {})
        if content_strategy:
            st.markdown("#### 📝 Content Strategy")
            col1, col2 = st.columns(2)
            
            with col1:
                key_messages = content_strategy.get('key_messages', [])
                if key_messages:
                    st.markdown("**Key Messages:**")
                    for message in key_messages[:3]:
                        st.markdown(f"• {message}")
            
            with col2:
                content_themes = content_strategy.get('content_themes', [])
                if content_themes:
                    st.markdown("**Content Themes:**")
                    for theme in content_themes[:3]:
                        st.markdown(f"• {theme}")
        
        # Conversion Elements
        conversion_elements = analysis.get('ai_analysis', {}).get('conversion_elements', {})
        if conversion_elements:
            st.markdown("#### 🎯 Conversion Optimization")
            col1, col2 = st.columns(2)
            
            with col1:
                primary_ctas = conversion_elements.get('primary_ctas', [])
                if primary_ctas:
                    st.markdown("**Primary CTAs:**")
                    for cta in primary_ctas[:3]:
                        st.markdown(f"• {cta}")
            
            with col2:
                trust_elements = conversion_elements.get('trust_elements', [])
                if trust_elements:
                    st.markdown("**Trust Elements:**")
                    for element in trust_elements[:3]:
                        st.markdown(f"• {element}")
        
        # Technical Requirements
        technical_insights = analysis.get('ai_analysis', {}).get('technical_insights', {})
        if technical_insights:
            st.markdown("#### ⚙️ Technical Requirements")
            col1, col2 = st.columns(2)
            
            with col1:
                essential_features = technical_insights.get('essential_features', [])
                if essential_features:
                    st.markdown("**Essential Features:**")
                    for feature in essential_features[:3]:
                        st.markdown(f"• {feature}")
            
            with col2:
                seo_requirements = technical_insights.get('seo_requirements', [])
                if seo_requirements:
                    st.markdown("**SEO Requirements:**")
                    for req in seo_requirements[:3]:
                        st.markdown(f"• {req}")
        
        # Detailed analysis tabs
        st.subheader("📊 Detailed Analysis")
        
        tab1, tab2, tab3 = st.columns(3)
        
        with tab1:
            if st.button("View SEO Analysis", use_container_width=True):
                self.display_seo_analysis(analysis.get('basic_analysis', {}).get('seo_elements', {}))
        
        with tab2:
            if st.button("View Content Quality", use_container_width=True):
                self.display_content_quality(analysis.get('basic_analysis', {}).get('content_quality', {}))
        
        with tab3:
            if st.button("View Technical SEO", use_container_width=True):
                self.display_technical_seo(analysis.get('basic_analysis', {}).get('technical_seo', {}))
    
    def display_seo_analysis(self, seo_data):
        """Display SEO analysis results"""
        if not seo_data:
            st.warning("No SEO data available")
            return
        
        # SEO Score
        seo_score = seo_data.get('seo_score', 0)
        st.metric("SEO Score", f"{seo_score}/100")
        
        # Issues and strengths
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("SEO Issues")
            issues = seo_data.get('issues', [])
            if issues:
                for issue in issues:
                    st.write(f"• {issue}")
            else:
                st.write("No major SEO issues found")
        
        with col2:
            st.subheader("SEO Strengths")
            strengths = seo_data.get('strengths', [])
            if strengths:
                for strength in strengths:
                    st.write(f"• {strength}")
            else:
                st.write("No specific strengths identified")
    
    def display_content_quality(self, quality_data):
        """Display content quality analysis"""
        if not quality_data:
            st.warning("No content quality data available")
            return
        
        # Quality metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Quality Score", f"{quality_data.get('overall_quality_score', 0):.0f}/100")
        
        with col2:
            st.metric("Avg Words per Page", f"{quality_data.get('avg_word_count_per_page', 0):.0f}")
        
        with col3:
            st.metric("Readability Score", f"{quality_data.get('avg_readability_score', 0):.0f}/100")
    
    
    def display_technical_seo(self, technical_data):
        """Display technical SEO analysis"""
        if not technical_data:
            st.warning("No technical SEO data available")
            return
        
        # Technical score
        technical_score = technical_data.get('technical_score', 0)
        st.metric("Technical SEO Score", f"{technical_score}/100")
        
        # Technical checks
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Technical Checks")
            
            https_analysis = technical_data.get('https_analysis', {})
            if https_analysis.get('uses_https'):
                st.write("✅ HTTPS enabled")
            else:
                st.write("❌ HTTPS not enabled")
            
            structured_data = technical_data.get('structured_data_analysis', {})
            if structured_data.get('has_structured_data'):
                st.write("✅ Structured data present")
            else:
                st.write("❌ No structured data found")
        
        with col2:
            st.subheader("URL Analysis")
            url_analysis = technical_data.get('url_analysis', {})
            if url_analysis.get('issues'):
                for issue in url_analysis['issues'][:3]:
                    st.write(f"• {issue}")
            else:
                st.write("No URL issues found")
    
    def render_prompt_page(self):
        """Render the AI prompt generator page"""
        st.header("🤖 AI Prompt Generator")
        st.write("Generate comprehensive AI prompts for page builders based on audit results")
        
        # Check if we have the required data
        if not st.session_state.audit_results:
            st.warning("Please run a performance audit first")
            return
        
        if not st.session_state.content_results:
            st.warning("Please run a content analysis first")
            return
        
        # Generate prompt button
        if st.button("Generate AI Prompt", type="primary"):
            with st.spinner("Generating comprehensive AI prompt..."):
                self.generate_ai_prompt()
        
        # Display generated prompt
        if st.session_state.generated_prompt:
            self.display_generated_prompt()
    
    def generate_ai_prompt(self):
        """Generate AI prompt using audit and content data"""
        try:
            url = st.session_state.audit_results.get('url', 'Unknown URL')
            audit_data = st.session_state.audit_results
            content_data = st.session_state.content_results
            
            # Extract the analysis data correctly
            if content_data and 'analysis' in content_data:
                analysis_data = content_data['analysis']
                # Create a structure that matches what the prompt generator expects
                enhanced_content_data = {
                    'analysis': analysis_data,
                    'scraped_data': content_data.get('scraped_data', {})
                }
            else:
                st.error("No content analysis data available")
                return
            
            # Generate the prompt
            prompt = self.prompt_generator.generate_prompt(url, audit_data, enhanced_content_data)
            
            st.session_state.generated_prompt = prompt
            st.success("AI prompt generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating AI prompt: {str(e)}")
            import traceback
            st.error(f"Traceback: {traceback.format_exc()}")
    
    def display_generated_prompt(self):
        """Display the generated AI prompt"""
        prompt = st.session_state.generated_prompt
        
        st.subheader("Generated AI Prompt")
        st.write("Use this prompt with your preferred AI page builder:")
        
        # Display prompt in a formatted box
        st.markdown(f"""
        <div class="prompt-box">
            {prompt}
        </div>
        """, unsafe_allow_html=True)
        
        # Download options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download as TXT"):
                prompt_bytes = self.prompt_generator.export_prompt(prompt, 'txt')
                st.download_button(
                    label="Download TXT",
                    data=prompt_bytes,
                    file_name="ai_prompt.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("Download as JSON"):
                prompt_bytes = self.prompt_generator.export_prompt(prompt, 'json')
                st.download_button(
                    label="Download JSON",
                    data=prompt_bytes,
                    file_name="ai_prompt.json",
                    mime="application/json"
                )

# Run the app
if __name__ == "__main__":
    app = WebsiteAuditApp()
    app.run()