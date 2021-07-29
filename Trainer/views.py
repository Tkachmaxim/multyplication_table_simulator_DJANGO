import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from Trainer import modulle
from Trainer.forms import MyResultForm




class Game(object):
    def __init__(self, number_of_tasks, action):
        self.tasks=modulle.choice_number(number_of_tasks, action)
        self.total=number_of_tasks
        self.number_example=0
        self.mistakes= 0
        self.session=0
        self.total_for_save=0
        self.mistakes_for_save=0
        self.mistakes_for_save_example=[]

class Start(View):
    def get(self, request):
        if game.total>0:
            return render(request, 'trainer_app.html', {'a': TrainerApp.a, 'b': TrainerApp.b,
                                                        'result': TrainerApp.result,
                                                        'number_task': game.number_example})
        return render(request, 'index.html')

    def post(self, request):
        global game
        if game.total==0:
            if (request.POST.get('number')).isdigit() and int(request.POST.get('number')) > 0 and request.POST.get('difficult') != None:
                    number_of_tasks=int(request.POST.get('number'))
                    action=request.POST.get('difficult')
                    game=Game(number_of_tasks=number_of_tasks, action=action)
                    game.session+=1
                    return redirect('trainer_app')
            else:
                return redirect('start')
        else:
            return redirect('trainer_app')
        return render(request, 'index.html')


class TrainerApp(View):
    a= int
    b= int
    result= int

    def get(self, request):
        if game.number_example==game.total:
            game.mistakes = 0
            game.total = len(game.tasks)
            game.number_example = 0
            return redirect('finish')

        try:
            TrainerApp.a, TrainerApp.b, TrainerApp.result = (game.tasks.pop()).values()
            game.number_example+=1
        except IndexError:
            return render(request, 'finish.html', {'result': game.total, 'mistakes': game.mistakes})
        return render(request,'trainer_app.html', {'a': TrainerApp.a, 'b': TrainerApp.b,
                                                   'result': TrainerApp.result, 'number_task': game.number_example, 'tasks_deb':game.tasks})

    def post(self, request):
        try:
            if int(request.POST.get('answer')) == TrainerApp.result:
                messages.success(request, 'ПРАВИЛЬНО')

            elif int(request.POST.get('answer')) != TrainerApp.result:
                messages.error(request, 'НЕ ПРАВИЛЬНО')
                game.mistakes += 1
                game.tasks.insert(0,{'a':TrainerApp.a, 'b':TrainerApp.b, 'result':TrainerApp.result})

        except ValueError:
            return redirect(request.path)

        return redirect(request.path)

class Finish(View):
    def get(self, request):
        result, mistakes = game.total, game.mistakes
        print(mistakes, result)
        if mistakes/result<=0.2:
            image='https://upload.wikimedia.org/wikipedia/commons/4/4f/Tesla_Model_S_02_2013.jpg'
        elif 0.2<mistakes/result<0.4:
            image='https://autoreview.ru/images/Article/1609/Article_160932_860_575.jpg'
        else:
            image='https://auto.ironhorse.ru/wp-content/uploads/1977/11/412.jpg'
        if mistakes==0:
            game.total_for_save = game.total
            game.mistakes_for_save = game.mistakes
            game.mistakes_for_save_example = tuple(game.tasks)
            return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':True})
        elif mistakes>0 and game.session==1:
            game.tasks*=5
            game.session+=1
        random.shuffle(game.tasks)
        game.total, game.mistakes, game.number_example = len(game.tasks), 0, 0
        return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':False})

class Enter_Result(View):
    def get(self, request):
        form=MyResultForm
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form=MyResultForm(request.POST)
        if form.is_valid():
            result=form.save(commit=False)
            result.total_tasks=game.total_for_save
            result.mistakes=game.mistakes_for_save
            result.examples_of_mistakes=game.mistakes_for_save_example
            result.save()
            print('this is taks', game.tasks)
            game.total=0
        return redirect('start')



game=Game(0,0)




'''
class WorkOnMistakes(View):
    def post(self, request):
        mistake=TrainerApp.mistakes.pop()
        return render(request, 'trainer_app.html', {'a':mistake['a'], 'b':mistake['b'], 'result':mistake['result']})
'''

