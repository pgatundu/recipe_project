document.addEventListener('DOMContentLoaded', function () {
    // Get the options button and dropdown container
    const optionsButtons = document.querySelectorAll('#delete-recipe-form .options-button');

    // Add event listener to each options button
    optionsButtons.forEach(optionsButton => {
        optionsButton.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent event from bubbling up

            const dropdownMenu = this.nextElementSibling; // Get the dropdown menu next to the clicked button
            dropdownMenu.classList.toggle('show'); // Toggle visibility of the dropdown
        });
    });

    // Hide dropdown if clicking outside
    document.addEventListener('click', function () {
        const dropdowns = document.querySelectorAll('#delete-recipe-form .dropdown-menu');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('show'); // Hide all dropdowns
        });
    });
});


        
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
