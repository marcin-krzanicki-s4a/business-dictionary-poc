document.addEventListener('DOMContentLoaded', async function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const resultsList = document.getElementById('results-list');
    
    if (!searchInput) return;
    
    let searchIndex = [];
    
    // Load search index
    try {
        const response = await fetch('/index.json');
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
    function performSearch(query) {
        if (!query.trim()) {
            searchResults.style.display = 'none';
            resultsList.innerHTML = '';
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
        
        if (results.length === 0) {
            resultsList.innerHTML = '<li class="uk-text-center uk-text-muted">No results found</li>';
            searchResults.style.display = 'block';
            return;
        }
        
        resultsList.innerHTML = results.map(item => `
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
        
        searchResults.style.display = 'block';
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
    
    // Event listener for search input
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300); // Debounce 300ms
    });
});

