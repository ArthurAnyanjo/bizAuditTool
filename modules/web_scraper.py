import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, parse_qs
from typing import Dict, List, Any, Optional, Set
import time
import logging
from collections import Counter
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """
    Comprehensive web scraping module for extracting website content and structure
    """
    
    def __init__(self, max_pages: int = 10, delay: float = 1.0):
        """
        Initialize web scraper
        
        Args:
            max_pages: Maximum number of pages to scrape
            delay: Delay between requests in seconds
        """
        self.max_pages = max_pages
        self.delay = delay
        self.session = requests.Session()
        
        # Set user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Common page types to look for
        self.target_pages = [
            'about', 'contact', 'services', 'products', 'home', 'index',
            'team', 'careers', 'blog', 'news', 'pricing', 'features'
        ]
    
    def scrape_website(self, base_url: str) -> Dict[str, Any]:
        """
        Scrape website content and structure
        
        Args:
            base_url: Base URL of the website
            
        Returns:
            Comprehensive website data
        """
        try:
            logger.info(f"Starting website scrape for {base_url}")
            
            # Normalize URL
            base_url = self._normalize_url(base_url)
            
            # Get main page content
            main_page = self._scrape_page(base_url)
            if not main_page:
                raise Exception("Could not access main page")
            
            # Find additional pages to scrape
            additional_urls = self._find_target_pages(base_url, main_page['soup'])
            
            # Scrape additional pages
            all_pages = [main_page]
            for url in additional_urls[:self.max_pages-1]:  # -1 because we already have main page
                page_data = self._scrape_page(url)
                if page_data:
                    all_pages.append(page_data)
                time.sleep(self.delay)
            
            # Compile comprehensive website data
            website_data = self._compile_website_data(all_pages, base_url)
            
            logger.info(f"Website scrape completed. Analyzed {len(all_pages)} pages")
            return website_data
            
        except Exception as e:
            logger.error(f"Error scraping website {base_url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ''
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        return meta_desc.get('content', '').strip() if meta_desc else ''
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all heading tags"""
        headings = {}
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            heading_tags = soup.find_all(level)
            headings[level] = [tag.get_text().strip() for tag in heading_tags if tag.get_text().strip()]
        return headings
    
    def _extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract main content from page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find main content area
        main_content = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find('div', class_=re.compile(r'content|main', re.I)) or
            soup.find('body')
        )
        
        if not main_content:
            return {'text': '', 'paragraphs': [], 'sections': []}
        
        # Extract text content
        text = main_content.get_text()
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        
        # Extract paragraphs
        paragraphs = []
        for p in main_content.find_all('p'):
            p_text = p.get_text().strip()
            if len(p_text) > 20:  # Filter out very short paragraphs
                paragraphs.append(p_text)
        
        # Extract sections
        sections = []
        for section in main_content.find_all(['section', 'div'], class_=re.compile(r'section|block', re.I)):
            section_title = ''
            # Look for section title
            title_tag = section.find(['h1', 'h2', 'h3', 'h4'])
            if title_tag:
                section_title = title_tag.get_text().strip()
            
            section_text = section.get_text().strip()
            if len(section_text) > 50:
                sections.append({
                    'title': section_title,
                    'content': section_text[:500] + '...' if len(section_text) > 500 else section_text
                })
        
        return {
            'text': cleaned_text,
            'paragraphs': paragraphs,
            'sections': sections
        }
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract image information"""
        images = []
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src', '')
            if src:
                # Convert relative URLs to absolute
                if src.startswith('/'):
                    src = urljoin(base_url, src)
                elif not src.startswith(('http://', 'https://')):
                    src = urljoin(base_url, src)
                
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                    'loading': img.get('loading', ''),
                    'has_alt': bool(img.get('alt', '').strip())
                })
        
        return images
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract internal and external links"""
        internal_links = []
        external_links = []
        
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').strip()
            if not href or href.startswith(('#', 'mailto:', 'tel:')):
                continue
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                full_url = urljoin(base_url, href)
                is_internal = True
            elif not href.startswith(('http://', 'https://')):
                full_url = urljoin(base_url, href)
                is_internal = True
            else:
                full_url = href
                is_internal = urlparse(href).netloc == base_domain
            
            link_data = {
                'url': full_url,
                'text': link.get_text().strip(),
                'title': link.get('title', ''),
                'rel': link.get('rel', []),
                'target': link.get('target', '')
            }
            
            if is_internal:
                internal_links.append(link_data)
            else:
                external_links.append(link_data)
        
        return {
            'internal': internal_links,
            'external': external_links
        }
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all meta tags"""
        meta_tags = {}
        
        # Standard meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
            content = meta.get('content')
            
            if name and content:
                meta_tags[name.lower()] = content
        
        # Additional SEO-relevant tags
        canonical = soup.find('link', rel='canonical')
        if canonical:
            meta_tags['canonical'] = canonical.get('href', '')
        
        # Language
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            meta_tags['lang'] = html_tag.get('lang')
        
        return meta_tags
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract structured data (JSON-LD, microdata)"""
        structured_data = []
        
        # JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string)
                structured_data.append({
                    'type': 'json-ld',
                    'data': data
                })
            except (json.JSONDecodeError, AttributeError):
                continue
        
        # Microdata (basic extraction)
        microdata_items = soup.find_all(attrs={'itemtype': True})
        for item in microdata_items:
            structured_data.append({
                'type': 'microdata',
                'itemtype': item.get('itemtype'),
                'itemscope': item.has_attr('itemscope')
            })
        
        return structured_data
    
    def _calculate_word_count(self, soup: BeautifulSoup) -> int:
        """Calculate word count of main content"""
        # Remove non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)
    
    def _identify_page_type(self, url: str, soup: BeautifulSoup) -> str:
        """Identify the type of page based on URL and content"""
        url_lower = url.lower()
        title_lower = soup.find('title')
        title_text = title_lower.get_text().lower() if title_lower else ''
        
        # Check URL patterns
        for page_type in self.target_pages:
            if page_type in url_lower or page_type in title_text:
                return page_type
        
        # Check for specific patterns
        if any(word in url_lower for word in ['blog', 'news', 'article']):
            return 'blog'
        elif any(word in url_lower for word in ['shop', 'store', 'product']):
            return 'product'
        elif url_lower.endswith('/') or 'home' in url_lower or url_lower.count('/') <= 3:
            return 'home'
        
        return 'other'
    
    def _find_target_pages(self, base_url: str, soup: BeautifulSoup) -> List[str]:
        """Find target pages to scrape based on navigation and common patterns"""
        target_urls = set()
        base_domain = urlparse(base_url).netloc
        
        # Extract from navigation
        nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'nav|menu', re.I))
        
        for nav in nav_elements:
            for link in nav.find_all('a', href=True):
                href = link.get('href', '').strip()
                if not href:
                    continue
                
                # Convert to absolute URL
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif not href.startswith(('http://', 'https://')):
                    full_url = urljoin(base_url, href)
                else:
                    full_url = href
                
                # Check if it's internal and matches target pages
                if urlparse(full_url).netloc == base_domain:
                    url_path = urlparse(full_url).path.lower()
                    link_text = link.get_text().lower()
                    
                    if any(page_type in url_path or page_type in link_text 
                           for page_type in self.target_pages):
                        target_urls.add(full_url)
        
        # Also look for common page patterns in footer
        footer = soup.find('footer')
        if footer:
            for link in footer.find_all('a', href=True):
                href = link.get('href', '').strip()
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                    url_path = urlparse(full_url).path.lower()
                    link_text = link.get_text().lower()
                    
                    if any(page_type in url_path or page_type in link_text 
                           for page_type in ['about', 'contact', 'privacy', 'terms']):
                        target_urls.add(full_url)
        
        # Remove base URL if it's in the set
        target_urls.discard(base_url)
        target_urls.discard(base_url + '/')
        
        return list(target_urls)
    
    def _compile_website_data(self, pages: List[Dict[str, Any]], base_url: str) -> Dict[str, Any]:
        """Compile comprehensive website data from all scraped pages"""
        
        # Aggregate data across all pages
        all_headings = {}
        all_images = []
        all_internal_links = []
        all_external_links = []
        all_meta_tags = {}
        all_structured_data = []
        total_word_count = 0
        
        # Process each page
        for page in pages:
            # Aggregate headings
            for level, headings in page['headings'].items():
                if level not in all_headings:
                    all_headings[level] = []
                all_headings[level].extend(headings)
            
            # Aggregate other data
            all_images.extend(page['images'])
            all_internal_links.extend(page['links']['internal'])
            all_external_links.extend(page['links']['external'])
            all_structured_data.extend(page['structured_data'])
            total_word_count += page['word_count']
            
            # Collect meta tags (prefer homepage meta tags)
            if page['page_type'] == 'home' or not all_meta_tags:
                all_meta_tags.update(page['meta_tags'])
        
        # Analyze CSS styles from the main page
        css_analysis = {'colors': [], 'fonts': [], 'css_url': '', 'total_css_size': 0}
        if pages:
            main_page = pages[0]     
            css_files = self._extract_css_files(main_page['soup'])
            if css_files:
                # Analyze the first CSS file (usually the main stylesheet)
                main_css_url = css_files[0]
                css_analysis = self._analyze_css_styles(main_css_url)

        print("This is the css analysis", css_analysis)
        
        # Analyze content themes
        content_themes = self._analyze_content_themes(pages)
        
        # SEO analysis
        seo_analysis = self._perform_seo_analysis(pages, all_meta_tags, all_images)
        
        # Compile final website data
        website_data = {
            'base_url': base_url,
            'pages_analyzed': len(pages),
            'raw_html': pages[0]['raw_html'] if pages else '',  # Include raw HTML from main page
            'css_analysis': css_analysis,  # Include CSS analysis
            'pages': [{
                'url': page['url'],
                'title': page['title'],
                'meta_description': page['meta_description'],
                'page_type': page['page_type'],
                'word_count': page['word_count'],
                'headings': page['headings'],
                'content': page['content'],  # Include full content for AI analysis
                'content_preview': page['content']['text'][:300] + '...' if len(page['content']['text']) > 300 else page['content']['text']
            } for page in pages],
            
            # Aggregated data
            'total_word_count': total_word_count,
            'all_headings': all_headings,
            'image_count': len(all_images),
            'images_without_alt': len([img for img in all_images if not img['has_alt']]),
            'internal_links_count': len(set(link['url'] for link in all_internal_links)),
            'external_links_count': len(set(link['url'] for link in all_external_links)),
            
            # Content analysis
            'content_themes': content_themes,
            'page_types_found': list(set(page['page_type'] for page in pages)),
            
            # SEO data
            'meta_tags': all_meta_tags,
            'seo_analysis': seo_analysis,
            'structured_data': all_structured_data,
            
            # Detailed data for further analysis
            'detailed_images': all_images[:50],  # Limit for performance
            'sample_internal_links': all_internal_links[:20],
            'sample_external_links': all_external_links[:10],
        }
        
        return website_data
    
    def _analyze_content_themes(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content themes across pages"""
        all_text = []
        all_headings = []
        
        for page in pages:
            all_text.append(page['content']['text'])
            for level, headings in page['headings'].items():
                all_headings.extend(headings)
        
        # Combine all text
        combined_text = ' '.join(all_text).lower()
        combined_headings = ' '.join(all_headings).lower()
        
        # Extract keywords (simple approach)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text)
        word_freq = Counter(words)
        
        # Filter out common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 
            'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 
            'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let',
            'put', 'say', 'she', 'too', 'use', 'will', 'with', 'have', 'this', 'that',
            'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time', 'very',
            'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such',
            'take', 'than', 'them', 'well', 'were'
        }
        
        # Get top keywords excluding stop words
        top_keywords = [word for word, count in word_freq.most_common(20) 
                       if word not in stop_words and len(word) > 3]
        
        return {
            'top_keywords': top_keywords[:10],
            'total_unique_words': len(word_freq),
            'avg_words_per_page': sum(len(text.split()) for text in all_text) / len(pages) if pages else 0,
            'heading_keywords': [word for word, count in Counter(re.findall(r'\b[a-zA-Z]{3,}\b', combined_headings)).most_common(10)
                               if word not in stop_words]
        }
    def _extract_css_files(self, soup: BeautifulSoup) -> List[str]:
        """Extract CSS files from the page"""
        css_files = []
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if href:
                css_files.append(href)
        return css_files
    
    def _analyze_css_styles(self, css_url: str) -> Dict[str, Any]:
        """Analyze CSS file to extract colors and fonts"""
        try:
            logger.info(f"Analyzing CSS file: {css_url}")
            
            # Fetch CSS content
            response = self.session.get(css_url, timeout=10)
            response.raise_for_status()
            css_content = response.text
            
            # Extract colors
            color_patterns = [
                r'#[0-9a-fA-F]{3,6}',  # Hex colors
                r'rgb\([^)]+\)',  # RGB colors
                r'rgba\([^)]+\)',  # RGBA colors
                r'color:\s*([^;]+)',  # Color properties
                r'background-color:\s*([^;]+)',  # Background colors
                r'border-color:\s*([^;]+)',  # Border colors
            ]
            
            colors = []
            for pattern in color_patterns:
                matches = re.findall(pattern, css_content, re.IGNORECASE)
                colors.extend(matches)
            
            # Extract fonts
            font_patterns = [
                r'font-family:\s*([^;]+)',  # Font family
                r'font:\s*([^;]+)',  # Font shorthand
                r'@import\s+url\([^)]*googleapis[^)]*\)',  # Google Fonts imports
            ]
            
            fonts = []
            for pattern in font_patterns:
                matches = re.findall(pattern, css_content, re.IGNORECASE)
                fonts.extend(matches)
            
            # Clean and deduplicate colors
            clean_colors = []
            for color in colors:
                color = color.strip()
                if color.startswith('#'):
                    clean_colors.append(color)
                elif color.startswith(('rgb', 'rgba')):
                    clean_colors.append(color)
                elif color in ['white', 'black', 'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'grey']:
                    clean_colors.append(color)
            
            # Clean and deduplicate fonts
            clean_fonts = []
            for font in fonts:
                font = font.strip()
                # Extract font names from font-family declarations
                if 'font-family:' in font.lower():
                    font_names = re.findall(r'([a-zA-Z\s]+)(?:,|$)', font)
                    clean_fonts.extend([f.strip() for f in font_names if f.strip()])
                elif 'googleapis' in font.lower():
                    # Extract font names from Google Fonts URLs
                    font_names = re.findall(r'family=([^&]+)', font)
                    clean_fonts.extend([f.replace('+', ' ') for f in font_names])
                else:
                    clean_fonts.append(font)
            
            # Remove duplicates and common fallback fonts
            fallback_fonts = {'arial', 'helvetica', 'sans-serif', 'serif', 'monospace', 'times', 'georgia', 'verdana', 'tahoma', 'trebuchet ms'}
            unique_fonts = list(set([f for f in clean_fonts if f.lower() not in fallback_fonts]))
            
            return {
                'colors': list(set(clean_colors))[:10],  # Limit to top 10 colors
                'fonts': unique_fonts[:5],  # Limit to top 5 fonts
                'css_url': css_url,
                'total_css_size': len(css_content)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing CSS file {css_url}: {str(e)}")
            return {'colors': [], 'fonts': [], 'css_url': css_url, 'total_css_size': 0}
    
    def _perform_seo_analysis(self, pages: List[Dict[str, Any]], meta_tags: Dict[str, str], images: List[Dict[str, str]]) -> Dict[str, Any]:
        """Perform basic SEO analysis"""
        
        seo_issues = []
        seo_strengths = []
        
        # Check for essential meta tags
        if not meta_tags.get('description'):
            seo_issues.append("Missing meta description")
        elif len(meta_tags.get('description', '')) > 160:
            seo_issues.append("Meta description too long (>160 characters)")
        else:
            seo_strengths.append("Meta description present and appropriate length")
        
        # Check title tags
        home_page = next((page for page in pages if page['page_type'] == 'home'), pages[0] if pages else None)
        if home_page:
            title = home_page['title']
            if not title:
                seo_issues.append("Missing page title")
            elif len(title) > 60:
                seo_issues.append("Page title too long (>60 characters)")
            else:
                seo_strengths.append("Page title present and appropriate length")
        
        # Check heading structure
        h1_count = 0
        for page in pages:
            h1_count += len(page['headings'].get('h1', []))
        
        if h1_count == 0:
            seo_issues.append("No H1 tags found")
        elif h1_count > len(pages):
            seo_issues.append("Multiple H1 tags found on some pages")
        else:
            seo_strengths.append("Appropriate H1 tag usage")
        
        # Check images
        images_without_alt = len([img for img in images if not img['has_alt']])
        if images_without_alt > 0:
            seo_issues.append(f"{images_without_alt} images missing alt text")
        else:
            seo_strengths.append("All images have alt text")
        
        # Check for HTTPS
        if any(page['url'].startswith('https://') for page in pages):
            seo_strengths.append("Site uses HTTPS")
        else:
            seo_issues.append("Site not using HTTPS")
        
        return {
            'issues': seo_issues,
            'strengths': seo_strengths,
            'seo_score': max(0, 100 - (len(seo_issues) * 10)),  # Simple scoring
            'recommendations': self._generate_seo_recommendations(seo_issues)
        }
    
    def _generate_seo_recommendations(self, issues: List[str]) -> List[str]:
        """Generate SEO recommendations based on identified issues"""
        recommendations = []
        
        for issue in issues:
            if "meta description" in issue.lower():
                recommendations.append("Add a compelling meta description of 150-160 characters that summarizes the page content")
            elif "title" in issue.lower():
                recommendations.append("Create descriptive, unique titles of 50-60 characters for each page")
            elif "h1" in issue.lower():
                recommendations.append("Use exactly one H1 tag per page that clearly describes the page content")
            elif "alt text" in issue.lower():
                recommendations.append("Add descriptive alt text to all images for better accessibility and SEO")
            elif "https" in issue.lower():
                recommendations.append("Implement HTTPS to improve security and search rankings")
        
        return recommendations
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL format"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def _scrape_page(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape individual page content
        
        Args:
            url: Page URL to scrape
            
        Returns:
            Page data dictionary or None if failed
        """
        try:
            logger.info(f"Scraping page: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract page data
            page_data = {
                'url': url,
                'title': self._extract_title(soup),
                'meta_description': self._extract_meta_description(soup),
                'headings': self._extract_headings(soup),
                'content': self._extract_content(soup),
                'images': self._extract_images(soup, url),
                'links': self._extract_links(soup, url),
                'meta_tags': self._extract_meta_tags(soup),
                'structured_data': self._extract_structured_data(soup),
                'word_count': self._calculate_word_count(soup),
                'page_type': self._identify_page_type(url, soup),
                'soup': soup,  # Keep soup for additional analysis
                'raw_html': response.text # Store raw HTML
            }
            
            return page_data
            
        except Exception as e:
            logger.error(f"Error scraping page {url}: {str(e)}")
            return None