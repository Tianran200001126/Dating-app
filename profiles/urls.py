from django.urls import path
from . import views

urlpatterns =[
    path('signup',views.signup,name='signup'),
    path('profiles',views.profile_list,name='profile_list'),
    path('chat/<int:other_user_id>/',views.chat,name='chat')
    ]