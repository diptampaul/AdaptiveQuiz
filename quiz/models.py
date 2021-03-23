from django.db import models

# Create your models here.

class Quiz(modeks.model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='Duration of the Quiz in Minutes')
    difftime = models.CharField(max_length=6, choices=(('easy','easy'),('medium','medium'),('hard','hard')))
    required_score = models.IntegerField()

    def __str__(self):
        return "{}:--:{}".format(self.name, self.topic)

    def get_question(self):
        #modelname_set.all()
        return self.question_set.all()
