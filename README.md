# 📊 Wayback URL Extractor

> **Extract all archived URLs** from any domain using the Wayback Machine CDX API

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)

## 🎯 What Does This Do?

Extract **every URL** ever archived for any domain:

- 🔗 **Complete URL Inventory** - All pages, posts, categories
- 📄 **Export Formats** - CSV, JSON, TXT
- 🎯 **Smart Filtering** - By file type, date range, status codes
- 📈 **SEO Gold Mine** - Find old content for recovery
- ⚡ **Fast Extraction** - Parallel processing

Perfect for:
- 🔍 **SEO Agencies** - Content audits & recovery
- 📝 **Content Strategists** - Historical content mapping
- 💼 **Business Owners** - Recovering lost pages
- 🎓 **Researchers** - URL dataset creation
- ⚖️ **Legal Teams** - Evidence collection

## 🚀 Quick Start

### For Non-Technical Users

1. **Download** this repository
2. **Double-click** `extractor.py` (or run in terminal)
3. **Enter your domain** when prompted
4. **Get your URLs** in a CSV file!

### For Technical Users

```bash
# Basic extraction
python extractor.py example.com

# With filters
python extractor.py example.com --format csv --filter "*.html"

# Date range
python extractor.py example.com --from 2020 --to 2023
```

## 💻 Installation

```bash
# Clone this repository
git clone https://github.com/waybackrevive/wayback-url-extractor.git
cd wayback-url-extractor

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage Examples

### Basic URL Extraction
```bash
python extractor.py example.com
```

### Filter by File Type
```bash
# Only HTML pages
python extractor.py example.com --filter "*.html"

# Only images
python extractor.py example.com --filter "*.jpg,*.png,*.gif"

# Only PDFs
python extractor.py example.com --filter "*.pdf"
```

### Date Range Extraction
```bash
# From specific year
python extractor.py example.com --from 2020

# Date range
python extractor.py example.com --from 2018 --to 2022
```

### Export Formats
```bash
# CSV (default - best for Excel)
python extractor.py example.com --format csv

# JSON (for developers)
python extractor.py example.com --format json

# Plain text (simple list)
python extractor.py example.com --format txt
```

### Status Code Filtering
```bash
# Only successful pages (200 OK)
python extractor.py example.com --status 200

# Include redirects
python extractor.py example.com --status "200,301,302"
```

## 📊 Output Example

**CSV Output:** (opens in Excel/Google Sheets)
```csv
url,timestamp,status_code,mime_type
http://example.com/,19961231235959,200,text/html
http://example.com/about,19970115120000,200,text/html
http://example.com/contact,19970203093000,200,text/html
```

**Statistics Report:**
```
🔍 Extracting URLs from: example.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Extraction Complete!

📊 Summary:
   Total URLs: 12,456
   Unique URLs: 8,234
   Duplicates: 4,222
   Date Range: 1996-2026
   
📁 File Types:
   HTML:  5,234 (63.5%)
   Images: 2,101 (25.5%)
   CSS:    567 (6.9%)
   JS:     332 (4.1%)
   
💾 Saved to: example_com_urls.csv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ⚠️ Free Version Limitations

This tool is powerful, but the free version has limits:

- ✅ Extract up to **50,000 URLs** per domain
- ✅ Basic filtering and export
- ❌ No bulk domain processing
- ❌ No content recovery
- ❌ No advanced deduplication
- ❌ No automatic content fetching
- ❌ No database reconstruction
- ❌ No broken link fixing

## 🚀 Need Professional Recovery?

**Extracting URLs is just the first step. We can restore everything.**

### Our Professional Services Include:

✨ **Complete Website Restoration**
- Full content recovery (10,000+ pages)
- All assets (images, videos, documents)
- Database reconstruction
- Working contact forms

✨ **SEO-Optimized Migration**
- 301 redirects setup
- Metadata preservation
- Search engine resubmission
- Sitemap regeneration

✨ **Advanced Recovery**
- Dynamic content restoration
- Custom functionality
- E-commerce recovery
- Membership site restoration

### 👉 [Get Professional Help → waybackrevive.com/contact-us](https://waybackrevive.com/contact-us)

**🎯 Perfect for SEO Agencies:**
- White-label services available
- Bulk domain processing
- Priority support
- Custom solutions

📧 Email: support@waybackrevive.com  
💬 Chat: Available on website

---

## 🛠️ Advanced Features

### Command-Line Options

```bash
python extractor.py DOMAIN [OPTIONS]

Options:
  --format FORMAT      Output format: csv, json, txt (default: csv)
  --output FILE        Output filename (auto-generated if not specified)
  --filter PATTERN     Filter by pattern: *.html, *.pdf, etc.
  --from YEAR          Start year (e.g., 2020)
  --to YEAR            End year (e.g., 2023)
  --status CODES       Filter by status codes: 200, 301, etc.
  --limit NUMBER       Max URLs to extract (default: 50000)
  --no-duplicates      Remove duplicate URLs
  --verbose            Show detailed progress
```

### Programmatic Usage

```python
from extractor import WaybackExtractor

# Initialize
extractor = WaybackExtractor('example.com')

# Extract URLs
urls = extractor.extract(
    limit=10000,
    filter_pattern='*.html',
    from_year=2020
)

# Export
extractor.export_csv('output.csv')
```

## 🔧 Technical Details

### API Integration
- Uses Wayback Machine CDX Server API
- Respectful rate limiting
- Automatic retry on failures
- Progress tracking

### Data Processing
- Streaming for memory efficiency
- Duplicate detection
- URL normalization
- Pattern matching

### Privacy & Security
- ✅ No data stored on our servers
- ✅ All processing happens locally
- ✅ Open source & auditable
- ✅ No tracking or analytics

## 📈 Use Cases

### For SEO Agencies
1. **Content Audit** - Find all historical content
2. **Competitor Analysis** - See their old pages
3. **Recovery Planning** - Identify valuable content
4. **Client Reports** - Show archive coverage

### For Business Owners
1. **Lost Content** - Find deleted pages
2. **Historical URLs** - For redirect planning
3. **Archive Inventory** - Know what's saved
4. **Recovery Assessment** - Plan restoration

### For Developers
1. **Data Mining** - Extract URL datasets
2. **Archive Research** - Historical analysis
3. **Automated Workflows** - Bulk processing
4. **Integration** - Use as library

## 🤝 Contributing

We love contributions!

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📜 License

MIT License - Free to use and modify

## ⭐ Support This Project

If this tool saved you hours of work:
- ⭐ **Star this repository**
- 🐦 **Share on social media**
- 💼 **Hire us** for professional recovery

## 🔗 Resources

- [Wayback Machine](https://web.archive.org/)
- [CDX Server API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
- [Our Other Tools](https://tools.waybackrevive.com/)
- [Professional Services](https://waybackrevive.com)

## 💡 Tips & Tricks

### For Large Sites
- Use `--limit` to start small
- Filter by file type first
- Process by year ranges
- Export to JSON for later analysis

### For SEO Work
- Focus on 200 status codes
- Filter for `*.html` pages
- Look for 404s in old archives
- Compare with current sitemap

### For Research
- Export to JSON for analysis
- Use date ranges strategically
- Combine with other datasets
- Consider API rate limits

---

<p align="center">
  <strong>Made with ❤️ by WaybackRevive Team</strong><br>
  <a href="https://waybackrevive.com">waybackrevive.com</a> | 
  <a href="https://github.com/your-username">GitHub</a>
</p>

<p align="center">
  <sub>Need Help? Contact us at support@waybackrevive.com</sub>
</p>
