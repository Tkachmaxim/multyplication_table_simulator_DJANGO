import random
task=[]
gen_task=[]

def choice_number(n):
    num=0
    while num!=n:
        a = random.randrange(2, 10, 1)
        b = random.randrange(2, 10, 1)
        gen_task = dict(a=a, b=b, result=a*b)
        if gen_task not in task:
            num+=1
            task.append(gen_task)
    return task
