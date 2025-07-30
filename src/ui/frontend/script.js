const searchBar = document.getElementById('search-bar');
const suggestionsBox = document.getElementById('suggestions-box');
const searchForm = document.getElementById('search-form');

const AUTOCOMPLETION_API_URL = 'http://127.0.0.1:8000/autocomplete';
const ADD_QUERY_API_URL = 'http://127.0.0.1:8000/insert';
const SEARCH_API_URL = "http://127.0.0.1:8050/search"

let debounceTimer;

searchBar.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = searchBar.value;

    if (query.length < 3) {
        suggestionsBox.innerHTML = '';
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch(`${AUTOCOMPLETION_API_URL}?prefix=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log('Suggestions reçues:', data);
                displaySuggestions(data);
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
                suggestionsBox.innerHTML = '';
            });
    }, 500);
});

function displaySuggestions(suggestions) {
    if (!suggestions || suggestions.length === 0) {
        suggestionsBox.innerHTML = '';
        return;
    }

    suggestionsBox.innerHTML = '';
    suggestions.slice(0, 3).forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = suggestion;
        suggestionItem.addEventListener('click', () => {
            searchBar.value = suggestion;
            suggestionsBox.innerHTML = '';
        });
        suggestionsBox.appendChild(suggestionItem);
    });
}

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const query = searchBar.value;

    if (query) {
        fetch(ADD_QUERY_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ words: [query] }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Query added:', data);
            searchBar.value = ''; // Clear the search bar
        })
        .catch(error => {
            console.error('Error adding query:', error);
        });

        const encodedQuery = encodeURIComponent(query);
        fetch(`${SEARCH_API_URL}?keyword=${encodedQuery}`)
        .then(response => response.json())
        .then(searchResults => {
                console.log('Search results:', searchResults);
            })
        .catch(error => {
                    console.error('Error fetching search results:', error);
                });
    }
}
);