from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_Level(models.Model):
    level = models.IntegerField()
    current_experience = models.IntegerField()
    border_experience = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_level(self):
        return self.level

    def get_current_experience(self):
        return self.current_experience

    def get_border_experience(self):
        return self.border_experience


class Theme(models.Model):
    name = models.CharField(max_length=50)
    access_level = models.IntegerField()
    theory = models.TextField()
    questions = models.TextField()
    answers = models.TextField()
    image = models.ImageField(null=True)


class Reward(models.Model):
    exp = models.IntegerField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
