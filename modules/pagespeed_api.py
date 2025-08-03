import requests 
import time
from typing import Dict, Any, Optional
import logging
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PageSpeedAnalyzer:
    """
    Google PageSpeed Insights API integration for comprehensive website performance analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PageSpeed analyzer
        
        Args:
            api_key: Google PageSpeed Insights API key (optional but recommended for higher rate limits)
        """
        self.api_key = api_key or st.secrets.get("PAGESPEED_API_KEY", "")
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        
        # Configure retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Categories to analyze
        self.categories = [
            'performance',
            'accessibility', 
            'best-practices',
            'seo'
        ]
        
        # Core Web Vitals mapping
        self.core_vitals_mapping = {
            'largest-contentful-paint': 'largest_contentful_paint',
            'first-input-delay': 'first_input_delay',
            'cumulative-layout-shift': 'cumulative_layout_shift',
            'first-contentful-paint': 'first_contentful_paint',
            'time-to-interactive': 'time_to_interactive',
            'speed-index': 'speed_index'
        }
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze URL for both mobile and desktop performance
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Comprehensive analysis results for both mobile and desktop
        """
        try:
            logger.info(f"Starting comprehensive analysis for {url}")
            
            # Analyze both mobile and desktop
            mobile_results = self.analyze(url, 'mobile')
            desktop_results = self.analyze(url, 'desktop')
            
            # Combine results
            combined_results = {
                'url': url,
                'mobile': mobile_results,
                'desktop': desktop_results,
                'overall': {
                    'avg_performance': (mobile_results.get('performance_score', 0) + desktop_results.get('performance_score', 0)) / 2,
                    'avg_accessibility': (mobile_results.get('accessibility_score', 0) + desktop_results.get('accessibility_score', 0)) / 2,
                    'avg_seo': (mobile_results.get('seo_score', 0) + desktop_results.get('seo_score', 0)) / 2,
                    'avg_best_practices': (mobile_results.get('best_practices_score', 0) + desktop_results.get('best_practices_score', 0)) / 2
                }
            }
            
            logger.info(f"Comprehensive analysis completed for {url}")
            return combined_results
            
        except Exception as e:
            logger.error(f"Error analyzing {url}: {str(e)}")
            raise Exception(f"URL analysis failed: {str(e)}")
    
    def analyze(self, url: str, strategy: str = 'mobile') -> Dict[str, Any]:
        """
        Perform comprehensive PageSpeed analysis
        
        Args:
            url: Website URL to analyze
            strategy: Analysis strategy ('mobile' or 'desktop')
            
        Returns:
            Comprehensive analysis results
        """
        try:
            logger.info(f"Starting PageSpeed analysis for {url} ({strategy})")
            
            # Validate URL
            if not self._validate_url(url):
                raise ValueError("Invalid URL format")
            
            # Check API key status
            has_api_key = self._check_api_key()
            
            # Make API request
            api_response = self._make_api_request(url, strategy)
            
            # Process and structure the response
            processed_results = self._process_api_response(api_response, url, strategy)
            
            # Add API key status to results
            processed_results['api_key_used'] = has_api_key
            
            logger.info(f"PageSpeed analysis completed for {url}")
            return processed_results
            
        except Exception as e:
            logger.error(f"Error analyzing {url}: {str(e)}")
            raise Exception(f"PageSpeed analysis failed: {str(e)}")
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        
        if not url.startswith(('http://', 'https://')):
            return False
        
        return True
    
    def _check_api_key(self) -> bool:
        """Check if API key is available and valid"""
        if not self.api_key:
            logger.warning("No API key provided. Using public API with limited rate limits.")
            return False
        return True
    
    def _make_api_request(self, url: str, strategy: str) -> Dict[str, Any]:
        """
        Make API request to Google PageSpeed Insights
        
        Args:
            url: Website URL
            strategy: mobile or desktop
            
        Returns:
            Raw API response
        """
        # Build request parameters
        params = {
            'url': url,
            'strategy': strategy,
            'category': self.categories
        }
        
        # Add API key if available
        if self.api_key:
            params['key'] = self.api_key
        
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Making API request to PageSpeed Insights (attempt {attempt + 1}/{max_retries})")
                
                # Make request with timeout - increased timeout for slow sites
                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=(10, 60)  # (connect timeout, read timeout)
                )
                
                # Check for API errors
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Rate limited, waiting {delay} seconds before retry...")
                        time.sleep(delay)
                        continue
                    else:
                        raise Exception("API rate limit exceeded. Please try again later.")
                elif response.status_code == 400:
                    raise Exception("Invalid request. Please check the URL format.")
                elif response.status_code == 403:
                    raise Exception("API key is invalid or quota exceeded. Please check your API key.")
                elif response.status_code != 200:
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                
                return response.json()
                
            except requests.Timeout as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Request timed out, retrying in {delay} seconds... (attempt {attempt + 1})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Request timed out after {max_retries} attempts. The website may be too slow to analyze.")
                    
            except requests.ConnectionError as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Connection error, retrying in {delay} seconds... (attempt {attempt + 1})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Connection error after {max_retries} attempts. Please check your internet connection.")
                    
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Network error: {str(e)}, retrying in {delay} seconds... (attempt {attempt + 1})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Network error during API request after {max_retries} attempts: {str(e)}")
        
        # This should never be reached, but just in case
        raise Exception("Failed to make API request after all retry attempts")
    
    def _process_api_response(self, response: Dict[str, Any], url: str, strategy: str) -> Dict[str, Any]:
        """
        Process and structure the API response into a clean format
        
        Args:
            response: Raw API response
            url: Original URL
            strategy: Analysis strategy
            
        Returns:
            Processed and structured results
        """
        try:
            lighthouse_result = response.get('lighthouseResult', {})
            loading_experience = response.get('loadingExperience', {})
            
            # Extract category scores
            categories = lighthouse_result.get('categories', {})
            audits = lighthouse_result.get('audits', {})
            
            # Structure the results
            processed_data = {
                'url': url,
                'strategy': strategy,
                'fetch_time': lighthouse_result.get('fetchTime'),
                'lighthouse_version': lighthouse_result.get('lighthouseVersion'),
                
                # Core scores
                'performance_score': categories.get('performance', {}).get('score', 0),
                'accessibility_score': categories.get('accessibility', {}).get('score', 0),
                'best_practices_score': categories.get('best-practices', {}).get('score', 0),
                'seo_score': categories.get('seo', {}).get('score', 0),
                
                # Core Web Vitals
                'core_web_vitals': self._extract_core_web_vitals(audits, loading_experience),
                
                # Performance metrics
                'performance_metrics': self._extract_performance_metrics(audits),
                
                # Opportunities (performance improvements)
                'opportunities': self._extract_opportunities(audits),
                
                # Diagnostics (additional insights)
                'diagnostics': self._extract_diagnostics(audits),
                
                # SEO audits
                'seo_audits': self._extract_seo_audits(audits),
                
                # Accessibility audits
                'accessibility_audits': self._extract_accessibility_audits(audits),
                
                # Loading experience (real user data)
                'loading_experience': self._process_loading_experience(loading_experience),
                
                # Resource summary
                'resource_summary': self._extract_resource_summary(audits)
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing API response: {str(e)}")
            raise Exception(f"Failed to process PageSpeed results: {str(e)}")
    
    def _extract_core_web_vitals(self, audits: Dict, loading_experience: Dict) -> Dict[str, Any]:
        """Extract Core Web Vitals metrics"""
        vitals = {}
        
        # From Lighthouse audits
        for audit_id, vital_key in self.core_vitals_mapping.items():
            audit = audits.get(audit_id, {})
            if audit:
                value = audit.get('numericValue', 0)
                
                # Convert milliseconds to seconds for certain metrics
                if audit_id in ['largest-contentful-paint', 'first-contentful-paint', 'time-to-interactive']:
                    value = value / 1000 if value else 0
                
                vitals[vital_key] = {
                    'value': value,
                    'score': audit.get('score', 0),
                    'display_value': audit.get('displayValue', ''),
                    'description': audit.get('description', '')
                }
        
        # Add real user data if available
        if loading_experience:
            metrics = loading_experience.get('metrics', {})
            for metric_name, metric_data in metrics.items():
                if metric_name == 'FIRST_CONTENTFUL_PAINT_MS':
                    vitals['fcp_real_user'] = {
                        'percentile': metric_data.get('percentile', 0) / 1000,
                        'category': metric_data.get('category', 'UNKNOWN')
                    }
                elif metric_name == 'FIRST_INPUT_DELAY_MS':
                    vitals['fid_real_user'] = {
                        'percentile': metric_data.get('percentile', 0),
                        'category': metric_data.get('category', 'UNKNOWN')
                    }
        
        return vitals
    
    def _extract_performance_metrics(self, audits: Dict) -> Dict[str, Any]:
        """Extract additional performance metrics"""
        metrics = {}
        
        performance_audits = [
            'first-contentful-paint', 'largest-contentful-paint', 'first-meaningful-paint',
            'speed-index', 'time-to-interactive', 'max-potential-fid', 'cumulative-layout-shift'
        ]
        
        for audit_id in performance_audits:
            audit = audits.get(audit_id, {})
            if audit:
                metrics[audit_id.replace('-', '_')] = {
                    'value': audit.get('numericValue', 0),
                    'score': audit.get('score', 0),
                    'display_value': audit.get('displayValue', ''),
                    'title': audit.get('title', ''),
                    'description': audit.get('description', '')
                }
        
        return metrics
    
    def _extract_opportunities(self, audits: Dict) -> list:
        """Extract performance optimization opportunities"""
        opportunities = []
        
        opportunity_audits = [
            'render-blocking-resources', 'unused-css-rules', 'unused-javascript',
            'modern-image-formats', 'offscreen-images', 'minify-css', 'minify-javascript',
            'enable-text-compression', 'properly-size-images', 'efficient-animated-content',
            'preload-lcp-image', 'uses-optimized-images'
        ]
        
        for audit_id in opportunity_audits:
            audit = audits.get(audit_id, {})
            if audit and audit.get('score', 1) < 1:  # Only include failed audits
                details = audit.get('details', {})
                savings_ms = details.get('overallSavingsMs', 0)
                savings_kb = details.get('overallSavingsBytes', 0) / 1024 if details.get('overallSavingsBytes') else 0
                
                opportunities.append({
                    'id': audit_id,
                    'title': audit.get('title', ''),
                    'description': audit.get('description', ''),
                    'score': audit.get('score', 0),
                    'display_value': audit.get('displayValue', ''),
                    'savings_ms': savings_ms,
                    'savings_kb': savings_kb,
                    'impact': self._calculate_impact(savings_ms, savings_kb),
                    'items': details.get('items', [])[:5]  # Limit to top 5 items
                })
        
        # Sort by impact (highest first)
        opportunities.sort(key=lambda x: x['impact'], reverse=True)
        return opportunities
    
    def _extract_diagnostics(self, audits: Dict) -> list:
        """Extract diagnostic information"""
        diagnostics = []
        
        diagnostic_audits = [
            'mainthread-work-breakdown', 'bootup-time', 'uses-rel-preconnect',
            'font-display', 'third-party-summary', 'largest-contentful-paint-element',
            'avoid-enormous-network-payloads', 'uses-long-cache-ttl', 'total-byte-weight'
        ]
        
        for audit_id in diagnostic_audits:
            audit = audits.get(audit_id, {})
            if audit:
                diagnostics.append({
                    'id': audit_id,
                    'title': audit.get('title', ''),
                    'description': audit.get('description', ''),
                    'score': audit.get('score'),
                    'display_value': audit.get('displayValue', ''),
                    'details': audit.get('details', {})
                })
        
        return diagnostics
    
    def _extract_seo_audits(self, audits: Dict) -> list:
        """Extract SEO audit results"""
        seo_audits = []
        
        seo_audit_ids = [
            'document-title', 'meta-description', 'http-status-code', 'link-text',
            'crawlable-anchors', 'is-crawlable', 'robots-txt', 'image-alt',
            'hreflang', 'canonical', 'structured-data'
        ]
        
        for audit_id in seo_audit_ids:
            audit = audits.get(audit_id, {})
            if audit:
                seo_audits.append({
                    'id': audit_id,
                    'title': audit.get('title', ''),
                    'description': audit.get('description', ''),
                    'score': audit.get('score'),
                    'score_display_mode': audit.get('scoreDisplayMode', ''),
                    'display_value': audit.get('displayValue', ''),
                    'details': audit.get('details', {})
                })
        
        return seo_audits
    
    def _extract_accessibility_audits(self, audits: Dict) -> list:
        """Extract accessibility audit results"""
        a11y_audits = []
        
        a11y_audit_ids = [
            'color-contrast', 'image-alt', 'label', 'link-name', 'list',
            'meta-viewport', 'heading-order', 'html-has-lang', 'valid-lang'
        ]
        
        for audit_id in a11y_audit_ids:
            audit = audits.get(audit_id, {})
            if audit:
                a11y_audits.append({
                    'id': audit_id,
                    'title': audit.get('title', ''),
                    'description': audit.get('description', ''),
                    'score': audit.get('score'),
                    'score_display_mode': audit.get('scoreDisplayMode', ''),
                    'display_value': audit.get('displayValue', ''),
                    'details': audit.get('details', {})
                })
        
        return a11y_audits
    
    def _process_loading_experience(self, loading_experience: Dict) -> Dict[str, Any]:
        """Process real user loading experience data"""
        if not loading_experience:
            return {}
        
        metrics = loading_experience.get('metrics', {})
        processed_metrics = {}
        
        for metric_name, metric_data in metrics.items():
            processed_metrics[metric_name.lower()] = {
                'percentile': metric_data.get('percentile', 0),
                'category': metric_data.get('category', 'UNKNOWN'),
                'distributions': metric_data.get('distributions', [])
            }
        
        return {
            'overall_category': loading_experience.get('overall_category', 'UNKNOWN'),
            'metrics': processed_metrics
        }
    
    def _extract_resource_summary(self, audits: Dict) -> Dict[str, Any]:
        """Extract resource usage summary"""
        resource_summary = {
            'total_byte_weight': 0,
            'image_count': 0,
            'script_count': 0,
            'stylesheet_count': 0,
            'font_count': 0,
            'total_requests': 0
        }
        
        # Total byte weight
        byte_weight_audit = audits.get('total-byte-weight', {})
        if byte_weight_audit:
            resource_summary['total_byte_weight'] = byte_weight_audit.get('numericValue', 0)
        
        # Resource counts from network requests
        network_requests_audit = audits.get('network-requests', {})
        if network_requests_audit:
            details = network_requests_audit.get('details', {})
            items = details.get('items', [])
            
            for item in items:
                resource_type = item.get('resourceType', '').lower()
                if resource_type == 'image':
                    resource_summary['image_count'] += 1
                elif resource_type == 'script':
                    resource_summary['script_count'] += 1
                elif resource_type == 'stylesheet':
                    resource_summary['stylesheet_count'] += 1
                elif resource_type == 'font':
                    resource_summary['font_count'] += 1
            
            resource_summary['total_requests'] = len(items)
        
        return resource_summary
    
    def _calculate_impact(self, savings_ms: float, savings_kb: float) -> str:
        """Calculate impact level based on potential savings"""
        if savings_ms > 1000 or savings_kb > 100:
            return 'HIGH'
        elif savings_ms > 500 or savings_kb > 50:
            return 'MEDIUM'
        elif savings_ms > 100 or savings_kb > 10:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def analyze_with_fallback(self, url: str, strategy: str = 'mobile') -> Dict[str, Any]:
        """
        Analyze URL with fallback for slow websites
        
        Args:
            url: Website URL to analyze
            strategy: Analysis strategy
            
        Returns:
            Analysis results or fallback data
        """
        try:
            return self.analyze(url, strategy)
        except Exception as e:
            error_msg = str(e)
            
            # If it's a timeout, provide helpful fallback
            if "timed out" in error_msg.lower():
                logger.warning(f"Analysis timed out for {url}, providing fallback data")
                return {
                    'url': url,
                    'strategy': strategy,
                    'error': 'timeout',
                    'message': 'Website analysis timed out. This may indicate the site is very slow or unresponsive.',
                    'recommendations': [
                        'Check if the website is accessible in a browser',
                        'The site may be experiencing high load or technical issues',
                        'Try analyzing during off-peak hours',
                        'Consider using a different URL or subdomain'
                    ],
                    'fallback_data': {
                        'performance_score': 0,
                        'accessibility_score': 0,
                        'best_practices_score': 0,
                        'seo_score': 0,
                        'core_web_vitals': {},
                        'performance_metrics': {},
                        'opportunities': [],
                        'diagnostics': [],
                        'seo_audits': [],
                        'accessibility_audits': [],
                        'loading_experience': {},
                        'resource_summary': {}
                    }
                }
            else:
                # Re-raise other errors
                raise e
    
    def batch_analyze(self, urls: list, strategy: str = 'mobile') -> Dict[str, Any]:
        """
        Analyze multiple URLs in batch
        
        Args:
            urls: List of URLs to analyze
            strategy: Analysis strategy
            
        Returns:
            Dictionary with results for each URL
        """
        results = {}
        
        for i, url in enumerate(urls):
            try:
                logger.info(f"Analyzing URL {i+1}/{len(urls)}: {url}")
                results[url] = self.analyze(url, strategy)
                
                # Rate limiting - wait between requests
                if i < len(urls) - 1:  # Don't wait after the last request
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Failed to analyze {url}: {str(e)}")
                results[url] = {'error': str(e)}
        
        return results
    
    def compare_strategies(self, url: str) -> Dict[str, Any]:
        """
        Compare mobile vs desktop performance
        
        Args:
            url: URL to analyze
            
        Returns:
            Comparison results
        """
        mobile_results = self.analyze(url, 'mobile')
        desktop_results = self.analyze(url, 'desktop')
        
        comparison = {
            'mobile': mobile_results,
            'desktop': desktop_results,
            'comparison': {
                'performance_diff': desktop_results['performance_score'] - mobile_results['performance_score'],
                'accessibility_diff': desktop_results['accessibility_score'] - mobile_results['accessibility_score'],
                'seo_diff': desktop_results['seo_score'] - mobile_results['seo_score'],
                'best_practices_diff': desktop_results['best_practices_score'] - mobile_results['best_practices_score']
            }
        }
        
        return comparison