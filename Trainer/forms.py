from django.forms import ModelForm

from Trainer.models import Result

class MyResultForm(ModelForm):
    class Meta:
        model=Result
        exclude=('total_tasks', 'mistakes', 'examples_of_mistakes',)
        labels={'name':'Введи сюда свое имя, УЧЕНИК',
                }




