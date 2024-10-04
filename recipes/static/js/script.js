function handleLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('logout-form').submit();  // Submit the form
        });
    }
}


// Function to handle delete confirmation
function confirmDelete(button) {
    const modal = document.getElementById('delete-confirmation-modal');
    modal.style.display = 'block';

    const confirmButton = document.getElementById('confirm-delete');
    // Remove previous click event listeners
    confirmButton.onclick = null;

    // Attach a new click event listener for the confirmation
    confirmButton.onclick = function () {
        button.closest('form').submit();
    };
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('delete-confirmation-modal');
    modal.style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function (event) {
    const modal = document.getElementById('delete-confirmation-modal');
    if (event.target === modal) {
        closeModal();
    }
};

