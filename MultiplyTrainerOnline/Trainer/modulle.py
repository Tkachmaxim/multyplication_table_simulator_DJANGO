import random
task=[]
gen_task=[]

def choice_number():
    while True:
        a = random.randrange(2, 10, 1)
        b = random.randrange(2, 10, 1)
        gen_task = [a,b]
        if gen_task not in task:
            break
    task.append(gen_task)
    result=a*b
    return a,b,result