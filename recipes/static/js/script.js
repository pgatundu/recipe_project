function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            const form = document.getElementById('logout-form');
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/login/'; // Redirect to login page after successful logout
                    } else {
                        console.error('Logout failed');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
}

// Ensure the function is called once the page loads
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

