from django.db import models

# Create your models here.


class Quiz(models.Model):
    topic = models.CharField(max_length=200)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='Duration of the Quiz in Minutes')
    required_score = models.IntegerField()

    def __str__(self):
        return "{}".format(self.topic)

    def get_question(self):
        # modelname_set.all()
        return self.question_set.all()[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'
