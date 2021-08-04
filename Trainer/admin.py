from django.contrib import admin
from .models import Result, Game

@admin.register(Result)
class Result(admin.ModelAdmin):
    list_display = ('name', 'total_tasks', 'mistakes', 'examples_of_mistakes', 'time')

@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = (
        'permission', 'number_of_tasks', 'total', 'number_example',
        'mistakes', 'mistakes_examples', 'tasks', 'total_for_save', 'mistakes_for_save', 'session', 'action'
                    )