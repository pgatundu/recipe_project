document.addEventListener('DOMContentLoaded', function () {
    const ratingElements = document.querySelectorAll('.rating');

    ratingElements.forEach(ratingElement => {
        ratingElement.addEventListener('click', function (e) {
            if (e.target.classList.contains('fa-star')) {
                const recipeId = this.getAttribute('data-recipe-id');
                const ratingValue = e.target.getAttribute('data-value');

                // Highlight selected stars
                this.querySelectorAll('.fa-star').forEach(star => {
                    if (star.getAttribute('data-value') <= ratingValue) {
                        star.classList.add('gold');
                    } else {
                        star.classList.remove('gold');
                    }
                });

                // Send the rating to the backend
                fetch(`/rate_recipe/${recipeId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ rating: ratingValue })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error(data.error);
                        } else {
                            // Update the displayed average rating
                            this.closest('li').querySelector('.average-rating').textContent = data.new_average.toFixed(2);
                        }
                    })
                    .catch(error => {
                        console.error('Error rating recipe:', error);
                    });
            }
        });
    });

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
});
