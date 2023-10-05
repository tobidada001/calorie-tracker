import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Meal(models.Model):
    meal_name = models.CharField( max_length=80, verbose_name='Meal Type')
    meal_carbohydrates_level = models.FloatField( verbose_name='Carb level')
    meal_protein_level = models.FloatField( verbose_name='Protein level')
    meal_fats_level = models.FloatField( verbose_name='Fats level')
    meal_cal_level = models.IntegerField(verbose_name='Calories level')
    meal_mg_level = models.FloatField( max_length=80, verbose_name='Mg level')
    meal_na_level = models.FloatField( max_length=80, verbose_name='Na level')
    meal_chol_level = models.FloatField( max_length=80, verbose_name='Cholesterol level')
    

    def __str__(self):
        return self.meal_name


class Consumed (models.Model):
    food = models.ForeignKey(Meal,  on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField( auto_now_add=False, default=datetime.datetime.now())

    def __str__(self):
        return self.food.meal_name

    class Meta:
        verbose_name_plural = 'Consumed'
    