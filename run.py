import pandas as pd
import requests
from urllib.parse import urlparse
import os
import time
import re
from tqdm import tqdm

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_html_content(url: str, timeout: int = 10) -> str:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def extract_reactions_count(html_content: str) -> str:
    try:
        pattern = r'<span[^>]*data-test-id="social-actions__reaction-count"[^>]*>\s*(\d+)\s*</span>'
        match = re.search(pattern, html_content)
        
        if match:
            return match.group(1).strip()
                
        return None
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return None

def process_csv_urls(csv_path: str, url_column: str = 'URL', delay: float = 1.0, min_likes: int = 10):
    """
    Process URLs from a CSV file and save their HTML content.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Get the directory and filename from the input path
    directory = os.path.dirname(csv_path) or '.'
    base_filename = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_filename)[0]
    
    # Create output filenames
    output_csv = os.path.join(directory, f'filtered_{base_filename}')
    
    results = []
    
    try:
        df = pd.read_csv(csv_path)
        
        if url_column not in df.columns:
            raise ValueError(f"Column '{url_column}' not found in CSV file")
        
        print(f"Processing {len(df)} rows...")
        
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing URLs", unit="url", ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            url = str(row[url_column]).strip()
            
            if not validate_url(url):
                print(f"Skipping invalid URL at row {index + 1}: {url}")
                continue
            
            # print(f"\nProcessing URL {index + 1}: {url}")
            html_content = get_html_content(url)
            
            if html_content:
                reactions_count = extract_reactions_count(html_content)

                if reactions_count == None:
                    reactions_count = 0
                else:
                    reactions_count = int(reactions_count)

                if reactions_count > min_likes:
                    results.append({
                        'url': url,
                        'reactions_count': reactions_count
                    })
                # print(f"Reactions count: {reactions_count}")
            
            time.sleep(delay)
        
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_csv, index=False)
        print(f"\nProcessing complete! Results saved to {output_csv}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process URLs from CSV and save HTML content')
    parser.add_argument('csv_path', help='Path to the CSV file')
    parser.add_argument('--url-column', default='URL', help='Name of URL column (default: URL)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--min_likes', type=int, default=10, help='Minimum number of likes that the post needs to have to be saved. (default: 10)')
    
    args = parser.parse_args()
    process_csv_urls(args.csv_path, args.url_column, args.delay)
