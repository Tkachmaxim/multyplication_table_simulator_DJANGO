import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from Trainer import modulle
from Trainer.models import Game
from Trainer.forms import MyResultForm




class Start(View):


    def get(self, request):
        try:
            game=Game.objects.order_by('id')[0]
            if game.permission==False:
                return redirect('trainer_app')
        except IndexError:
            return render(request, 'index.html')

        return render(request, 'index.html')



    def post(self, request):
            try:
                if int(request.POST.get('number')) > 0 and request.POST.get('difficult') != None:
                        number_of_tasks=int(request.POST.get('number'))
                        action=request.POST.get('difficult')
                        game=Game(permission=False, number_of_tasks=number_of_tasks, total=number_of_tasks,
                                  action=action, tasks=modulle.choice_number(number_of_tasks,action), session=1,
                                  mistakes=0,  total_for_save=0, mistakes_for_save=0)
                        game.save()

            except ValueError:
                return redirect('start')


            return redirect('trainer_app')



class TrainerApp(View):

    def get(self, request):
        #if number_example>=total:
        #    return redirect('finish')
        try:
            data=Game.objects.order_by('id')[0]
            all_tasks = data.tasks
            a, b, result = all_tasks[:].pop().values()

        except IndexError:
            return redirect('finish')


        return render(request,'trainer_app.html', {'a': a, 'b': b,
                                                   'result': result, 'number_task': data.number_example})

    def post(self, request):
        try:
            data = Game.objects.order_by('id')[0]
            try:
                a, b, result = data.tasks.pop().values()
            except IndexError:
                return redirect('finish')

            if int(request.POST.get('answer')) == int(result):
                messages.success(request, 'ПРАВИЛЬНО')

            elif int(request.POST.get('answer')) != int(result):
                messages.error(request, 'НЕ ПРАВИЛЬНО')
                data.mistakes+= 1
                data.tasks.insert(0,{'a': a, 'b': b, 'result': result})


        except ValueError:
            return render(request, 'trainer_app.html', { 'a': a, 'b': b,
                                                         'result': result, 'number_task': data.number_example })


        data.number_example += 1
        if data.number_example == data.total+1:
            data.save()
            return redirect('finish')
        data.save()


        return redirect(request.path)

class Finish(View):
    def get(self, request):
        data=Game.objects.order_by('id')[0]
        images=['https://upload.wikimedia.org/wikipedia/commons/4/4f/Tesla_Model_S_02_2013.jpg',
               'https://autoreview.ru/images/Article/1609/Article_160932_860_575.jpg',
               'https://auto.ironhorse.ru/wp-content/uploads/1977/11/412.jpg']
        result, mistakes = data.total, data.mistakes
        if mistakes/result<=0.2:
            image=images[0]
        elif 0.2<mistakes/result<0.4:
            image=images[1]
        else:
            image=images[2]
        if mistakes==0:
            return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':True})


        if mistakes>0 and data.session==1:
            data.mistakes_examples=data.tasks[:]
            data.tasks*=5
            data.session+=1



        random.shuffle(data.tasks)
        data.total, data.mistakes, data.number_example = len(data.tasks), 0, 1
        data.save()
        return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':False})

class Enter_Result(View):

    def get(self, request):
        form=MyResultForm
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form=MyResultForm(request.POST)
        data=Game.objects.order_by('id')[0]

        if form.is_valid():
            total_save=data.total
            total_mistakes_save=data.mistakes

            result=form.save(commit=False)
            result.total_tasks = total_save
            result.mistakes = total_mistakes_save
            result.examples_of_mistakes = data.mistakes_examples
            result.save()
            data.delete()
            return redirect('start')

        return redirect('enter_result')


