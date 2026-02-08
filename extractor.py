#!/usr/bin/env python3
"""
Wayback URL Extractor
Extract all archived URLs from the Wayback Machine CDX API

Usage:
    python extractor.py example.com
    python extractor.py example.com --format csv --from 2020
"""

import sys
import argparse
import requests
import csv
import json
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse
import time


class WaybackExtractor:
    """Extract URLs from Wayback Machine"""
    
    CDX_API = "http://web.archive.org/cdx/search/cdx"
    FREE_LIMIT = 50000  # Free version limit
    
    def __init__(self, domain):
        self.domain = domain.replace('http://', '').replace('https://', '').strip('/')
        self.urls = []
        self.stats = {
            'total': 0,
            'unique': 0,
            'by_type': Counter(),
            'by_status': Counter()
        }
        
    def extract(self, limit=None, filter_pattern=None, from_year=None, 
                to_year=None, status_codes=None, remove_duplicates=True,
                verbose=False):
        """Extract URLs from Wayback Machine"""
        
        print(f"🔍 Extracting URLs from: {self.domain}")
        print("━" * 50)
        
        if limit is None:
            limit = self.FREE_LIMIT
        elif limit > self.FREE_LIMIT:
            print(f"⚠️ Free version limited to {self.FREE_LIMIT:,} URLs")
            print(f"   Your limit: {limit:,}")
            print(f"   Using: {self.FREE_LIMIT:,}")
            print(f"\n💡 Need more? Contact: https://waybackrevive.com/contact\n")
            limit = self.FREE_LIMIT
        
        print(f"⏳ Fetching up to {limit:,} URLs...")
        if from_year or to_year:
            print(f"📅 Date range: {from_year or 'Start'} to {to_year or 'Present'}")
        if filter_pattern:
            print(f"🔍 Filter: {filter_pattern}")
        if status_codes:
            print(f"📊 Status codes: {status_codes}")
        print()
        
        # Build API parameters
        params = {
            'url': self.domain + '/*',
            'output': 'json',
            'fl': 'original,timestamp,statuscode,mimetype',
            'limit': limit,
            'collapse': 'urlkey'  # Remove duplicates by URL
        }
        
        # Add date filters
        if from_year:
            params['from'] = str(from_year)
        if to_year:
            params['to'] = str(to_year)
        
        # Add filter
        if filter_pattern:
            params['filter'] = f'original:.*{filter_pattern}'
        
        # Add status filter
        if status_codes:
            params['filter'] = f'statuscode:{status_codes}'
        
        try:
            start_time = time.time()
            response = requests.get(self.CDX_API, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            # Skip header row
            if data and len(data) > 1:
                self.urls = data[1:]
                self._calculate_stats()
                
                elapsed = time.time() - start_time
                print(f"✅ Extraction complete in {elapsed:.1f}s")
                print()
                
                return True
            else:
                print("❌ No URLs found matching criteria")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            return False
    
    def _calculate_stats(self):
        """Calculate statistics"""
        self.stats['total'] = len(self.urls)
        
        seen_urls = set()
        for item in self.urls:
            url = item[0]
            status = item[2] if len(item) > 2 else 'unknown'
            mime = item[3] if len(item) > 3 else 'unknown'
            
            seen_urls.add(url)
            self.stats['by_status'][status] += 1
            
            # Categorize by file type
            file_type = self._categorize_mime(mime, url)
            self.stats['by_type'][file_type] += 1
        
        self.stats['unique'] = len(seen_urls)
    
    def _categorize_mime(self, mime, url):
        """Categorize MIME type"""
        if 'html' in mime.lower():
            return 'HTML'
        elif 'image' in mime.lower():
            return 'Image'
        elif 'css' in mime.lower():
            return 'CSS'
        elif 'javascript' in mime.lower() or 'json' in mime.lower():
            return 'JavaScript'
        elif 'pdf' in mime.lower():
            return 'PDF'
        elif 'video' in mime.lower():
            return 'Video'
        elif url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
            return 'Image'
        elif url.endswith(('.css',)):
            return 'CSS'
        elif url.endswith(('.js',)):
            return 'JavaScript'
        elif url.endswith(('.pdf',)):
            return 'PDF'
        else:
            return 'Other'
    
    def print_stats(self):
        """Print extraction statistics"""
        print("📊 Extraction Summary:")
        print("━" * 50)
        print(f"\n📈 URLs:")
        print(f"   Total Extracted: {self.stats['total']:,}")
        print(f"   Unique URLs: {self.stats['unique']:,}")
        
        if self.stats['total'] >= self.FREE_LIMIT:
            print(f"\n⚠️ FREE VERSION LIMIT REACHED")
            print(f"   This domain may have more URLs available.")
            print(f"   Contact us for complete extraction:")
            print(f"   👉 https://waybackrevive.com/contact")
        
        if self.stats['by_type']:
            print(f"\n📁 By File Type:")
            total = self.stats['total']
            for ftype, count in self.stats['by_type'].most_common(5):
                percentage = (count / total * 100) if total > 0 else 0
                print(f"   {ftype:12s}: {count:6,} ({percentage:5.1f}%)")
        
        if self.stats['by_status']:
            print(f"\n📊 By Status Code:")
            for status, count in sorted(self.stats['by_status'].items())[:5]:
                percentage = (count / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
                print(f"   {status:6s}: {count:6,} ({percentage:5.1f}%)")
        
        print()
    
    def export_csv(self, filename=None):
        """Export to CSV"""
        if filename is None:
            filename = f"{self.domain.replace('.', '_')}_urls.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'timestamp', 'status_code', 'mime_type'])
            
            for item in self.urls:
                writer.writerow(item)
        
        print(f"💾 CSV saved to: {filename}")
        return filename
    
    def export_json(self, filename=None):
        """Export to JSON"""
        if filename is None:
            filename = f"{self.domain.replace('.', '_')}_urls.json"
        
        data = {
            'domain': self.domain,
            'extracted_at': datetime.now().isoformat(),
            'stats': {
                'total_urls': self.stats['total'],
                'unique_urls': self.stats['unique']
            },
            'urls': [
                {
                    'url': item[0],
                    'timestamp': item[1],
                    'status_code': item[2] if len(item) > 2 else None,
                    'mime_type': item[3] if len(item) > 3 else None
                }
                for item in self.urls
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 JSON saved to: {filename}")
        return filename
    
    def export_txt(self, filename=None):
        """Export to plain text (URLs only)"""
        if filename is None:
            filename = f"{self.domain.replace('.', '_')}_urls.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.urls:
                f.write(item[0] + '\n')
        
        print(f"💾 TXT saved to: {filename}")
        return filename
    
    def export(self, format='csv', filename=None):
        """Export in specified format"""
        if format == 'csv':
            return self.export_csv(filename)
        elif format == 'json':
            return self.export_json(filename)
        elif format == 'txt':
            return self.export_txt(filename)
        else:
            raise ValueError(f"Unknown format: {format}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Extract archived URLs from the Wayback Machine',
        epilog='Professional services: https://waybackrevive.com'
    )
    
    parser.add_argument('domain', help='Domain to extract URLs from')
    parser.add_argument('--format', choices=['csv', 'json', 'txt'], 
                       default='csv', help='Output format (default: csv)')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--filter', help='Filter pattern (e.g., *.html)')
    parser.add_argument('--from', dest='from_year', type=int, 
                       help='Start year (e.g., 2020)')
    parser.add_argument('--to', dest='to_year', type=int,
                       help='End year (e.g., 2023)')
    parser.add_argument('--status', help='Filter by status codes (e.g., 200,301)')
    parser.add_argument('--limit', type=int, help=f'Max URLs (limit: {WaybackExtractor.FREE_LIMIT:,})')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    print("\n" + "═" * 50)
    print("  📊 WAYBACK URL EXTRACTOR")
    print("  Extract All Archived URLs")
    print("═" * 50 + "\n")
    
    # Initialize extractor
    extractor = WaybackExtractor(args.domain)
    
    # Extract URLs
    success = extractor.extract(
        limit=args.limit,
        filter_pattern=args.filter,
        from_year=args.from_year,
        to_year=args.to_year,
        status_codes=args.status,
        verbose=args.verbose
    )
    
    if success:
        # Print stats
        extractor.print_stats()
        
        # Export
        print("📦 Exporting...")
        extractor.export(format=args.format, filename=args.output)
        
        print("\n" + "━" * 50)
        print("\n✨ Next Steps:")
        print("   1. Review the extracted URLs")
        print("   2. Identify valuable content")
        print("   3. Plan your recovery strategy")
        print("\n💡 Need help recovering the actual content?")
        print("   We can restore your complete website:")
        print("   👉 https://waybackrevive.com/contact")
        print("   📧 hello@waybackrevive.com")
        print("\n" + "━" * 50)
    
    print("\n⭐ If this tool helped you, star us on GitHub!")
    print("🚀 Professional recovery: https://waybackrevive.com\n")


if __name__ == '__main__':
    # Interactive mode if no arguments
    if len(sys.argv) == 1:
        print("\n" + "═" * 50)
        print("  📊 WAYBACK URL EXTRACTOR")
        print("  Extract All Archived URLs")
        print("═" * 50 + "\n")
        
        domain = input("Enter domain to extract URLs from: ").strip()
        
        if domain:
            print("\nOutput format:")
            print("  1. CSV (Excel-friendly)")
            print("  2. JSON (Developer-friendly)")
            print("  3. TXT (Simple list)")
            
            format_choice = input("\nChoose format (1-3, default: 1): ").strip() or "1"
            format_map = {'1': 'csv', '2': 'json', '3': 'txt'}
            output_format = format_map.get(format_choice, 'csv')
            
            extractor = WaybackExtractor(domain)
            
            if extractor.extract():
                extractor.print_stats()
                extractor.export(format=output_format)
                
                print("\n✨ Done! Check the output file.")
                print("💼 Need professional recovery?")
                print("   👉 https://waybackrevive.com/contact")
        
        input("\nPress Enter to exit...")
    else:
        main()
