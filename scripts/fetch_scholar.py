import json
from scholarly import scholarly
from difflib import SequenceMatcher

# Your Google Scholar ID
AUTHOR_ID = 'L6Esq54AAAAJ'

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

def fetch_publications():
    print(f"Fetching data for Author ID: {AUTHOR_ID}...")
    
    try:
        # Search for the author
        author = scholarly.search_author_id(AUTHOR_ID)
        # Fill the author object with sections (publications, etc.)
        author = scholarly.fill(author, sections=['publications'])
        
        cleaned_pubs = []
        
        # Sort publications by year (newest first)
        pubs = author['publications']
        pubs.sort(key=lambda x: x['bib'].get('pub_year', '0'), reverse=True)

        for pub in pubs:
            # Fill publication details to get complete information
            try:
                filled_pub = scholarly.fill(pub)
            except:
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
            
            # Create entry
            if title=="Data Privacy Preservation With Federated Learning: A Systematic Review":
                entry = {
                "title": title,
                "authors": authors,
                "journal": journal,
                "year": str(year),
                "citations": citations+1,
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
                print(f"✓ Added: {title[:60]}...")
            
        # Save to the public folder where Next.js can read it
        with open('../public/scholar.json', 'w', encoding='utf-8') as f:
            json.dump(cleaned_pubs, f, indent=2, ensure_ascii=False)
            
        print(f"\n✓ Successfully scraped {len(cleaned_pubs)} unique publications.")
        print(f"✓ Data saved to public/scholar.json")

    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    fetch_publications()