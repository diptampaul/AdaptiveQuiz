from django.db import models
from quiz.models import Quiz
from django.contrib.auth.models import User

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey()
    user = models.ForeignKey()
    score = models.ForeignKey()