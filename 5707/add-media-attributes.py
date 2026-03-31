#!/usr/bin/env python3
"""
Add data attributes to media cards in media-index.html for filtering and sorting.

This script:
1. Reads the minified media-index.html
2. Extracts file path from each <a href> attribute
3. Adds data-type, data-folders, and data-filename attributes to <article> tags
4. Writes the updated HTML back (keeping minified format)
5. Reports statistics on files processed
"""

import re
import os
from pathlib import Path

def get_file_type(file_path):
    """Determine media type from file extension."""
    ext = Path(file_path).suffix.lower()

    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
        return 'image'
    elif ext == '.pdf':
        return 'pdf'
    elif ext in ['.md', '.txt', '.json']:
        return 'document'
    elif ext in ['.html', '.htm']:
        return 'raw-html'
    else:
        return 'document'  # Default to document for unknown types

def extract_folders(file_path):
    """Extract folder hierarchy from media path.

    Example: media/images/history/skinner-family/timothy-warner-skinner/file.jpg
    Returns: images|history|skinner-family|timothy-warner-skinner
    """
    # Remove 'media/' prefix and filename
    path_parts = file_path.replace('\\', '/').split('/')

    # Remove 'media' and filename
    if path_parts[0] == 'media':
        path_parts = path_parts[1:]

    # Remove filename (last part)
    if path_parts:
        path_parts = path_parts[:-1]

    # Join with pipe delimiter
    return '|'.join(path_parts) if path_parts else 'root'

def extract_filename(file_path):
    """Extract filename without extension and normalize to lowercase."""
    filename = Path(file_path).stem  # Remove extension
    return filename.lower()

def process_media_index():
    """Process media-index.html and add data attributes."""

    html_path = Path('media-index.html')

    if not html_path.exists():
        print("Error: media-index.html not found")
        return False

    # Read the minified HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Pattern to find article cards with href
    # <article class="card media-card"><a href="..."><img src="...">...
    pattern = r'<article class="card media-card"><a href="([^"]+)">'

    matches = list(re.finditer(pattern, html_content))
    print(f"Found {len(matches)} media cards")

    # Track statistics
    stats = {
        'image': 0,
        'pdf': 0,
        'document': 0,
        'raw-html': 0,
    }

    folders_set = set()

    # Process each match in reverse order to maintain correct positions
    # when we insert data attributes
    for match in reversed(matches):
        file_path = match.group(1)

        # Determine file type
        file_type = get_file_type(file_path)
        stats[file_type] += 1

        # Extract folders and filename
        folders = extract_folders(file_path)
        filename = extract_filename(file_path)

        folders_set.add(folders.split('|')[0])  # Track top-level folders

        # Create the data attributes
        data_attrs = (
            f' data-type="{file_type}"'
            f' data-folders="{folders}"'
            f' data-filename="{filename}"'
        )

        # Find the exact position to insert attributes
        # They should go at the end of the <article> tag, before the closing >
        article_start = match.start()
        article_tag_end = html_content.find('>', article_start) + 1

        # Insert attributes before the closing >
        insert_pos = article_tag_end - 1  # Before the >
        html_content = (
            html_content[:insert_pos] +
            data_attrs +
            html_content[insert_pos:]
        )

    # Write the updated HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Print statistics
    print("\n=== Processing Complete ===")
    print(f"Total cards processed: {len(matches)}")
    print(f"  Images: {stats['image']}")
    print(f"  PDFs: {stats['pdf']}")
    print(f"  Documents: {stats['document']}")
    print(f"  Raw HTML: {stats['raw-html']}")
    print(f"\nTop-level folders found: {sorted(folders_set)}")
    print(f"\nFile updated: {html_path}")

    return True

if __name__ == '__main__':
    success = process_media_index()
    exit(0 if success else 1)
