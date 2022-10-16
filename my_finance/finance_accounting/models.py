from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False)

    def __str__(self):
        return self.name


class Operations(models.Model):
    sum = models.IntegerField(null=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.BooleanField()
