from django.db import models
from quiz.models import Quiz
# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=6, choices=(
        ('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Question = {}, Answer: {}".format(self.question.text, self.answer)