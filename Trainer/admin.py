from django.contrib import admin
from .models import Result

@admin.register(Result)
class Result(admin.ModelAdmin):
    list_display = ('name', 'total_tasks', 'mistakes', 'examples_of_mistakes', 'time')