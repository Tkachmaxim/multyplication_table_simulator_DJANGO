import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from Trainer import modulle
from Trainer.forms import MyResultForm



class Game:
    permission=True
    number_of_tasks = 0
    action = ''
    tasks = []
    total = 0
    number_example = 0
    mistakes = 0
    session = 0
    total_for_save = 0
    mistakes_for_save = 0
    mistakes_for_save_example = []
    a = 0
    b = 0
    result = 0


    def generate_task(self):
        self.tasks=modulle.choice_number(self.number_of_tasks, self.action)
        return self.tasks

class Start(View):

    def get(self, request):
        if Game.permission==False:
            return render(request,'trainer_app.html', {'a': Game.a, 'b': Game.b,
                                                   'result': Game.result, 'number_task': Game.number_example, 'tasks_deb':Game.tasks})
        return render(request, 'index.html')

    def post(self, request):
        if Game.permission==True:
        #if Game.total==0:
            if (request.POST.get('number')).isdigit() and int(request.POST.get('number')) > 0 and request.POST.get('difficult') != None:
                    number_of_tasks=int(request.POST.get('number'))
                    action=request.POST.get('difficult')
                    Game.number_of_tasks=number_of_tasks
                    Game.total=number_of_tasks
                    Game.action=action
                    Game.tasks=modulle.choice_number(number_of_tasks,action)
                    Game.session+=1
                    Game.permission=False
                    return redirect('trainer_app')
            else:
                return redirect('start')
        else:
            return redirect('trainer_app')
        #return redirect('trainer_app')


class TrainerApp(View):

    def get(self, request):
        if Game.number_example==Game.total:
            return redirect('finish')

        try:
            Game.a, Game.b, Game.result = (Game.tasks.pop()).values()
            Game.number_example+=1
        except IndexError:
            return render(request, 'finish.html', {'result': Game.total, 'mistakes': Game.mistakes})
        return render(request,'trainer_app.html', {'a': Game.a, 'b': Game.b,
                                                   'result': Game.result, 'number_task': Game.number_example, 'tasks_deb':Game.tasks})

    def post(self, request):
        try:
            if int(request.POST.get('answer')) == Game.result:
                messages.success(request, 'ПРАВИЛЬНО')

            elif int(request.POST.get('answer')) != Game.result:
                messages.error(request, 'НЕ ПРАВИЛЬНО')
                Game.mistakes += 1
                Game.tasks.insert(0,{'a':Game.a, 'b':Game.b, 'result':Game.result})

        except ValueError:
            return redirect(request.path)



        return redirect(request.path)

class Finish(View):
    def get(self, request):
        result, mistakes = Game.total, Game.mistakes
        if mistakes/result<=0.2:
            image='https://upload.wikimedia.org/wikipedia/commons/4/4f/Tesla_Model_S_02_2013.jpg'
        elif 0.2<mistakes/result<0.4:
            image='https://autoreview.ru/images/Article/1609/Article_160932_860_575.jpg'
        else:
            image='https://auto.ironhorse.ru/wp-content/uploads/1977/11/412.jpg'
        if mistakes==0:
            return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':True})
        elif mistakes>0 and Game.session==1:
            Game.tasks*=5
            Game.session+=1
        random.shuffle(Game.tasks)
        Game.total, Game.mistakes, Game.number_example = len(Game.tasks), 0, 0
        return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':False})

class Enter_Result(View):

    def get(self, request):
        form=MyResultForm
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form=MyResultForm(request.POST)

        if form.is_valid():
            total_save=Game.total
            total_mistakes_save=Game.mistakes
            example_mmistakes_save=tuple(Game.tasks)
            result=form.save(commit=False)
            result.total_tasks = total_save
            result.mistakes = total_mistakes_save
            result.examples_of_mistakes = example_mmistakes_save
            result.save()
            Game.permission=True
            Game.number_of_tasks = 0
            Game.action = ''
            Game.tasks = []
            Game.total = 0
            Game.number_example = 0
            Game.mistakes = 0
            Game.session = 0
            Game.total_for_save = 0
            Game.mistakes_for_save = 0
            return redirect('start')
        return redirect('enter_result')







'''
class WorkOnMistakes(View):
    def post(self, request):
        mistake=TrainerApp.mistakes.pop()
        return render(request, 'trainer_app.html', {'a':mistake['a'], 'b':mistake['b'], 'result':mistake['result']})
'''

