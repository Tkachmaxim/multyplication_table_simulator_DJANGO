import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from Trainer import modulle
from Trainer.forms import MyResultForm

all_parameters = { 'permission': True,
                   'number_of_tasks': 0, 'action': '',
                   'total': 0, 'number_example': 0, 'mistakes': 0,
                   'total_for_save': 0, 'mistakes_for_save': 0, 'a': 0,'b':0, 'result':0, 'session':0}


class Start(View):

    def get(self, request):
        if all_parameters['permission']==False:
            return redirect('trainer_app')
        return render(request, 'index.html', {'all_parameters': all_parameters})



    def post(self, request):
        if all_parameters['permission']==True:
            try:
                if int(request.POST.get('number')) > 0 and request.POST.get('difficult') != None:
                        number_of_tasks=int(request.POST.get('number'))
                        action=request.POST.get('difficult')
                        all_parameters['number_of_tasks']=number_of_tasks
                        all_parameters['total']=number_of_tasks
                        all_parameters['action']=action
                        all_parameters['tasks']=modulle.choice_number(number_of_tasks,action)
                        all_parameters['session']+=1
                        all_parameters['permission']=False
            except ValueError:
                return redirect('start')
        else:
            return render(request, 'trainer_app.html', {'a': all_parameters['a'], 'b': all_parameters['b'],
                                                        'result': all_parameters['result'], 'number_task': all_parameters['number_example'],
                                                        'tasks_deb': all_parameters['tasks'], 'all_parameters':modulle.all_parameters})

        return redirect('trainer_app')



class TrainerApp(View):

    def get(self, request):
        #if number_example>=total:
        #    return redirect('finish')
        try:
            all_parameters['a'], all_parameters['b'], all_parameters['result'] = (all_parameters['tasks'].pop()).values()
            all_parameters['number_example']+=1
        except IndexError:
            return redirect(request.path)

        return render(request,'trainer_app.html', {'a': all_parameters['a'], 'b': all_parameters['b'],
                                                   'result': all_parameters['result'], 'number_task': all_parameters['number_example'], 'tasks_deb':all_parameters['tasks'], 'all_parameters':all_parameters})

    def post(self, request):
        try:
            if int(request.POST.get('answer')) == all_parameters['result']:
                messages.success(request, 'ПРАВИЛЬНО')


            elif int(request.POST.get('answer')) != all_parameters['result']:
                messages.error(request, 'НЕ ПРАВИЛЬНО')
                all_parameters['mistakes'] += 1
                all_parameters['tasks'].insert(0,{'a':all_parameters['a'], 'b':all_parameters['b'], 'result':all_parameters['result']})
        except ValueError:
            return redirect(request.path)

        if all_parameters['number_example'] >= all_parameters['total']:
            return redirect('finish')

        return redirect(request.path)

class Finish(View):
    def get(self, request):
        images=['https://upload.wikimedia.org/wikipedia/commons/4/4f/Tesla_Model_S_02_2013.jpg',
               'https://autoreview.ru/images/Article/1609/Article_160932_860_575.jpg',
               'https://auto.ironhorse.ru/wp-content/uploads/1977/11/412.jpg']
        result, mistakes = all_parameters['total'], all_parameters['mistakes']
        if mistakes/result<=0.2:
            image=images[0]
        elif 0.2<mistakes/result<0.4:
            image=images[1]
        else:
            image=images[2]
        if mistakes==0:
            return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':True, 'all_parameters':all_parameters})
        if mistakes>0 and all_parameters['session']==1:
            all_parameters['tasks']*=5
            all_parameters['session']+=1
        random.shuffle(all_parameters['tasks'])
        all_parameters['total'], all_parameters['mistakes'], all_parameters['number_example'] = len(all_parameters['tasks']), 0, 0
        return render(request, 'finish.html', {'result': result, 'mistakes': mistakes, 'image':image, 'button':False, 'all_parameters':all_parameters})

class Enter_Result(View):

    def get(self, request):
        form=MyResultForm
        return render(request, 'form.html', {'form':form, 'all_parameters': all_parameters})

    def post(self, request):
        form=MyResultForm(request.POST)

        if form.is_valid():
            total_save=all_parameters['total']
            total_mistakes_save=all_parameters['mistakes']
            example_mmistakes_save=tuple(all_parameters['tasks'])
            result=form.save(commit=False)
            result.total_tasks = total_save
            result.mistakes = total_mistakes_save
            result.examples_of_mistakes = example_mmistakes_save
            result.save()
            all_parameters['permission']=True
            all_parameters['number_of_tasks'],all_parameters['total'],all_parameters['number_example'],all_parameters['mistakes']=0,0,0,0
            all_parameters['total_for_save'], all_parameters['mistakes_for_save'], all_parameters['a'], all_parameters['b'], \
            all_parameters['result'], all_parameters['session']=0,0,0,0,0,0
            return redirect('start')
        return redirect('enter_result')






'''
class WorkOnMistakes(View):
    def post(self, request):
        mistake=TrainerApp.mistakes.pop()
        return render(request, 'trainer_app.html', {'a':mistake['a'], 'b':mistake['b'], 'result':mistake['result']})
'''

