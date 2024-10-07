document.addEventListener("DOMContentLoaded", function () {
    // Attach event listeners to delete photo buttons
    const deletePhotoForms = document.querySelectorAll('.delete-photo-form');

    deletePhotoForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            const confirmed = confirm("Are you sure you want to delete this photo?");
            if (!confirmed) {
                event.preventDefault(); // Prevent form submission if not confirmed
            }
        });
    });

    // Attach event listeners to delete recipe buttons
    const deleteRecipeForms = document.querySelectorAll('.delete-recipe-form');

    deleteRecipeForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            const confirmed = confirm("Are you sure you want to delete this recipe?");
            if (!confirmed) {
                event.preventDefault(); // Prevent form submission if not confirmed
            }
        });
    });
});
