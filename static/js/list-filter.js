// S4A Dictionary - List Page Filtering with Frontend Only
(function () {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function () {
        const searchInput = document.querySelector('.list-search-input');
        const statusSelect = document.querySelector('select[aria-label="Status Filter"]');
        const categorySelect = document.querySelector('select[aria-label="Category Filter"]');
        const dataTypeSelect = document.querySelector('select[aria-label="Data Type Filter"]');
        const cardContainers = document.querySelectorAll('[uk-grid] > div');

        if (!searchInput || !cardContainers.length) {
            console.log('Filter elements not found');
            return;
        }

        // Filter function
        function filterCards() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            const selectedStatus = statusSelect ? statusSelect.value : '';
            const selectedCategory = categorySelect ? categorySelect.value : '';
            const selectedDataType = dataTypeSelect ? dataTypeSelect.value : '';

            let visibleCount = 0;

            cardContainers.forEach(function (container) {
                const card = container.querySelector('.uk-card');
                if (!card) return;

                const cardTitle = card.querySelector('.uk-card-title');
                const cardBadge = card.querySelector('.uk-badge');
                const cardCategory = card.querySelector('.uk-text-small.uk-text-uppercase');
                
                const titleText = cardTitle ? cardTitle.textContent.toLowerCase() : '';
                const categoryText = cardCategory ? cardCategory.textContent.toLowerCase() : '';
                const badgeText = cardBadge ? cardBadge.textContent.toLowerCase().trim() : '';

                // Search Match Logic - search in title and category
                let matchesSearch = true;
                if (searchTerm) {
                    matchesSearch = titleText.includes(searchTerm) || 
                                   categoryText.includes(searchTerm);
                }

                // Status Filter
                let matchesStatus = true;
                if (selectedStatus && selectedStatus !== '') {
                    if (selectedStatus === '1') { // Active
                        matchesStatus = badgeText === 'active';
                    } else if (selectedStatus === '2') { // Draft
                        matchesStatus = badgeText === 'draft';
                    } else if (selectedStatus === '3') { // Deprecated
                        matchesStatus = badgeText === 'deprecated';
                    }
                }

                // Category Filter
                let matchesCategory = true;
                if (selectedCategory && selectedCategory !== '') {
                    if (selectedCategory === '1') { // Business Object
                        matchesCategory = categoryText.includes('business object');
                    } else if (selectedCategory === '2') { // UI View
                        matchesCategory = categoryText.includes('ui view');
                    } else if (selectedCategory === '3') { // Perspective
                        matchesCategory = categoryText.includes('perspective');
                    } else if (selectedCategory === '4') { // Global Attribute
                        matchesCategory = categoryText.includes('global attribute');
                    }
                }

                // Data Type Filter
                let matchesDataType = true;
                if (selectedDataType && selectedDataType !== '') {
                    matchesDataType = badgeText === selectedDataType.toLowerCase();
                }

                // Show/hide card container
                if (matchesSearch && matchesStatus && matchesCategory && matchesDataType) {
                    container.style.display = '';
                    visibleCount++;
                } else {
                    container.style.display = 'none';
                }
            });

            // Update "no results" message
            updateNoResultsMessage(visibleCount);
        }

        // Update or create "no results" message
        function updateNoResultsMessage(count) {
            let noResultsDiv = document.getElementById('no-results-message');

            if (count === 0) {
                if (!noResultsDiv) {
                    const grid = document.querySelector('[uk-grid]');
                    if (grid) {
                        noResultsDiv = document.createElement('div');
                        noResultsDiv.id = 'no-results-message';
                        noResultsDiv.className = 'uk-width-1-1 uk-text-center uk-margin-large-top uk-margin-large-bottom';
                        noResultsDiv.innerHTML = `
                            <div style="padding: 60px 20px;">
                                <span uk-icon="icon: search; ratio: 3" class="uk-text-muted"></span>
                                <h3 class="uk-margin-small-top">No results found</h3>
                                <p class="uk-text-muted uk-margin-small-top">Try adjusting your filters or search term</p>
                                <button id="reset-filters-btn" class="uk-button uk-button-default uk-margin-top">
                                    <span uk-icon="icon: refresh"></span> Reset Filters
                                </button>
                            </div>
                        `;
                        grid.appendChild(noResultsDiv);

                        // Add click handler for reset button
                        document.getElementById('reset-filters-btn').addEventListener('click', resetFilters);
                    }
                } else {
                    noResultsDiv.style.display = '';
                }
            } else {
                if (noResultsDiv) {
                    noResultsDiv.style.display = 'none';
                }
            }
        }

        // Reset all filters
        function resetFilters() {
            if (searchInput) searchInput.value = '';
            if (statusSelect) statusSelect.selectedIndex = 0;
            if (categorySelect) categorySelect.selectedIndex = 0;
            if (dataTypeSelect) dataTypeSelect.selectedIndex = 0;

            // Trigger UIkit update for custom selects
            if (window.UIkit) {
                UIkit.update();
            }

            // Re-run filter to show all cards
            filterCards();
        }

        // Debounce function for search input
        function debounce(func, wait) {
            let timeout;
            return function executedFunction() {
                const later = function () {
                    clearTimeout(timeout);
                    func();
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Event listeners
        if (searchInput) {
            searchInput.addEventListener('input', debounce(filterCards, 300));
        }

        if (statusSelect) {
            statusSelect.addEventListener('change', filterCards);
        }

        if (categorySelect) {
            categorySelect.addEventListener('change', filterCards);
        }

        if (dataTypeSelect) {
            dataTypeSelect.addEventListener('change', filterCards);
        }

        console.log('Filter initialized');
    });
})();
