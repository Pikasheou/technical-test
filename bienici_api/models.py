from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=100)
    dept_code = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    condominium_expenses = models.FloatField()
