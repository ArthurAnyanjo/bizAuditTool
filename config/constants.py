from enum import Enum
from typing import Dict, List

class DeviceType(Enum):
    """Device types for analysis"""
    MOBILE = "mobile"
    DESKTOP = "desktop"

class ReportFormat(Enum):
    """Report output formats"""
    PDF = "pdf"
    HTML = "html"
    JSON = "json"

class ScoreCategory(Enum):
    """Score categories for analysis"""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"

class PriorityLevel(Enum):
    """Priority levels for recommendations"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Score thresholds
SCORE_THRESHOLDS = {
    ScoreCategory.EXCELLENT: 90,
    ScoreCategory.GOOD: 70,
    ScoreCategory.NEEDS_IMPROVEMENT: 50,
    ScoreCategory.POOR: 0
}

# Color schemes for different score levels
SCORE_COLORS = {
    ScoreCategory.EXCELLENT: "#22c55e",  # Green
    ScoreCategory.GOOD: "#eab308",        # Yellow
    ScoreCategory.NEEDS_IMPROVEMENT: "#f97316",  # Orange
    ScoreCategory.POOR: "#ef4444"         # Red
}

# Core Web Vitals thresholds
CORE_WEB_VITALS_THRESHOLDS = {
    'largest_contentful_paint': {
        'good': 2500,
        'needs_improvement': 4000,
        'poor': float('inf')
    },
    'first_input_delay': {
        'good': 100,
        'needs_improvement': 300,
        'poor': float('inf')
    },
    'cumulative_layout_shift': {
        'good': 0.1,
        'needs_improvement': 0.25,
        'poor': float('inf')
    }
}

# Common page types for scraping
PAGE_TYPES = [
    'home', 'about', 'contact', 'services', 'products',
    'team', 'careers', 'blog', 'news', 'pricing', 'features',
    'portfolio', 'testimonials', 'faq', 'privacy', 'terms'
]

# SEO elements to analyze
SEO_ELEMENTS = [
    'title', 'meta_description', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'img', 'a', 'canonical', 'robots', 'viewport', 'charset',
    'og_tags', 'twitter_cards', 'schema_markup'
]

# Brand archetypes for PRD generation
BRAND_ARCHETYPES = {
    'innovator': {
        'keywords': ['innovative', 'cutting-edge', 'technology', 'future', 'advanced'],
        'colors': ['blue', 'purple', 'black'],
        'tone': 'Forward-thinking and innovative'
    },
    'caregiver': {
        'keywords': ['caring', 'supportive', 'helpful', 'nurturing', 'compassionate'],
        'colors': ['green', 'blue', 'pink'],
        'tone': 'Warm and supportive'
    },
    'creator': {
        'keywords': ['creative', 'artistic', 'imaginative', 'original', 'expressive'],
        'colors': ['purple', 'orange', 'pink'],
        'tone': 'Creative and inspiring'
    },
    'explorer': {
        'keywords': ['adventurous', 'bold', 'discovery', 'freedom', 'exploration'],
        'colors': ['orange', 'green', 'brown'],
        'tone': 'Adventurous and bold'
    },
    'sage': {
        'keywords': ['wise', 'knowledgeable', 'expert', 'authoritative', 'educational'],
        'colors': ['blue', 'gray', 'navy'],
        'tone': 'Authoritative and trustworthy'
    },
    'hero': {
        'keywords': ['courageous', 'determined', 'confident', 'strong', 'leadership'],
        'colors': ['red', 'black', 'gold'],
        'tone': 'Confident and powerful'
    },
    'innocent': {
        'keywords': ['pure', 'simple', 'honest', 'trustworthy', 'optimistic'],
        'colors': ['white', 'light_blue', 'pink'],
        'tone': 'Pure and trustworthy'
    },
    'magician': {
        'keywords': ['transformative', 'mysterious', 'powerful', 'visionary', 'inspiring'],
        'colors': ['purple', 'black', 'silver'],
        'tone': 'Transformative and inspiring'
    }
}

# Industry themes for analysis
INDUSTRY_THEMES = {
    'technology': {
        'keywords': ['innovation', 'digital', 'software', 'tech', 'automation'],
        'target_audience': 'Tech-savvy professionals and businesses',
        'pain_points': ['Complex technical challenges', 'Need for scalable solutions']
    },
    'healthcare': {
        'keywords': ['health', 'medical', 'wellness', 'care', 'treatment'],
        'target_audience': 'Healthcare professionals and patients',
        'pain_points': ['Access to quality care', 'Complex medical information']
    },
    'finance': {
        'keywords': ['financial', 'investment', 'security', 'wealth', 'planning'],
        'target_audience': 'Financial professionals and investors',
        'pain_points': ['Financial security', 'Complex investment decisions']
    },
    'education': {
        'keywords': ['learning', 'knowledge', 'training', 'development', 'growth'],
        'target_audience': 'Students and professionals seeking education',
        'pain_points': ['Access to quality education', 'Skill development needs']
    },
    'retail': {
        'keywords': ['shopping', 'products', 'convenience', 'quality', 'service'],
        'target_audience': 'Online shoppers and retail customers',
        'pain_points': ['Finding quality products', 'Convenient shopping experience']
    },
    'consulting': {
        'keywords': ['expertise', 'strategy', 'solutions', 'professional', 'advice'],
        'target_audience': 'Businesses seeking expert guidance',
        'pain_points': ['Complex business challenges', 'Need for expert advice']
    }
}

# Report sections
REPORT_SECTIONS = [
    'executive_summary',
    'performance_analysis',
    'seo_analysis',
    'content_analysis',
    'technical_analysis',
    'recommendations',
    'implementation_roadmap'
]

# PRD sections
PRD_SECTIONS = [
    'executive_summary',
    'current_state_analysis',
    'brand_identity',
    'target_audience',
    'strategic_goals',
    'design_specifications',
    'technical_requirements',
    'content_strategy',
    'seo_strategy',
    'implementation_roadmap',
    'success_metrics'
]

# Error messages
ERROR_MESSAGES = {
    'invalid_url': 'Please enter a valid URL starting with http:// or https://',
    'api_error': 'Error connecting to PageSpeed API. Please try again.',
    'scraping_error': 'Error scraping website. Please check the URL and try again.',
    'report_generation_error': 'Error generating report. Please try again.',
    'prd_generation_error': 'Error generating PRD. Please try again.'
}

# Success messages
SUCCESS_MESSAGES = {
    'audit_completed': 'SEO audit completed successfully!',
    'report_generated': 'Report generated successfully!',
    'prd_generated': 'PRD generated successfully!',
    'analysis_completed': 'Content analysis completed successfully!'
} 