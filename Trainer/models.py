from django.db import models

class Result(models.Model):
    name=models.CharField(max_length=20)
    total_tasks=models.IntegerField()
    mistakes=models.IntegerField()
    examples_of_mistakes=models.TextField()

class Game(models.Model):
    permission=models.BooleanField()
    number_of_tasks=models.IntegerField()
    total=models.IntegerField()
    number_example=models.IntegerField(default=0)
    mistakes=models.IntegerField()
    tasks=models.JSONField(default=[])
    total_for_save=models.IntegerField()
    mistakes_for_save=models.IntegerField()
    session=models.IntegerField()
    action=models.CharField(max_length=10)


