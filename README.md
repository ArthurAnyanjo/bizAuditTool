# Website Audit & AI Prompt Generator

A comprehensive Streamlit application that performs website audits using Google PageSpeed Insights API, analyzes content with AI-powered insights, and generates detailed AI prompts for website builders.

## 🚀 Features

### Performance Audit Dashboard
- **URL Input & Validation** - Accept and validate website URLs
- **PageSpeed API Integration** - Mobile & Desktop analysis
- **Performance Metrics Visualization** - Core Web Vitals, Performance, SEO, Best Practices, Accessibility scores
- **Opportunity Analysis Dashboard** - Detailed improvement recommendations
- **PDF Report Generation** - Professional reports in multiple formats

### AI-Powered Content Analysis
- **Multi-page Scraping** - Home, About, Contact, Services pages
- **AI-Powered Insights** - Brand identity, target audience, goals, value propositions
- **Content Structure Analysis** - SEO elements, headings, images
- **Industry Analysis** - Market positioning and competitive insights
- **Conversion Strategy** - CTAs, trust elements, user journey optimization

### Enhanced AI Prompt Generation
- **Comprehensive Analysis** - Brand colors, industry, tone, target audience
- **Strategic Recommendations** - Website goals, value propositions, conversion elements
- **Technical Requirements** - Essential features, performance, SEO requirements
- **Design Guidelines** - Visual style, typography, layout specifications
- **Content Strategy** - Key messages, themes, tone of voice

## 🛠️ Technology Stack

### Backend
- **Python 3.9+**
- **Streamlit** - Web framework
- **Requests** - API calls
- **BeautifulSoup4** - Web scraping
- **Pandas** - Data manipulation
- **ReportLab** - PDF generation
- **Plotly** - Data visualization
- **G4F (GPT4Free)** - AI-powered analysis

### APIs & Services
- **Google PageSpeed Insights API**
- **G4F (GPT4Free)** - AI analysis and insights

## 📋 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bizAuditTool
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup G4F for AI analysis (Optional but recommended)**
   ```bash
   python setup_g4f.py
   ```

5. **Set up environment variables**
   Create a `.streamlit/secrets.toml` file:
   ```toml
   PAGESPEED_API_KEY = "your_pagespeed_api_key_here"
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 🔧 Configuration

### API Keys

#### Google PageSpeed Insights API (Required)
- Get your API key from [Google Cloud Console](https://console.cloud.google.com/)
- Enable PageSpeed Insights API
- Add to `.streamlit/secrets.toml`

#### G4F (Optional but Recommended)
- Automatically installed via `setup_g4f.py`
- Provides AI-powered website analysis
- No API key required (uses free AI models)

### Application Settings
Edit `config/settings.py` to customize:
- Maximum pages to scrape
- Request delays
- Cache duration
- Report formats

## 📊 Usage

### 1. Performance Audit
1. Enter website URL
2. Click "Run Performance Audit"
3. View performance metrics and scores
4. Analyze opportunities and diagnostics
5. Generate PDF report

### 2. AI-Powered Content Analysis
1. Navigate to "Content Analysis" tab
2. Run content analysis on scraped data
3. Review AI-generated insights:
   - Brand identity and visual style
   - Industry analysis and market positioning
   - Target audience and demographics
   - Website goals and conversion strategy
   - Value propositions and messaging
   - Content strategy and tone of voice
   - Conversion optimization elements
   - Technical requirements

### 3. AI Prompt Generation
1. Navigate to "AI Prompt Generator" tab
2. Generate comprehensive AI prompt
3. Download prompt for use with AI website builders
4. Get strategic recommendations for website redesign

## 📁 Project Structure

```
bizAuditTool/
├── main.py                      # Main Streamlit app
├── setup_g4f.py                # G4F setup script
├── config/
│   ├── __init__.py
│   ├── settings.py             # API keys and configuration
│   └── constants.py            # Constants and enums
├── modules/
│   ├── __init__.py
│   ├── pagespeed_api.py        # PageSpeed API integration
│   ├── web_scraper.py          # Website scraping
│   ├── report_generator.py     # PDF report generation
│   ├── prompt_generator.py     # AI prompt creation
│   ├── enhanced_data_processor.py # AI-powered analysis
│   └── data_processor.py       # Basic data analysis (legacy)
├── templates/
│   ├── prd_template.md         # PRD template
│   └── report_template.html
├── assets/                     # Static assets
├── data/
│   └── cache/                  # Temporary data storage
├── requirements.txt
└── README.md
```

## 🎯 Key Features

### Performance Audit Dashboard
- Real-time PageSpeed analysis
- Mobile and desktop comparison
- Core Web Vitals tracking
- Opportunity and diagnostic insights
- Interactive performance charts

### AI-Powered Content Analysis
- Multi-page website scraping
- Brand identity analysis
- Industry and market positioning
- Target audience profiling
- Value proposition identification
- Conversion strategy optimization
- Technical requirements analysis

### Enhanced AI Prompt Generation
- Comprehensive website analysis
- Brand identity and visual style
- Target audience and demographics
- Website goals and conversion strategy
- Value propositions and messaging
- Content strategy and tone
- Technical requirements and features
- Strategic recommendations

## 📈 Success Metrics

- **Performance**: 90+ PageSpeed score
- **SEO**: 95+ SEO score
- **Accessibility**: 90+ accessibility score
- **Best Practices**: 90+ best practices score
- **Conversion**: Optimized for lead generation
- **User Experience**: High engagement metrics
- **AI Analysis**: Comprehensive insights for redesign

## 🔄 Workflow

1. **Input URL** → Website validation
2. **Performance Audit** → PageSpeed analysis
3. **AI Content Analysis** → Multi-page scraping + AI insights
4. **Enhanced Data Processing** → Comprehensive analysis
5. **Report Generation** → PDF/HTML reports
6. **AI Prompt Creation** → Strategic recommendations
7. **Website Builder Ready** → Ready for AI website builders

## 🚀 Deployment

### Local Development
```bash
streamlit run main.py
```

### Production Deployment
1. Set up environment variables
2. Configure API keys
3. Install G4F for AI analysis
4. Deploy to Streamlit Cloud or similar platform
5. Set up monitoring and logging

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

## 🔮 Future Enhancements

- [ ] Competitor analysis integration
- [ ] Advanced AI-powered recommendations
- [ ] Real-time monitoring dashboard
- [ ] Automated report scheduling
- [ ] Integration with popular CMS platforms
- [ ] Advanced analytics and tracking
- [ ] Multi-language support
- [ ] Advanced AI model integration 