function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken');

function handleLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            const csrfToken = getCookie('csrftoken'); // Get CSRF token from cookies
            const form = document.getElementById('logout-form');
            const formData = new FormData(form);
            formData.append('csrfmiddlewaretoken', csrfToken); // Append CSRF token manually
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // This helps Django recognize it as an AJAX request
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload(); // Reload the page or redirect after successful logout
                } else {
                    console.error('Logout failed');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
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

