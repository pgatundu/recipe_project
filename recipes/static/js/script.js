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


