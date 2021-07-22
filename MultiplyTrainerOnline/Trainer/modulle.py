import random
task=[]
gen_task=[]

def choice_number(n,action):
    if action=='multi':
        num=0
        while num!=n:
            gen_task=set_multy()
            if  gen_task not in task:
                num+=1
                task.append(gen_task)
        return task

    if action=='divide':
        num = 0
        while num != n:
           gen_task=set_divide()
           if gen_task not in task:
                num += 1
                task.append(gen_task)
        return task

    if action=='complex':
        num = 0
        while num != n:
            gen_task=random.choice([set_divide(), set_multy()])
            print(gen_task)
            if gen_task not in task:
                num += 1
                task.append(gen_task)
        return task

def set_multy():
    a = random.randrange(2, 10, 1)
    b = random.randrange(2, 10, 1)
    task_ = str(a) + ' × ' + str(b)
    gen_task = dict(a=task_, b=b, result=a * b)
    return gen_task

def set_divide():
    a = random.randrange(2, 10, 1)
    b = random.randrange(2, 10, 1)
    task_ = str(a * b) + ':' + str(b)
    gen_task = dict(a=task_, b=b, result=a)
    return gen_task