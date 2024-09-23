# Recipe Management App

## Distinctiveness and Complexity

This project is a recipe management application that allows users to upload recipes, view their own recipes, and search for recipes based on ingredients. Unlike social networks or e-commerce sites, this application focuses on managing and searching recipes. It is built with Django for the backend and JavaScript for interactive features on the frontend.

## File Descriptions

- `recipes_project/settings.py`: Django project settings.
- `recipes/models.py`: Defines the Recipe model.
- `recipes/views.py`: Contains view functions for handling user requests.
- `recipes/forms.py`: Includes forms for recipe upload and user registration.
- `recipes/urls.py`: Defines URL patterns for the recipes app.
- `recipes/templates/base.html`: Base template for common layout.
- `recipes/templates/index.html`: Search page and recipe listing.
- `recipes/templates/register.html`: User registration page.
- `recipes/templates/upload_recipe.html`: Page for uploading recipes.
- `recipes/templates/recipe_list.html`: Page for viewing user’s recipes.
- `static/styles.css`: Custom styles for the application.

## Running the Application

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    ```bash
    python -m pip install Pillow
    ```

2. Apply migrations:

    ```bash
    python manage.py migrate
    ```

3. Create a superuser (for admin access):

    ```bash
    python manage.py createsuperuser
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

Visit `http://127.0.0.1:8000/` in your browser to use the application.

## Additional Information

Ensure you have Django installed and configured correctly. The application includes user authentication and recipe management features, making it a comprehensive solution for recipe enthusiasts.

