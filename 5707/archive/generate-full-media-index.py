#!/usr/bin/env python3
"""
Generate complete media-index.html with all media types (images, PDFs, docs, raw-html).

This script scans the media/ directory and creates a comprehensive index with:
- All media files from images/, pdfs/, docs/, raw-html/
- Data attributes for filtering: data-type, data-folders, data-filename
- Original navbar and sidebar navigation from current HTML
- Responsive grid layout with all media types
"""

import re
import os
from pathlib import Path
from datetime import datetime

def get_file_type(file_path):
    """Determine media type from file extension and folder."""
    ext = Path(file_path).suffix.lower()
    folder = file_path.split('/')[0]  # First folder: images, pdfs, docs, raw-html

    if folder == 'images':
        return 'image'
    elif folder == 'pdfs':
        return 'pdf'
    elif folder == 'raw-html':
        return 'raw-html'
    else:  # docs
        return 'document'

def extract_folders(file_path):
    """Extract folder hierarchy from media path."""
    parts = file_path.replace('\\', '/').split('/')
    # Remove filename (last part)
    if parts:
        parts = parts[:-1]
    return '|'.join(parts) if parts else 'root'

def extract_filename(file_path):
    """Extract filename without extension and normalize."""
    return Path(file_path).stem.lower()

def get_display_name(file_path):
    """Get human-readable display name for file."""
    # For images, just use filename
    # For docs, try to make readable from filename
    filename = Path(file_path).name
    return filename

def scan_media_directory(media_dir):
    """Scan media directory and build list of all media files."""
    media_files = []
    media_path = Path(media_dir)

    # Scan each media type folder
    for folder in ['images', 'pdfs', 'docs', 'raw-html']:
        folder_path = media_path / folder
        if not folder_path.exists():
            continue

        for file_path in sorted(folder_path.rglob('*')):
            if file_path.is_file():
                # Skip hidden files
                if file_path.name.startswith('.'):
                    continue

                # Relative path from media directory
                rel_path = str(file_path.relative_to(media_path)).replace('\\', '/')
                media_files.append(rel_path)

    return media_files

def extract_nav_from_current(current_html_path):
    """Extract navigation HTML from current media-index.html."""
    with open(current_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract navigation section
    nav_match = re.search(r'<nav[^>]*>.*?</nav>', content)
    if nav_match:
        return nav_match.group(0)

    return None

def create_media_card(file_path):
    """Create HTML card for a media file."""
    file_type = get_file_type(file_path)
    folders = extract_folders(file_path)
    filename = extract_filename(file_path)
    display_name = get_display_name(file_path)

    # Determine alt text based on type
    if file_type == 'image':
        alt_text = f"Media image: {display_name}"
    else:
        alt_text = f"{file_type.upper()}: {display_name}"

    if file_type == 'image':
        # For images, create preview with thumbnail
        full_path = f"media/{file_path}"
        card = (
            f'<article class="card media-card" data-type="image" '
            f'data-folders="{folders}" data-filename="{filename}">'
            f'<a href="{full_path}">'
            f'<img src="{full_path}" alt="{alt_text}"></a>'
            f'<div class="meta"><strong>{display_name}</strong>'
            f'<div class="muted">media/{folders}</div></div>'
            f'</article>'
        )
    else:
        # For non-image files, create card with icon/label
        file_ext = Path(file_path).suffix.upper()[1:]  # Remove the dot
        full_path = f"media/{file_path}"
        card = (
            f'<article class="card media-card" data-type="{file_type}" '
            f'data-folders="{folders}" data-filename="{filename}">'
            f'<a href="{full_path}" class="file-link">'
            f'<div class="file-icon">[{file_ext}]</div>'
            f'</a>'
            f'<div class="meta"><strong>{display_name}</strong>'
            f'<div class="muted">media/{folders}</div></div>'
            f'</article>'
        )

    return card

def generate_media_index():
    """Generate complete media-index.html with all media types."""

    current_html_path = Path('media-index.html')
    media_dir = Path('media')

    if not media_dir.exists():
        print("Error: media/ directory not found")
        return False

    print("Scanning media directory...")
    media_files = scan_media_directory(media_dir)
    print(f"Found {len(media_files)} media files")

    # Extract navigation from current HTML
    nav_html = extract_nav_from_current(current_html_path)

    # Count by type
    type_counts = {'image': 0, 'pdf': 0, 'document': 0, 'raw-html': 0}
    for file_path in media_files:
        file_type = get_file_type(file_path)
        type_counts[file_type] += 1

    # Generate all cards
    cards = [create_media_card(f) for f in media_files]
    cards_html = '\n'.join(cards)  # We'll minify later if needed

    # Build complete HTML
    html_parts = [
        '<!doctype html><html><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>Media index</title><link rel="stylesheet" href="style.css">',
        '</head><body><header><div class="bar"><a href="index.html" class="brand">5707 Scenic Ave Research</a></div></header>',
        '<main class="shell">',
    ]

    # Add navigation
    if nav_html:
        html_parts.append(nav_html)

    # Add layout and content
    html_parts.extend([
        '<div class="layout"><aside class="panel sidebar-desktop"></aside>',
        '<section class="panel content">',
        '<div class="gallery">',
        cards_html,
        '</div></section></div></main></body></html>'
    ])

    full_html = ''.join(html_parts)

    # Write to file
    with open(current_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print("\n=== Generation Complete ===")
    print(f"Total media cards: {len(media_files)}")
    print(f"  Images: {type_counts['image']}")
    print(f"  PDFs: {type_counts['pdf']}")
    print(f"  Documents: {type_counts['document']}")
    print(f"  Raw HTML: {type_counts['raw-html']}")
    print(f"\nFile written: {current_html_path}")

    return True

if __name__ == '__main__':
    success = generate_media_index()
    exit(0 if success else 1)
