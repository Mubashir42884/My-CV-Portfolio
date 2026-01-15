import json
import time
import random
import os
from scholarly import scholarly, ProxyGenerator
from difflib import SequenceMatcher

# Your Google Scholar ID
AUTHOR_ID = 'L6Esq54AAAAJ'

def setup_scholarly():
    """Configure scholarly with proxy support for better reliability"""
    try:
        pg = ProxyGenerator()
        # Try to use free proxies to avoid rate limiting
        success = pg.FreeProxies()
        if success:
            scholarly.use_proxy(pg)
            print("✓ Using proxy for requests")
            return True
    except Exception as e:
        print(f"⚠ Could not set up proxy: {e}")
    return False

def capitalize_title(title):
    """Capitalize the first letter of each word in the title"""
    return title.title()

def similarity_ratio(str1, str2):
    """Calculate similarity between two strings (0 to 1)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def is_duplicate(new_pub, existing_pubs, similarity_threshold=0.85):
    """
    Check if a publication is a duplicate based on title and journal similarity
    Returns True if it's a duplicate, False otherwise
    """
    for existing in existing_pubs:
        # Calculate title similarity
        title_similarity = similarity_ratio(new_pub['title'], existing['title'])
        
        # Calculate journal similarity
        journal_similarity = similarity_ratio(new_pub['journal'], existing['journal'])
        
        # Check if authors are similar (at least one common author)
        new_authors_lower = new_pub['authors'].lower()
        existing_authors_lower = existing['authors'].lower()
        
        # Extract individual author names (split by 'and' or ',')
        import re
        new_author_list = re.split(r',|\sand\s', new_authors_lower)
        existing_author_list = re.split(r',|\sand\s', existing_authors_lower)
        
        # Clean up author names
        new_author_list = [a.strip() for a in new_author_list if a.strip()]
        existing_author_list = [a.strip() for a in existing_author_list if a.strip()]
        
        # Check for common authors
        common_authors = any(
            similarity_ratio(new_auth, exist_auth) > 0.8 
            for new_auth in new_author_list 
            for exist_auth in existing_author_list
        )
        
        # Duplicate detection logic:
        # 1. If titles are very similar (>85%) and authors overlap = duplicate
        # 2. If title appears in journal name or vice versa = likely duplicate entry error
        if title_similarity > similarity_threshold and common_authors:
            print(f"  → Duplicate detected (similar titles): '{new_pub['title'][:50]}...'")
            return True
        
        # Special case: Sometimes Scholar creates entries where title = journal name
        if (similarity_ratio(new_pub['title'], existing['journal']) > 0.85 or
            similarity_ratio(new_pub['journal'], existing['title']) > 0.85):
            print(f"  → Duplicate detected (title/journal mismatch): '{new_pub['title'][:50]}...'")
            return True
        
        # If journals are the same and titles are moderately similar (>70%)
        if journal_similarity > 0.85 and title_similarity > 0.70 and common_authors:
            print(f"  → Duplicate detected (same journal + similar title): '{new_pub['title'][:50]}...'")
            return True
    
    return False

def fetch_with_retry(func, max_retries=3, base_delay=5):
    """Retry a function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = base_delay * (2 ** attempt) + random.uniform(1, 3)
                print(f"  Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
            else:
                # Small random delay even on first attempt
                time.sleep(random.uniform(1, 2))
            
            return func()
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {str(e)[:100]}")
            if attempt == max_retries - 1:
                raise
    return None

def fetch_publications():
    print(f"Fetching data for Author ID: {AUTHOR_ID}...")
    
    # Set up proxy if possible
    setup_scholarly()
    
    # Determine output path (works both locally and in GitHub Actions)
    if os.path.exists('../public'):
        output_path = '../public/scholar.json'
    elif os.path.exists('public'):
        output_path = 'public/scholar.json'
    else:
        output_path = 'scholar.json'
    
    try:
        # Search for the author with retry
        print("Searching for author profile...")
        author = fetch_with_retry(lambda: scholarly.search_author_id(AUTHOR_ID))
        
        if not author:
            raise Exception("Could not find author profile")
        
        # Small delay before filling
        time.sleep(random.uniform(2, 4))
        
        # Fill the author object with publications
        print("Fetching publications list...")
        author = fetch_with_retry(
            lambda: scholarly.fill(author, sections=['publications']),
            max_retries=3,
            base_delay=10
        )
        
        if not author:
            raise Exception("Could not fetch publications")
        
        cleaned_pubs = []
        
        # Sort publications by year (newest first)
        pubs = author['publications']
        pubs.sort(key=lambda x: x['bib'].get('pub_year', '0'), reverse=True)

        print(f"Processing {len(pubs)} publications...")

        for idx, pub in enumerate(pubs):
            # Add delay between publications to avoid rate limiting
            if idx > 0:
                delay = random.uniform(2, 4)
                time.sleep(delay)
            
            print(f"\n[{idx + 1}/{len(pubs)}] Processing publication...")
            
            # Fill publication details with retry
            try:
                filled_pub = fetch_with_retry(
                    lambda: scholarly.fill(pub),
                    max_retries=2,
                    base_delay=5
                )
                if not filled_pub:
                    filled_pub = pub
            except Exception as e:
                print(f"  ⚠ Could not fill complete details: {str(e)[:80]}")
                filled_pub = pub
            
            bib = filled_pub.get('bib', {})
            
            # Extract authors - try multiple possible fields
            authors = 'Unknown Author'
            if 'author' in bib:
                # If author is a string, use it directly
                if isinstance(bib['author'], str):
                    authors = bib['author']
                # If author is a list, join the names
                elif isinstance(bib['author'], list):
                    authors = ', '.join(bib['author'])
            
            # Extract journal/venue - try multiple possible fields
            journal = 'Preprint/Unknown'
            if 'journal' in bib:
                journal = bib['journal']
            elif 'venue' in bib:
                journal = bib['venue']
            elif 'citation' in bib:
                # Sometimes the full citation contains venue info
                citation = bib['citation']
                # Try to extract journal from citation
                if ',' in citation:
                    parts = citation.split(',')
                    if len(parts) > 1:
                        journal = parts[1].strip()
            elif 'publisher' in bib:
                journal = bib['publisher']
            
            # Clean up journal name if it contains page numbers or years
            if journal and journal != 'Preprint/Unknown':
                # Remove common patterns like page numbers at the end
                import re
                journal = re.sub(r',\s*\d+-\d+$', '', journal)
                journal = re.sub(r',\s*\d+$', '', journal)
            
            # Extract year
            year = bib.get('pub_year', 'n.d.')
            
            # Get citation count
            citations = filled_pub.get('num_citations', 0)
            
            # Generate link
            pub_id = filled_pub.get('author_pub_id', '')
            if pub_id:
                link = f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={AUTHOR_ID}&citation_for_view={pub_id}"
            else:
                link = f"https://scholar.google.com/citations?user={AUTHOR_ID}"
            
            # Capitalize title
            title = capitalize_title(bib.get('title', 'Untitled'))
            
            # Create entry (with your custom citation adjustment)
            if title == "Data Privacy Preservation With Federated Learning: A Systematic Review":
                entry = {
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "year": str(year),
                    "citations": citations + 1,
                    "link": link
                }
            else:
                entry = {
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "year": str(year),
                    "citations": citations,
                    "link": link
                }

            # Check for duplicates before adding
            if not is_duplicate(entry, cleaned_pubs):
                cleaned_pubs.append(entry)
                print(f"  ✓ Added: {title[:60]}...")
            
        # Save to the public folder where Next.js can read it
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_pubs, f, indent=2, ensure_ascii=False)
            
        print(f"\n{'='*60}")
        print(f"✓ Successfully scraped {len(cleaned_pubs)} unique publications.")
        print(f"✓ Data saved to {output_path}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ Error occurred: {e}")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        
        # Try to preserve existing data if fetch fails
        try:
            with open(output_path, 'r') as f:
                existing_data = json.load(f)
                if existing_data:
                    print(f"\n⚠ Keeping existing data ({len(existing_data)} publications)")
                    print("The workflow will continue without failing.")
                    exit(0)  # Exit successfully to avoid breaking the workflow
        except FileNotFoundError:
            print("\n✗ No existing data found to preserve.")
        except Exception as preserve_error:
            print(f"\n✗ Could not read existing data: {preserve_error}")
        
        exit(1)

if __name__ == "__main__":
    fetch_publications()