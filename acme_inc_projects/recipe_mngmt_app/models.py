from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    # quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    # instructions = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title