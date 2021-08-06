from django.db import models

class Result(models.Model):
    name=models.CharField(max_length=20)
    total_tasks=models.IntegerField()
    mistakes=models.IntegerField()
    number_of_sessions=models.IntegerField(default=0)
    examples_of_mistakes=models.TextField()
    time=models.DateTimeField(auto_now=True)


class Game(models.Model):
    permission=models.BooleanField(default=True) # forbid start again if task dont complete
    number_of_tasks=models.IntegerField()
    total=models.IntegerField()
    number_example=models.IntegerField(default=1)
    mistakes=models.IntegerField()
    mistakes_examples=models.JSONField(default=[])
    tasks=models.JSONField(default=[])
    total_for_save=models.IntegerField()
    mistakes_for_save=models.IntegerField()
    session=models.IntegerField()
    action=models.CharField(max_length=10)


