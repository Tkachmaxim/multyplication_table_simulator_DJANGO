from django.db import models

class Result(models.Model):
    name=models.CharField(max_length=20)
    total_tasks=models.IntegerField()
    mistakes=models.IntegerField()
    examples_of_mistakes=models.TextField()
