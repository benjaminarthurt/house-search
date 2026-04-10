/**
 * Media Gallery Filtering and Sorting
 * Handles dynamic filtering by media type and folder, plus sorting options
 */

class MediaGalleryFilter {
  constructor() {
    this.allCards = Array.from(document.querySelectorAll('.media-card'));
    this.filterTypeInputs = document.querySelectorAll('.filter-type');
    this.filterFolderInputs = document.querySelectorAll('.filter-folder');
    this.sortSelect = document.getElementById('sort-by');
    this.clearButton = document.getElementById('clear-filters');
    this.resultCount = document.getElementById('result-count');
    this.filterToggle = document.getElementById('filter-toggle');
    this.filterContainer = document.querySelector('.filter-container');

    this.totalCards = this.allCards.length;
    this.visibleCards = new Set(this.allCards);

    this.init();
  }

  init() {
    // Add event listeners
    this.filterTypeInputs.forEach(input => {
      input.addEventListener('change', () => this.applyFilters());
    });

    this.filterFolderInputs.forEach(input => {
      input.addEventListener('change', () => this.applyFilters());
    });

    this.sortSelect.addEventListener('change', () => this.applySorting());
    this.clearButton.addEventListener('click', () => this.clearFilters());

    // Mobile filter toggle
    if (this.filterToggle) {
      this.filterToggle.addEventListener('click', () => {
        this.filterToggle.classList.toggle('active');
        this.filterContainer.classList.toggle('show');
      });
    }

    // Load saved filter state from localStorage (optional)
    this.loadFilterState();

    // Initial render
    this.updateGallery();
  }

  applyFilters() {
    const selectedTypes = Array.from(this.filterTypeInputs)
      .filter(input => input.checked)
      .map(input => input.value);

    const selectedFolders = Array.from(this.filterFolderInputs)
      .filter(input => input.checked)
      .map(input => input.value);

    this.visibleCards = new Set(
      this.allCards.filter(card => {
        // Get card data
        const cardType = card.dataset.type;
        const cardFolders = card.dataset.folders;

        // Filter by media type (OR logic within type filter)
        if (selectedTypes.length > 0 && !selectedTypes.includes(cardType)) {
          return false;
        }

        // Filter by folder (OR logic within folder filter)
        if (selectedFolders.length > 0) {
          const matches = selectedFolders.some(folder => {
            // Check if card's folders start with selected folder
            return cardFolders.startsWith(folder);
          });
          if (!matches) {
            return false;
          }
        }

        return true;
      })
    );

    this.updateGallery();
    this.saveFilterState();
  }

  applySorting() {
    const sortMethod = this.sortSelect.value;
    const visibleArray = Array.from(this.visibleCards);

    switch (sortMethod) {
      case 'filename':
        visibleArray.sort((a, b) => {
          const aName = a.dataset.filename.toLowerCase();
          const bName = b.dataset.filename.toLowerCase();
          return aName.localeCompare(bName);
        });
        break;

      case 'folder':
        visibleArray.sort((a, b) => {
          const aFolder = a.dataset.folders;
          const bFolder = b.dataset.folders;
          return aFolder.localeCompare(bFolder);
        });
        break;

      case 'type':
        const typeOrder = { image: 0, pdf: 1, document: 2, 'raw-html': 3 };
        visibleArray.sort((a, b) => {
          const aType = typeOrder[a.dataset.type] || 999;
          const bType = typeOrder[b.dataset.type] || 999;
          if (aType !== bType) return aType - bType;
          // Secondary sort by filename within same type
          return a.dataset.filename.localeCompare(b.dataset.filename);
        });
        break;

      case 'default':
      default:
        // Keep original order
        visibleArray.sort((a, b) => {
          return this.allCards.indexOf(a) - this.allCards.indexOf(b);
        });
        break;
    }

    this.visibleCards = new Set(visibleArray);
    this.updateGallery();
  }

  clearFilters() {
    // Uncheck all filters
    this.filterTypeInputs.forEach(input => input.checked = false);
    this.filterFolderInputs.forEach(input => input.checked = false);
    this.sortSelect.value = 'default';

    // Show all cards
    this.visibleCards = new Set(this.allCards);
    this.updateGallery();

    // Clear localStorage
    localStorage.removeItem('mediaGalleryFilters');
    localStorage.removeItem('mediaGallerySortMethod');
  }

  updateGallery() {
    const gallery = document.querySelector('.gallery');

    // Hide all cards first
    this.allCards.forEach(card => {
      card.classList.add('hidden');
    });

    // Show filtered cards in order
    this.visibleCards.forEach(card => {
      card.classList.remove('hidden');
    });

    // Reorder visible cards in DOM
    const visibleArray = Array.from(this.visibleCards);
    const container = gallery;

    // Create a document fragment with correctly ordered cards
    // (or just rely on CSS display:none/grid for performance)

    // Update result count
    this.updateResultCount();
  }

  updateResultCount() {
    const count = this.visibleCards.size;
    if (count === this.totalCards) {
      this.resultCount.textContent = `Showing all ${count} items`;
    } else {
      this.resultCount.textContent = `Showing ${count} of ${this.totalCards} items`;
    }
  }

  saveFilterState() {
    const filters = {
      types: Array.from(this.filterTypeInputs)
        .filter(input => input.checked)
        .map(input => input.value),
      folders: Array.from(this.filterFolderInputs)
        .filter(input => input.checked)
        .map(input => input.value),
    };
    const sortMethod = this.sortSelect.value;

    localStorage.setItem('mediaGalleryFilters', JSON.stringify(filters));
    localStorage.setItem('mediaGallerySortMethod', sortMethod);
  }

  loadFilterState() {
    const savedFilters = localStorage.getItem('mediaGalleryFilters');
    const savedSort = localStorage.getItem('mediaGallerySortMethod');

    if (savedFilters) {
      const { types, folders } = JSON.parse(savedFilters);

      types.forEach(type => {
        const input = Array.from(this.filterTypeInputs).find(i => i.value === type);
        if (input) input.checked = true;
      });

      folders.forEach(folder => {
        const input = Array.from(this.filterFolderInputs).find(i => i.value === folder);
        if (input) input.checked = true;
      });
    }

    if (savedSort) {
      this.sortSelect.value = savedSort;
    }

    // Reapply filters with loaded state
    if (savedFilters || savedSort) {
      this.applyFilters();
      this.applySorting();
    }
  }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new MediaGalleryFilter();
  });
} else {
  new MediaGalleryFilter();
}
