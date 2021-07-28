def choice_number(self):
    while True:
        a = random.randrange(2, 10, 1)
        b = random.randrange(2, 10, 1)
            gen_task = [a,b]
            if gen_task not in task:
                break




        if self.with_div==1:
            self.task.append(self.gen_task)


        elif self.with_div == 2:


            if random.choice(['multi', 'divide']) == 'multi':
                self.task.append(self.gen_task)
            else:
                self.gen_task=[a*b,a]
                self.task.append(self.gen_task)


        elif self.with_div==3:
            self.gen_task = [a * b, a]
            self.task.append(self.gen_task)



    def show_number_of_tasks(self):

        if self.number_of_task>0:
            number = str(self.number_of_task)
        else:
            number=str(len(self.notcorrect))




        self.show_number_task = Label(self, font='arial 16', text=('Пример №' + number))
        self.show_number_task.grid(row=3, column=3)






    def make_widgets(self,data):

        self.show_number_of_tasks()
        self.check = time.time()
        self.first = str(data[-1][0])
        self.second = str(data[-1][1])
        if data[-1][0]<10:
            self.question =self.first+'*'+self.second+' = '
        else:
            self.question = self.first + ':' + self.second + ' = '

        self.info = Label(self,font='arial 16',text=self.question)
        self.info.grid(row=0,column=0,sticky=E)
        self.pe = Label(self, font='arial 16',text="Ответ")
        self.pe.grid(row=1, column=0, sticky=W)

        self.window_enter = Entry(self,font='arial 16')
        self.window_enter.focus()
        if self.number_of_task>0:
            self.window_enter.bind('<Return>', self.reveal)
        elif self.number_of_task==0:
            self.window_enter.bind('<Return>', self.reveal_on_mistakes)

        self.window_enter.grid(row=0, column=1, sticky=W)
        self.submit_but = Label(self,font='arial 16', text="Нажми Enter - чтобы ответит")
        self.submit_but.grid(row=2, column=0, sticky=W)


    def print_result(self,message):
        self.text_secret = Text(self, width=35, height=5, wrap=WORD)
        self.text_secret.grid(row=3, column=0, columnspan=2, sticky=W)
        self.text_secret.delete(0.0, END)
        self.text_secret.insert(0.0, message)


    def reveal(self,event):
        self.show_number_task.destroy()



        content = self.window_enter.get()
        a_answer=int(self.first)
        b_answer=int(self.second)
        if a_answer < 10:

            if a_answer*b_answer==int(content) and time.time()-self.check<11:
                message='Правильно! + 1 балл'
                self.print_result(message)

                self.ball+=1

            else:
                if  a_answer*b_answer!=int(content):
                    message = 'Не ПРАВИЛЬНО! УЧИ ТАБЛИЦУ УМНОЖЕНИЯ!!!'
                    self.print_result(message)

                elif time.time() - self.check > 11:

                    message = 'ОЧЕНЬ МЕДЛЕННО!!!'
                    self.print_result(message)
                n=0

                while n!=5:
                    self.notcorrect.append(self.gen_task)
                    n+=1

        else:
            if a_answer/b_answer == int(content) and time.time() - self.check < 11:
                message = 'Правильно! + 1 балл'
                self.print_result(message)

                self.ball += 1

            else:
                if a_answer/b_answer != int(content):
                    message = 'Не ПРАВИЛЬНО! УЧИ ТАБЛИЦУ УМНОЖЕНИЯ!!!'
                    self.print_result(message)

                elif time.time() - self.check > 11:

                    message = 'ОЧЕНЬ МЕДЛЕННО!!!'
                    self.print_result(message)
                n = 0

                while n != 5:
                    self.notcorrect.append(self.gen_task)
                    n += 1


        self.number_of_task-=1

        if self.number_of_task!=0:
            self.choice_number()
            self.info.destroy()
            self.make_widgets(self.task)
        else:
            if self.ball/self.total<0.8:

                message='Примеры закончились, Ваш результат:'+str(self.ball)+'\tПОКА НИКАКОГО КОМПЬЮТЕРА!!!'
            else:
                message='Примеры закончились, Ваш результат:'+str(self.ball)+'\t'+'Можно и поиграть, но делаем работу над ошибками!!!'
            self.mistakes=Label(self,text=('Количество ошибок:\t'+str(len(self.notcorrect)/5)))
            self.mistakes.grid(row=4,column=0)

            self.finish = Label(self, font='arial 20', text=message)
            self.finish.grid(row=6, column=0, columnspan=2, sticky=W)
            self.number_mistakes = len(self.notcorrect)/5
            self.work_on_mistakes()






    def work_on_mistakes(self):
        number_tasks=len(self.task)
        random.shuffle(self.notcorrect)
        self.show_number_task.destroy()
        self.info.destroy()




        if len(self.notcorrect)>0:
            self.check_mistake=time.time()

            self.make_widgets(self.notcorrect)





    def repeat(self):
        self.destroy()
        app1=Start(root)

    def reveal_on_mistakes(self,event):

        content = self.window_enter.get()
        a_answer=int(self.first)
        b_answer=int(self.second)
        self.show_number_task.destroy()
        if a_answer < 10:

            if a_answer*b_answer==int(content) and time.time()-self.check<11:
                message='Правильно! ОШИБКУ ВЫУЧИЛ'
                self.print_result(message)
                self.notcorrect.pop()


            else:
                if  a_answer*b_answer!=int(content):
                    message = 'Не ПРАВИЛЬНО! УЧИ ТАБЛИЦУ УМНОЖЕНИЯ!!!'
                    self.print_result(message)

                elif time.time() - self.check > 11:

                    message = 'ОЧЕНЬ МЕДЛЕННО!!!'
                    self.print_result(message)


        else:
            if a_answer/b_answer == int(content) and time.time() - self.check < 11:
                message = 'Правильно! ОШИБКУ ВЫУЧИЛ'
                self.print_result(message)
                self.notcorrect.pop()


            else:
                if a_answer/b_answer != int(content):
                    message = 'Не ПРАВИЛЬНО! УЧИ ТАБЛИЦУ УМНОЖЕНИЯ!!!'
                    self.print_result(message)

                elif time.time() - self.check > 11:

                    message = 'ОЧЕНЬ МЕДЛЕННО!!!'
                    self.print_result(message)




        if len(self.notcorrect)!=0:
            self.work_on_mistakes()
        else:

            self.info = Label(self,font='Arial-16',text='Работа над ошибками сделана!')
            self.info.grid(row=3, column=0, columnspan=2, sticky=W)
            t_me = time.asctime()
            print('mistakes:', self.number_mistakes, 'task:', self.number_of_task, t_me,
                  file=open('C:/Users/Максим/Desktop/математический тренажер/result.txt', 'a+'))



            self.repeat = Button(self, font='Arial 16', text='Попробовать еще раз?', command=self.repeat)
            self.repeat.grid(row=2, column=4)



root=Tk()
root.title("Тренажер таблицы умножения")
root.geometry("300x300")

app = Start(root)

root.mainloop()