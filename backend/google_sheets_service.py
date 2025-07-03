import re
import pandas as pd
import requests
from typing import Dict, List, Any, Optional, Tuple
import logging
from urllib.parse import urlparse, parse_qs
import json

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Service for Google Sheets integration without authentication"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def extract_sheet_id(self, url: str) -> Optional[str]:
        """Extract Google Sheets ID from various URL formats"""
        try:
            # Handle different Google Sheets URL formats
            patterns = [
                r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Standard format
                r'[?&]id=([a-zA-Z0-9-_]+)',           # Query parameter
                r'/d/([a-zA-Z0-9-_]+)/',              # Direct ID format
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            # If it looks like a direct sheet ID
            if re.match(r'^[a-zA-Z0-9-_]{40,}$', url.strip()):
                return url.strip()
                
            return None
            
        except Exception as e:
            logger.error(f"Error extracting sheet ID: {str(e)}")
            return None
    
    def get_sheet_name_from_url(self, url: str) -> Optional[str]:
        """Extract sheet/tab name from URL if specified"""
        try:
            if '#gid=' in url:
                # Extract gid and try to get sheet name
                gid_match = re.search(r'#gid=(\d+)', url)
                if gid_match:
                    return f"gid_{gid_match.group(1)}"
            
            if '&range=' in url or '?range=' in url:
                range_match = re.search(r'[?&]range=([^&]+)', url)
                if range_match:
                    range_val = range_match.group(1)
                    if '!' in range_val:
                        return range_val.split('!')[0].replace('%20', ' ')
            
            return None  # Use default sheet
            
        except Exception as e:
            logger.error(f"Error extracting sheet name: {str(e)}")
            return None
    
    def get_public_csv_url(self, sheet_id: str, gid: str = "0") -> str:
        """Generate public CSV export URL for Google Sheets"""
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    def get_public_json_url(self, sheet_id: str, sheet_name: str = None) -> str:
        """Generate public JSON export URL for Google Sheets"""
        if sheet_name:
            return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:json&sheet={sheet_name}"
        else:
            return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:json"
    
    def parse_google_json_response(self, json_text: str) -> List[List[Any]]:
        """Parse Google Sheets JSON response format"""
        try:
            # Remove the JavaScript callback wrapper
            json_text = json_text.replace("google.visualization.Query.setResponse(", "").rstrip(");")
            
            data = json.loads(json_text)
            
            if 'table' not in data or 'rows' not in data['table']:
                return []
            
            table = data['table']
            rows = []
            
            # Extract column headers
            if 'cols' in table:
                headers = []
                for col in table['cols']:
                    label = col.get('label', '')
                    if not label:
                        label = col.get('id', f'Column_{len(headers)}')
                    headers.append(label)
                rows.append(headers)
            
            # Extract data rows
            for row in table['rows']:
                row_data = []
                if 'c' in row:
                    for cell in row['c']:
                        if cell is None:
                            row_data.append('')
                        elif 'v' in cell:
                            value = cell['v']
                            # Handle different data types
                            if isinstance(value, str) and value.startswith('Date('):
                                # Handle date format
                                row_data.append(value)
                            else:
                                row_data.append(value)
                        else:
                            row_data.append('')
                rows.append(row_data)
            
            return rows
            
        except Exception as e:
            logger.error(f"Error parsing Google JSON response: {str(e)}")
            return []
    
    def fetch_sheet_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from Google Sheets using public access methods"""
        try:
            # Extract sheet ID and sheet name
            sheet_id = self.extract_sheet_id(url)
            if not sheet_id:
                return {
                    "success": False,
                    "error": "Could not extract sheet ID from URL. Please ensure the sheet is publicly accessible."
                }
            
            sheet_name = self.get_sheet_name_from_url(url)
            
            # Try multiple methods to fetch data
            data = None
            method_used = None
            
            # Method 1: Try CSV export
            try:
                gid = "0"  # Default to first sheet
                if sheet_name and sheet_name.startswith("gid_"):
                    gid = sheet_name.replace("gid_", "")
                
                csv_url = self.get_public_csv_url(sheet_id, gid)
                response = self.session.get(csv_url, timeout=10)
                
                if response.status_code == 200 and 'text/csv' in response.headers.get('content-type', ''):
                    # Parse CSV data
                    from io import StringIO
                    csv_data = StringIO(response.text)
                    df = pd.read_csv(csv_data)
                    
                    # Convert to list format
                    data = [df.columns.tolist()] + df.values.tolist()
                    method_used = "CSV Export"
                    
            except Exception as csv_error:
                logger.warning(f"CSV method failed: {str(csv_error)}")
            
            # Method 2: Try JSON API if CSV failed
            if data is None:
                try:
                    json_url = self.get_public_json_url(sheet_id, sheet_name)
                    response = self.session.get(json_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = self.parse_google_json_response(response.text)
                        if data:
                            method_used = "JSON API"
                            
                except Exception as json_error:
                    logger.warning(f"JSON method failed: {str(json_error)}")
            
            # Method 3: Try alternative CSV with different parameters
            if data is None:
                try:
                    alt_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                    response = self.session.get(alt_csv_url, timeout=10)
                    
                    if response.status_code == 200:
                        from io import StringIO
                        csv_data = StringIO(response.text)
                        df = pd.read_csv(csv_data)
                        
                        data = [df.columns.tolist()] + df.values.tolist()
                        method_used = "Alternative CSV"
                        
                except Exception as alt_error:
                    logger.warning(f"Alternative CSV method failed: {str(alt_error)}")
            
            if data is None:
                return {
                    "success": False,
                    "error": "Could not access the Google Sheet. Please ensure:\n• The sheet is publicly accessible (Anyone with the link can view)\n• The sharing settings allow public access\n• The URL is correct"
                }
            
            # Clean and validate data
            cleaned_data = self.clean_sheet_data(data)
            
            return {
                "success": True,
                "data": cleaned_data,
                "sheet_id": sheet_id,
                "method": method_used,
                "rows": len(cleaned_data) - 1 if cleaned_data else 0,
                "columns": len(cleaned_data[0]) if cleaned_data and cleaned_data[0] else 0,
                "message": f"Successfully loaded Google Sheet with {len(cleaned_data)-1 if cleaned_data else 0} rows"
            }
            
        except Exception as e:
            logger.error(f"Error fetching Google Sheet: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to fetch Google Sheet: {str(e)}"
            }
    
    def clean_sheet_data(self, data: List[List[Any]]) -> List[List[Any]]:
        """Clean and normalize sheet data"""
        if not data:
            return []
        
        try:
            cleaned_data = []
            
            for row_idx, row in enumerate(data):
                cleaned_row = []
                for cell in row:
                    # Handle different data types
                    if pd.isna(cell) or cell is None:
                        cleaned_row.append('')
                    elif isinstance(cell, (int, float)):
                        cleaned_row.append(cell)
                    else:
                        # Convert to string and clean
                        cell_str = str(cell).strip()
                        # Try to convert to number if possible
                        try:
                            if '.' in cell_str or 'e' in cell_str.lower():
                                cleaned_row.append(float(cell_str))
                            else:
                                cleaned_row.append(int(cell_str))
                        except (ValueError, TypeError):
                            cleaned_row.append(cell_str)
                
                # Only add non-empty rows
                if any(str(cell).strip() for cell in cleaned_row):
                    cleaned_data.append(cleaned_row)
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Error cleaning sheet data: {str(e)}")
            return data  # Return original data if cleaning fails
    
    def validate_sheet_url(self, url: str) -> Dict[str, Any]:
        """Validate if the provided URL is a valid Google Sheets URL"""
        try:
            if not url or not isinstance(url, str):
                return {"valid": False, "error": "URL is required"}
            
            # Check if it's a Google Sheets URL
            if "docs.google.com/spreadsheets" not in url and "drive.google.com" not in url:
                return {"valid": False, "error": "Please provide a valid Google Sheets URL"}
            
            # Try to extract sheet ID
            sheet_id = self.extract_sheet_id(url)
            if not sheet_id:
                return {"valid": False, "error": "Could not extract sheet ID from URL"}
            
            return {
                "valid": True,
                "sheet_id": sheet_id,
                "message": "Valid Google Sheets URL"
            }
            
        except Exception as e:
            return {"valid": False, "error": f"URL validation failed: {str(e)}"}
    
    def get_sample_urls(self) -> List[Dict[str, str]]:
        """Get sample Google Sheets URLs for testing"""
        return [
            {
                "name": "Sample Sales Data",
                "url": "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit",
                "description": "Public Google Sheets with sales data for testing"
            },
            {
                "name": "Sample Financial Data", 
                "url": "https://docs.google.com/spreadsheets/d/1mHIWnDvW9cALRMq9OdNfRwjAthCUq8OOWBdiBP5OQPM/edit",
                "description": "Financial analysis data sample"
            }
        ]
    
    def create_sharing_instructions(self) -> Dict[str, Any]:
        """Provide instructions for making Google Sheets accessible"""
        return {
            "title": "How to Share Your Google Sheet",
            "steps": [
                "1. Open your Google Sheet",
                "2. Click the 'Share' button (top right)",
                "3. Click 'Change to anyone with the link'",
                "4. Set permission to 'Viewer'",
                "5. Click 'Copy link'",
                "6. Paste the link in SheetGenie"
            ],
            "tips": [
                "• The sheet must be publicly accessible for SheetGenie to read it",
                "• 'Viewer' permission is sufficient - no editing access needed",
                "• Both full URLs and sheet IDs work",
                "• Specific sheet tabs can be accessed using the tab URL"
            ],
            "troubleshooting": [
                "If access fails, check sharing settings",
                "Ensure the link works in an incognito browser",
                "Try copying the link again from Google Sheets"
            ]
        }