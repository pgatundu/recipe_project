document.addEventListener('DOMContentLoaded', function () {
    // Function to handle pagination
    window.goToPage = function (pageNumber) {
        const url = new URL(window.location.href);
        url.searchParams.set('page', pageNumber); // Set the page query parameter

        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const recipeList = doc.getElementById('recipe-list').innerHTML;
                const paginationControls = doc.getElementById('pagination-controls').innerHTML;

                // Update the recipe list and pagination controls
                document.getElementById('recipe-list').innerHTML = recipeList;
                document.getElementById('pagination-controls').innerHTML = paginationControls;
            })
            .catch(error => console.error('Error fetching the recipes:', error));
    };
});
