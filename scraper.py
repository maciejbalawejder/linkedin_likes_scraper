import requests
from bs4 import BeautifulSoup
import re

def extract_reactions_count(html_content: str):
    """
    Extract the reactions count from the specified span element using regex.

    Args:
        html_content (str): HTML content to parse

    Returns:
        Optional[str]: Extracted value if found, None otherwise
    """
    try:
        # Updated pattern to match the new HTML structure
        pattern = r'<span[^>]*data-test-id="social-actions__reaction-count"[^>]*>\s*(\d+)\s*</span>'
        match = re.search(pattern, html_content)

        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return None

def get_linkedin_post_likes(url):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Send a GET request to the LinkedIn post URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            reactions_count = extract_reactions_count(response.text)
            return("Number of reactions: " + reactions_count)        
        else:
            return f"Failed to retrieve page. Status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Error: {str(e)}"


# Example usage
#url = "https://www.linkedin.com/posts/wojtek-kuberski_detect-drift-then-retrain-your-model-this-activity-7273289995635871744-3SQW/?utm_source=share&utm_medium=member_desktop"

url = "https://www.linkedin.com/posts/hakimelakhrass_the-most-popular-univariate-drift-detection-activity-7274394112236101632-ItjZ/?utm_source=share&utm_medium=member_desktop"
print(get_linkedin_post_likes(url))
