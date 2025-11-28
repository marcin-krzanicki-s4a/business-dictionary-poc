document.addEventListener('DOMContentLoaded', async function () {
    // Support both home page search and navbar search
    const homeSearchInput = document.getElementById('search-input');
    const homeSearchResults = document.getElementById('search-results');
    const homeResultsList = document.getElementById('results-list');

    const navbarSearchInput = document.getElementById('navbar-search-input');
    const navbarSearchResults = document.getElementById('navbar-search-results');

    // Exit if no search inputs found
    if (!homeSearchInput && !navbarSearchInput) return;

    let searchIndex = [];

    // Load search index
    try {
        const baseUrl = window.baseURL || '/';
        const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl : baseUrl + '/';
        const response = await fetch(cleanBaseUrl + 'index.json');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        searchIndex = await response.json();
    } catch (error) {
        console.error('Error loading search index:', error);
    }

    // Get icon and color for category
    function getCategoryIcon(category) {
        const icons = {
            'Business Object': 'file-text',
            'UI View': 'laptop',
            'Perspective': 'album',
            'Global Attribute': 'tag'
        };
        return icons[category] || 'file-text';
    }

    // Search function
    function performSearch(query, resultsContainer, resultsList) {
        if (!query.trim()) {
            resultsContainer.style.display = 'none';
            if (resultsList) resultsList.innerHTML = '';
            return;
        }

        const lowercaseQuery = query.toLowerCase();
        const results = searchIndex.filter(item => {
            const searchableContent = [
                item.title,
                item.section,
                item.category,
                item.content,
                item.status
            ].join(' ').toLowerCase();

            return searchableContent.includes(lowercaseQuery);
        }).slice(0, 10); // Limit to 10 results

        const resultsHTML = results.length === 0
            ? '<div class="uk-text-center uk-text-muted uk-padding-small">No results found</div>'
            : results.map(item => `
                <div style="padding: 12px; border-bottom: 1px solid #e5e5e5;">
                    <div style="margin-bottom: 4px;">
                        <strong style="font-size: 1.05em; color: #1f2937;">${escapeHtml(item.title)}</strong>
                    </div>
                    <div style="margin-bottom: 6px; display: flex; align-items: center; gap: 8px; font-size: 0.85em; color: #6b7280;">
                        <span uk-icon="icon: ${getCategoryIcon(item.category)}; ratio: 0.7"></span>
                        <span>${escapeHtml(item.category)} • ${escapeHtml(item.section)}</span>
                    </div>
                    <p style="margin: 0 0 8px 0; font-size: 0.9em; color: #4b5563; line-height: 1.4;">
                        ${escapeHtml(item.content.substring(0, 100))}...
                    </p>
                    <a href="${item.permalink}" class="uk-button uk-button-text uk-button-small" 
                       style="padding: 0; font-size: 0.9em;">View Details →</a>
                </div>
            `).join('');

        if (resultsList) {
            // Home page (uses <ul><li>)
            resultsList.innerHTML = results.length === 0
                ? '<li class="uk-text-center uk-text-muted">No results found</li>'
                : results.map(item => `
                    <li style="text-align: left;">
                        <div style="margin-bottom: 4px;">
                            <strong style="font-size: 1.1em;">${escapeHtml(item.title)}</strong>
                        </div>
                        <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px; font-size: 0.9em; color: #6b7280;">
                            <span uk-icon="icon: ${getCategoryIcon(item.category)}; ratio: 0.8"></span>
                            <span>${escapeHtml(item.category)} • ${escapeHtml(item.section)}</span>
                        </div>
                        <p style="margin: 0; font-size: 0.95em; color: #374151; line-height: 1.4;">
                            ${escapeHtml(item.content.substring(0, 120))}...
                        </p>
                        <a href="${item.permalink}" class="uk-button uk-button-text uk-button-small uk-margin-small-top" style="padding-left: 0;">View Details →</a>
                    </li>
                `).join('');
        } else {
            // Navbar (uses <div>)
            resultsContainer.innerHTML = resultsHTML;
        }

        resultsContainer.style.display = 'block';
    }

    // Helper function to escape HTML
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // Setup home page search
    if (homeSearchInput && homeSearchResults && homeResultsList) {
        let searchTimeout;
        homeSearchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(e.target.value, homeSearchResults, homeResultsList);
            }, 300);
        });
    }

    // Setup navbar search
    if (navbarSearchInput && navbarSearchResults) {
        let searchTimeout;
        navbarSearchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(e.target.value, navbarSearchResults, null);
            }, 300);
        });

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!navbarSearchInput.contains(e.target) && !navbarSearchResults.contains(e.target)) {
                navbarSearchResults.style.display = 'none';
            }
        });
    }
});
