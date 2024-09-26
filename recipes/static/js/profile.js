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
    editBioButton.addEventListener('click', function () {
        editBioButton.style.display = 'none';
        bioDisplay.style.display = 'none';
        editBioForm.style.display = 'block';
    });

    // Cancel the edit and revert back to displaying the bio
    cancelBioButton.addEventListener('click', function () {
        editBioForm.style.display = 'none';
        editBioButton.style.display = 'block';
        bioDisplay.style.display = 'block';
    });

    // Confirm deletion of profile
    deleteProfileButton.addEventListener('click', function () {
        if (confirm("Are you sure you want to delete your profile? This action cannot be undone.")) {
            deleteProfileForm.submit();  // Submit the form if confirmed
        }
    });

    // Confirm deletion of profile photo
    deleteProfilePhotoButton.addEventListener('click', function () {
        if (confirm("Are you sure you want to delete your profile photo? This action cannot be undone.")) {
            deleteProfilePhotoForm.submit();  // Submit the form if confirmed
        }
    });

    // Show/hide the delete photo button
    const threeDotsMenu = document.querySelector('.three-dots-menu');
    const deletePhotoForm = document.querySelector('.delete-photo-form');

    threeDotsMenu.addEventListener('click', function () {
        deletePhotoForm.style.display = deletePhotoForm.style.display === 'block' ? 'none' : 'block';
    });
});