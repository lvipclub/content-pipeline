"""
dify_asin_checker.py — Check Dify knowledge base books against Amazon
======================================================================
For each book in the Dify KB (dataset 51610c8d-...):
  1. Skip if it already has an ASIN in Dify metadata
  2. Search Amazon for the book title + author
  3. Extract the 10-digit ASIN
  4. Update Dify document metadata with ASIN
  5. Generate hyperlinks with affiliate tag=xinca-20

Usage: python dify_asin_checker.py
"""

import os
import sys
import requests
import re
import json
import time
from pathlib import Path

# --- CONFIG ---
DIFY_DATASET_KEY = "dataset-PC1cMX9XVkD9q2eZb9VTNTeQ"
DATASET_ID = "51610c8d-79c7-41fb-bb7e-1af3b120a850"
DIFY_API_BASE = "https://api.dify.ai/v1"
AFFILIATE_TAG = "xinca-20"
HEADERS = {"Authorization": f"Bearer {DIFY_DATASET_KEY}", "Content-Type": "application/json"}

# Cache of already-checked ASINs (avoid duplicate Amazon searches)
CHECKED_CACHE = set()
SKIP_WORDS = ["standard", "guide", "commissioning", "faq", "what-is", "ddc", "ansI", "bsi",
              "bsr", "acgih", "cibse", "femp", "all", "practice", "questions"]


def get_dify_documents():
    """Fetch all documents from Dify KB."""
    docs = []
    page = 1
    while True:
        resp = requests.get(
            f"{DIFY_API_BASE}/datasets/{DATASET_ID}/documents",
            headers=HEADERS,
            params={"limit": 50, "page": page}
        )
        if resp.status_code != 200:
            print(f"  ❌ Dify API error: {resp.status_code}")
            break
        data = resp.json()
        batch = data.get("data", [])
        if not batch:
            break
        docs.extend(batch)
        if len(batch) < 50:
            break
        page += 1
        time.sleep(0.3)
    return docs


def get_document_metadata(doc_id):
    """Get document metadata including custom fields."""
    try:
        resp = requests.get(
            f"{DIFY_API_BASE}/datasets/{DATASET_ID}/documents/{doc_id}",
            headers=HEADERS
        )
        if resp.status_code == 200:
            return resp.json().get("doc_metadata", {}) or {}
    except:
        pass
    return {}


def update_document_metadata(doc_id, metadata):
    """Update document metadata in Dify."""
    try:
        resp = requests.post(
            f"{DIFY_API_BASE}/datasets/{DATASET_ID}/documents/{doc_id}/metadata",
            headers=HEADERS,
            json={"doc_metadata": metadata}
        )
        if resp.status_code == 200:
            return True
        print(f"  ⚠️ Metadata update failed: {resp.status_code} — {resp.text[:100]}")
    except Exception as e:
        print(f"  ⚠️ Metadata update error: {e}")
    return False


