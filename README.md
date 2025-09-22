# 🍳 Recipe Management App

A **full-stack web application** for managing, searching, and rating recipes.  
Users can upload their own recipes, search by ingredients, rate others’ recipes in real time, and manage their profiles with photos and bios.  
Built with **Django, JavaScript, and AJAX** as part of Harvard’s **CS50W Web Programming with Python and JavaScript** course.

---

## 🚀 Features
- ⭐ **Real-time Ratings** – AJAX-powered 5-star rating system with instant updates.  
- 🔍 **Ingredient Search** – Find recipes by specific ingredients.  
- 👤 **Profile Management** – Upload profile pictures, edit bios, and manage user details.  
- 📂 **Recipe Management** – Upload, edit, and delete your recipes.  
- 🖥 **Dynamic UI** – Pagination and updates handled via AJAX for a smooth experience.  

---

## 🛠 Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript (AJAX)  
- **Database:** SQLite (default, can be swapped for PostgreSQL)  
- **Images:** Pillow (for handling image uploads)  

---

## 📦 Installation

Run the following commands:

```bash
# Clone the repository
git clone https://github.com/pgatundu/recipe_project.git

# Navigate into the project
cd recipe_project

# Install dependencies
pip install -r requirements.txt

# Install Pillow for image uploads
python -m pip install Pillow

# Apply migrations
python manage.py migrate

# (Optional) Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver
