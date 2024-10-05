# Recipe Management App

## Distinctiveness and Complexity

This Recipe Management App is built with a unique focus on culinary content management and integrates several advanced features, setting it apart from simpler applications. It allows users to upload, search for, and rate recipes, while also managing their own profiles. These features are designed with both user interaction and performance in mind, offering a dynamic, real-time experience.

The complexity of this application is reflected in its real-time AJAX-based functionality. For instance, the star rating system allows users to rate recipes, and the interface updates immediately without a page reload. The ingredient-based search feature enables users to find recipes by specific ingredients, adding both efficiency and convenience. Additionally, users can manage their profile by editing bios and uploading profile pictures through an intuitive interface.

The app leverages Django’s robust backend framework to handle authentication, recipe management, and profile data, while JavaScript and AJAX manage the dynamic, frontend interactions. This combination creates a highly interactive user experience and distinguishes the project by its multifaceted functionality—making it more than a simple recipe-sharing platform.

## File Descriptions

### Django Files
- `recipes_project/settings.py`: Django project settings and configurations.
- `recipes/models.py`: Defines the `Recipe` and `Profile` models to manage recipe data and user profiles.
- `recipes/views.py`: Contains view logic for recipe handling, profile management, and search functionality.
- `recipes/forms.py`: Forms for user registration and recipe submission.
- `recipes/urls.py`: Maps URLs to their respective views.

### HTML Templates (in `recipes/templates`)
- `base.html`: The base template used throughout the app.
- `index.html`: Displays the recipe search bar and the recipe list.
- `login.html`: Page for user authentication.
- `register.html`: User registration page.
- `upload_recipe.html`: Form page for submitting new recipes.
- `recipe_list.html`: Displays recipes uploaded by the user.
- `profile.html`: User profile page where users can upload photos and edit their bio.
- `edit_recipe.html`: Page for editing existing recipes.
- `search.html`: Displays search results based on ingredient queries.

### JavaScript Files (in `recipes/static/js`)
- `pagination.js`: Handles pagination of recipes without reloading the page.
- `profile.js`: Manages interactions on the profile page, including profile picture uploads and bio edits.
- `ratings.js`: Implements the AJAX-powered 5-star rating system, allowing users to rate recipes in real-time.
- `recipe_list.js`: Manages user interactions on the recipe list page, such as recipe editing and deletion.
- `script.js`: General UI and functional JavaScript for dropdown menus and other enhancements.

### Static Files
- `static/styles.css`: Defines the app’s custom styles for layout, forms, buttons, and other design elements.

## Running the Application

1. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    Additionally, install Pillow for handling image uploads:

    ```bash
    python -m pip install Pillow
    ```

2. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

3. **Create a superuser** (for accessing the admin panel):

    ```bash
    python manage.py createsuperuser
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

5. **Access the app**:
   
    Visit `http://127.0.0.1:8000/` to interact with the application.

## Additional Information

### Key Features
- **Real-time Recipe Ratings**: AJAX-powered rating system that allows users to rate recipes instantly, with real-time updates to the rating count and average.
- **Ingredient-Based Search**: Search recipes by ingredients, which is accessible to both logged-in and logged-out users.
- **Profile Management**: Users can upload profile pictures, update their bios, and edit their profile information directly from the profile page.
- **Recipe Management**: Users can upload, edit, and delete their own recipes, while other users can view and rate them.

### Python Packages

To run the project, ensure the following Python packages are installed:

- Django (>=4.0, <5.0)
- Pillow (for handling image uploads)

All necessary packages are listed in the `requirements.txt` file for easy installation:

```bash
pip install -r requirements.txt
