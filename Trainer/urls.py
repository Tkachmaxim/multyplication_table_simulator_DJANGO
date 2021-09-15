from django.urls import path
from Trainer.views import Start, TrainerApp, Finish, Enter_Result

app_name='mathtrainer'

urlpatterns = [
    path('', Start.as_view(), name='math_start'),
    path('trainer/', TrainerApp.as_view(), name='trainer_app'),
    path('finish/', Finish.as_view(), name='finish'),
    path('sent_result/', Enter_Result.as_view(), name='enter_result'),
    ]
