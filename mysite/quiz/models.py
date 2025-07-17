from django.db import models

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    published_date = models.DateTimeField('date published')

    def __str__(self):
        return self.text

class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text