#!/usr/bin/env python3
"""
Generate media-index.html with filtering and sorting UI.

Adds filter panel HTML with:
- Media type checkboxes (Images, PDFs, Documents, Raw HTML)
- Folder category checkboxes (dynamically generated from data)
- Sorting dropdown
- Clear Filters button
"""

import re
import os
from pathlib import Path
from collections import defaultdict

def get_file_type(file_path):
    """Determine media type from file extension and folder."""
    folder = file_path.split('/')[0]
    if folder == 'images':
        return 'image'
    elif folder == 'pdfs':
        return 'pdf'
    elif folder == 'raw-html':
        return 'raw-html'
    else:
        return 'document'

def extract_folders(file_path):
    """Extract folder hierarchy from media path."""
    parts = file_path.replace('\\', '/').split('/')
    if parts:
        parts = parts[:-1]
    return parts

def extract_filename(file_path):
    """Extract filename without extension."""
    return Path(file_path).stem.lower()

def get_display_name(file_path):
    """Get human-readable display name for file."""
    return Path(file_path).name

def scan_media_directory(media_dir):
    """Scan media directory and return files and folder structure."""
    media_files = []
    all_folders = set()

    media_path = Path(media_dir)

    for folder in ['images', 'pdfs', 'docs', 'raw-html']:
        folder_path = media_path / folder
        if not folder_path.exists():
            continue

        for file_path in sorted(folder_path.rglob('*')):
            if file_path.is_file() and not file_path.name.startswith('.'):
                rel_path = str(file_path.relative_to(media_path)).replace('\\', '/')
                media_files.append(rel_path)

                # Track all folder levels
                parts = extract_folders(rel_path)
                for i in range(len(parts)):
                    all_folders.add('|'.join(parts[:i+1]))

    return media_files, sorted(all_folders)

def create_media_card(file_path):
    """Create HTML card for a media file."""
    file_type = get_file_type(file_path)
    folders = '|'.join(extract_folders(file_path))
    filename = extract_filename(file_path)
    display_name = get_display_name(file_path)

    if file_type == 'image':
        alt_text = f"Media: {display_name}"
        full_path = f"media/{file_path}"
        card = (
            f'<article class="card media-card" data-type="image" '
            f'data-folders="{folders}" data-filename="{filename}">'
            f'<a href="{full_path}"><img src="{full_path}" alt="{alt_text}"></a>'
            f'<div class="meta"><strong>{display_name}</strong>'
            f'<div class="muted">media/{folders}</div></div></article>'
        )
    else:
        file_ext = Path(file_path).suffix.upper()[1:]
        full_path = f"media/{file_path}"
        card = (
            f'<article class="card media-card" data-type="{file_type}" '
            f'data-folders="{folders}" data-filename="{filename}">'
            f'<a href="{full_path}" class="file-link">'
            f'<div class="file-icon">[{file_ext}]</div></a>'
            f'<div class="meta"><strong>{display_name}</strong>'
            f'<div class="muted">media/{folders}</div></div></article>'
        )

    return card

def get_top_level_folders(all_folders):
    """Extract unique top-level folder categories."""
    top_level = set()
    for folder_path in all_folders:
        first_part = folder_path.split('|')[0]
        top_level.add(first_part)
    return sorted(top_level)

def create_filter_panel_html(media_files):
    """Create the filter panel HTML."""

    # Build unique folder paths
    all_folder_paths = set()
    for file_path in media_files:
        folders = extract_folders(file_path)
        for i in range(len(folders)):
            all_folder_paths.add('|'.join(folders[:i+1]))

    all_folder_paths = sorted(all_folder_paths)
    top_level_folders = get_top_level_folders(all_folder_paths)

    # Create HTML for media type filters
    type_filters = (
        '<div class="filter-group">'
        '<h3>Media Type</h3>'
        '<label><input type="checkbox" class="filter-type" value="image"> Images</label>'
        '<label><input type="checkbox" class="filter-type" value="pdf"> PDFs</label>'
        '<label><input type="checkbox" class="filter-type" value="document"> Documents</label>'
        '<label><input type="checkbox" class="filter-type" value="raw-html"> Raw HTML</label>'
        '</div>'
    )

    # Create HTML for folder filters
    folder_filters_html = '<div class="filter-group"><h3>Folders</h3>'
    for folder in all_folder_paths:
        # Create readable label from folder path
        parts = folder.split('|')
        label = ' / '.join(p.replace('-', ' ').title() for p in parts)
        folder_filters_html += (
            f'<label><input type="checkbox" class="filter-folder" value="{folder}"> '
            f'{label}</label>'
        )
    folder_filters_html += '</div>'

    # Combine into full filter panel
    filter_panel = (
        '<div id="filter-panel" class="filter-panel">'
        '<button id="filter-toggle" class="filter-toggle" aria-label="Toggle filters">'
        'Filters</button>'
        '<div class="filter-container">'
        '<div class="filter-header">'
        '<h2>Filter Media</h2>'
        '<button id="clear-filters" class="clear-btn">Clear All</button>'
        '</div>'
        '<div class="filter-controls">'
        f'{type_filters}'
        f'{folder_filters_html}'
        '<div class="filter-group">'
        '<h3>Sort By</h3>'
        '<select id="sort-by" class="sort-select">'
        '<option value="default">Default Order</option>'
        '<option value="filename">Filename (A-Z)</option>'
        '<option value="folder">Folder Path</option>'
        '<option value="type">Media Type</option>'
        '</select>'
        '</div>'
        '</div>'
        '<div id="result-count" class="result-count">Showing all items</div>'
        '</div>'
        '</div>'
    )

    return filter_panel

def extract_nav_from_current(current_html_path):
    """Extract navigation HTML from current media-index.html."""
    try:
        with open(current_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        nav_match = re.search(r'<nav[^>]*>.*?</nav>', content)
        if nav_match:
            return nav_match.group(0)
    except:
        pass
    return None

def generate_media_index():
    """Generate media-index.html with filtering UI."""

    current_html_path = Path('media-index.html')
    media_dir = Path('media')

    if not media_dir.exists():
        print("Error: media/ directory not found")
        return False

    print("Scanning media directory...")
    media_files, all_folders = scan_media_directory(media_dir)
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
    cards_html = ''.join(cards)

    # Create filter panel
    filter_panel = create_filter_panel_html(media_files)

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

    # Add layout with filter panel and content
    html_parts.extend([
        '<div class="layout">',
        '<aside class="panel sidebar-desktop"></aside>',
        '<section class="panel content">',
        filter_panel,
        '<div class="gallery">',
        cards_html,
        '</div></section></div></main>',
        '<script>',
        # JavaScript will be added inline later
        '</script>',
        '</body></html>'
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
    print(f"Total folder categories: {len(all_folders)}")
    print(f"\nFile written: {current_html_path}")

    return True

if __name__ == '__main__':
    success = generate_media_index()
    exit(0 if success else 1)
