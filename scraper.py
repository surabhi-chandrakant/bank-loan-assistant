import requests
from bs4 import BeautifulSoup
import time

# Updated URLs provided by you
urls = [
    "https://bankofmaharashtra.bank.in/",
    "https://bankofmaharashtra.bank.in/online-loans",
    "https://bankofmaharashtra.bank.in/home-loan",
    "https://bankofmaharashtra.bank.in/housing-loan",
    "https://bankofmaharashtra.bank.in/maha-super-flexi-housing-loan",
    "https://bankofmaharashtra.bank.in/personal-loans",
    "https://bankofmaharashtra.bank.in/education-loans",
    "https://bankofmaharashtra.bank.in/msme-loans"
]

def extract_meaningful_text(url):
    print(f"Scraping: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        page = requests.get(url, timeout=15, headers=headers)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        # Remove scripts, styles, nav
        for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
            tag.decompose()

        # Extract from main content areas
        main_content = soup.find_all(['main', 'article', 'section', 'div'], class_=lambda x: x and any(
            term in str(x).lower() for term in ['content', 'main', 'article', 'body']
        ))
        
        if not main_content:
            main_content = [soup.body] if soup.body else [soup]

        text_blocks = []
        
        for container in main_content:
            # Get headings for context
            for heading in container.find_all(['h1', 'h2', 'h3', 'h4']):
                text = heading.get_text(separator=" ", strip=True)
                if len(text) > 5:
                    text_blocks.append(f"\n## {text}\n")
            
            # Get paragraphs and list items
            for tag in container.find_all(['p', 'li', 'td', 'div']):
                text = tag.get_text(separator=" ", strip=True)
                # Keep more content - less restrictive filtering
                if len(text) > 20 and len(text) < 1000:
                    # Remove excessive whitespace
                    text = ' '.join(text.split())
                    if text not in text_blocks:  # Avoid exact duplicates
                        text_blocks.append(text)

        return "\n\n".join(text_blocks)
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""


all_text = ""
for url in urls:
    content = extract_meaningful_text(url)
    if content:
        all_text += f"\n\n=== Source: {url} ===\n\n{content}"
    time.sleep(1)  # Be polite to server

with open("data/raw_loans.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"✅ Scraping completed! Total characters: {len(all_text)}")
print(f"📄 Saved to data/raw_loans.txt")