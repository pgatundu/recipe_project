document.addEventListener('DOMContentLoaded', function () {
    const editBioButton = document.getElementById('edit-bio-btn');
    const editBioForm = document.getElementById('edit-bio-form');
    const cancelBioButton = document.getElementById('cancel-bio-btn');
    const bioDisplay = document.getElementById('bio-display');
    const deleteProfileButton = document.getElementById('delete-profile-btn');
    const deleteProfileForm = document.getElementById('delete-profile-form');
    const deleteProfilePhotoButton = document.getElementById('delete-profile-photo-btn');
    const deleteProfilePhotoForm = document.getElementById('delete-profile-photo-form');

    // Show the form and hide the "Edit Bio" button when clicked
    if (editBioButton) {
        editBioButton.addEventListener('click', function () {
            editBioButton.style.display = 'none';
            bioDisplay.style.display = 'none';
            editBioForm.style.display = 'block';
            deleteProfileForm.style.display = 'block';  // Show the delete profile button
        });
    }

    // Cancel the edit and revert back to displaying the bio
    if (cancelBioButton) {
        cancelBioButton.addEventListener('click', function () {
            editBioForm.style.display = 'none';
            editBioButton.style.display = 'block';
            bioDisplay.style.display = 'block';
            deleteProfileForm.style.display = 'none';  // Hide the delete profile button
        });
    }

    // Confirm deletion of profile
    if (deleteProfileButton && deleteProfileForm) {
        deleteProfileButton.addEventListener('click', function () {
            const confirmation = confirm("Are you sure you want to delete your profile? This action cannot be undone.");
            if (confirmation) {
                deleteProfileForm.submit();  // Submit the form if confirmed
            }
        });
    }

    // Confirm deletion of profile photo
    if (deleteProfilePhotoButton && deleteProfilePhotoForm) {
        deleteProfilePhotoButton.addEventListener('click', function () {
            const confirmation = confirm("Are you sure you want to delete your profile photo? This action cannot be undone.");
            if (confirmation) {
                deleteProfilePhotoForm.submit();  // Submit the form if confirmed
            }
        });
    }
});