def search_amazon_asin(title, author=""):
    """Search Amazon for a book and extract ASIN."""
    # Try multiple search strategies
    queries = [
        f"{title} {author} book",
        f"{title} book",
    ]
    if author:
        queries.insert(0, f"{title} {author}")

    for query in queries[:2]:
        # Use DuckDuckGo to search Amazon
        search_url = f"https://www.amazon.com/s?k={requests.utils.quote(query)}"
        try:
            resp = requests.get(
                search_url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; XINCABot/1.0; +https://ai.xinca.com)"},
                timeout=15,
                allow_redirects=True
            )
            # Extract ASINs from product links
            # Pattern: /dp/XXXXXXXXXX or /gp/product/XXXXXXXXXX
            asin_pattern = r'/dp/([0-9A-Z]{10})'
            matches = re.findall(asin_pattern, resp.text)
            if matches:
                asin = matches[0]
                # Verify it looks like a real ASIN
                if len(asin) == 10 and asin not in CHECKED_CACHE:
                    CHECKED_CACHE.add(asin)
                    # Quick verification — check item exists
                    verify_url = f"https://www.amazon.com/dp/{asin}"
                    try:
                        vresp = requests.get(verify_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                        if vresp.status_code == 200 and "productTitle" in vresp.text:
                            return asin, f"{title} by {author}" if author else title
                    except:
                        pass
        except Exception as e:
            print(f"  ⚠️ Search failed for '{query}': {e}")
            time.sleep(1)
    return None, None


def extract_title_author(doc_name):
    """Extract clean title and author from Dify document name."""
    # Remove file extension
    name = doc_name.rsplit(".", 1)[0]

    # Try to identify patterns like "Title Year Author.pdf"
    # Common: "Making Your Data Center Energy Efficient 2011 Gilbert Held"
    author_patterns = [
        r"(\d{4})\s+(.+?)$",      # Title... Year Author
        r"by\s+(.+?)$",            # Title by Author
    ]

    author = ""
    title = name

    for pattern in author_patterns:
        m = re.search(pattern, name)
        if m:
            year = m.group(1) if "(" not in pattern else ""
            author = m.group(2) if "by" not in pattern else m.group(1)
            # Remove year and author from title
            title = name[:m.start()].strip().rstrip("0123456789 ").strip()
            break

    # If no author found, try splitting on common delimiters
    if not author:
        parts = re.split(r'\s+\d{4}\s+', name, maxsplit=1)
        if len(parts) == 2:
            title = parts[0].strip()
            author = parts[1].strip()

    return title, author


def should_skip(doc_name):
    """Skip if filename contains standard/document keywords that aren't books."""
    name_lower = doc_name.lower()
    for word in SKIP_WORDS:
        if word in name_lower:
            return True
    # Also skip if it's an .epub that's not clearly a book
    if name_lower.endswith(".epub"):
        return False  # EPUBs are books
    # Skip markdown files
    if name_lower.endswith(".md"):
        return True
    return False


def main():
    print("📚 Dify Book ASIN Checker")
    print(f"   Dataset: {DATASET_ID}")
    print(f"   Affiliate: {AFFILIATE_TAG}")
    print()

    docs = get_dify_documents()
    print(f"📋 Total documents in Dify: {len(docs)}")
    print()

    checked = 0
    skipped = 0
    found = 0
    updated = 0

    for doc in docs:
        doc_id = doc.get("id", "")
        doc_name = doc.get("name", "")
        indexing_status = doc.get("indexing_status", "")

        # Only process completed documents
        if indexing_status != "completed":
            continue

        # Skip non-books
        if should_skip(doc_name):
            continue

        checked += 1
        print(f"📖 [{checked}] {doc_name}")

        # Check existing metadata for ASIN
        meta = get_document_metadata(doc_id)
        existing_asin = meta.get("asin", "") or meta.get("ASIN", "")
        if existing_asin:
            print(f"  ⏭️ Already has ASIN: {existing_asin}")
            skipped += 1
            continue

        # Extract title and author
        title, author = extract_title_author(doc_name)
        print(f"  Title: {title[:60]}")
        if author:
            print(f"  Author: {author[:40]}")

        # Search Amazon
        asin, matched_title = search_amazon_asin(title, author)
        if asin:
            print(f"  ✅ ASIN found: {asin}")
            print(f"     Affiliate link: https://www.amazon.com/dp/{asin}?tag={AFFILIATE_TAG}")

            # Update Dify metadata
            new_meta = dict(meta)
            new_meta["asin"] = asin
            new_meta["amazon_url"] = f"https://www.amazon.com/dp/{asin}?tag={AFFILIATE_TAG}"

            if update_document_metadata(doc_id, new_meta):
                print(f"  📝 Metadata updated in Dify")
                updated += 1
            found += 1
        else:
            print(f"  ❌ ASIN not found on Amazon")

        time.sleep(1.5)  # Rate limit

    print()
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   Books checked: {checked}")
    print(f"   Already had ASIN: {skipped}")
    print(f"   New ASINs found: {found}")
    print(f"   Dify metadata updated: {updated}")
    print("=" * 50)


if __name__ == "__main__":
    main()
