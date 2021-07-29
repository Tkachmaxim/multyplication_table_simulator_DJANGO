import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from Trainer import modulle
from Trainer.forms import MyResultForm



class Game:
    permission=True
    class_counter=0


    def __init__(self, number_of_tasks, action):
        self.number_of_tasks=number_of_tasks
        self.action=action
        self.tasks=[]
        self.total=number_of_tasks
        self.number_example=0
        self.mistakes= 0
        self.session=0
        self.total_for_save=0
        self.mistakes_for_save=0
        self.mistakes_for_save_example=[]
        self.a = 0
        self.b = 0
        self.result = 0

    def generate_task(self):
        self.tasks=modulle.choice_number(self.number_of_tasks, self.action)
        return self.tasks

class Start(View):

    def get(self, request):
        if Game.permission==False:
            return render(request,'trainer_app.html', {'a': game.a, 'b': game.b,
                                                   'result': game.result, 'number_task': game.number_example, 'tasks_deb':game.tasks})
        return render(request, 'index.html')

    def post(self, request):
        if Game.permission==True:
        #if game.total==0:
            if (request.POST.get('number')).isdigit() and int(request.POST.get('number')) > 0 and request.POST.get('difficult') != None:
                    number_of_tasks=int(request.POST.get('number'))
                    action=request.POST.get('difficult')
                    global game
                    game=Game(number_of_tasks=number_of_tasks, action=action)
                    game.generate_task()
                    game.session+=1
                    Game.permission=False
                    Game.class_counter+=1
                    return redirect('trainer_app')
            else:
                return redirect('start')
        else:
            return redirect('trainer_app')
        #return render(request, 'index.html')


class TrainerApp(View):

    def get(self, request):
        global game
        if game.number_example==game.total:
            return redirect('finish')

        try:
            game.a, game.b, game.result = (game.tasks.pop()).values()
            game.number_example+=1
        except IndexError:
            return render(request, 'finish.html', {'result': game.total, 'mistakes': game.mistakes})
        return render(request,'trainer_app.html', {'a': game.a, 'b': game.b,
                                                   'result': game.result, 'number_task': game.number_example, 'tasks_deb':game.tasks, 'counter':Game.class_counter })

    def post(self, request):
        try:
            if int(request.POST.get('answer')) == game.result:
                messages.success(request, 'ПРАВИЛЬНО')

            elif int(request.POST.get('answer')) != game.result:
                messages.error(request, 'НЕ ПРАВИЛЬНО')
                game.mistakes += 1
                game.tasks.insert(0,{'a':game.a, 'b':game.b, 'result':game.result})

        except ValueError:
            return redirect(request.path)



        return redirect(request.path)

class Finish(View):
    def get(self, request):

        result, mistakes = game.total, game.mistakes


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
            Game.permission=True
        return redirect('start')






'''
class WorkOnMistakes(View):
    def post(self, request):
        mistake=TrainerApp.mistakes.pop()
        return render(request, 'trainer_app.html', {'a':mistake['a'], 'b':mistake['b'], 'result':mistake['result']})
'''

