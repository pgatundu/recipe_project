from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    description = models.TextField()
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    food_photo = models.ImageField(upload_to='food_photos/', blank=True, null=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} by {self.user.username if self.user else 'Anonymous'}"

class FoodPhoto(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_photos/')

class RecipeRating(models.Model):
   recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reciperating')
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   rating = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username


