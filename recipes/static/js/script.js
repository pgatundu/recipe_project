
function confirmDelete() {
            return confirm('Are you sure you want to delete this recipe? This action cannot be undone.');
}
        
function handleLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('logout-form').submit();  // Submit the form
        });
    }
}

// Call the function when the document is ready
document.addEventListener('DOMContentLoaded', handleLogout);


