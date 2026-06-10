from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('session/start/', views.session_start, name='session_start'),
    path('session/<int:session_id>/question/<int:question_order>/', views.question_view, name='question_view'),
    path('session/<int:session_id>/question/<int:question_order>/submit/', views.question_submit, name='question_submit'),
    path('session/<int:session_id>/question/<int:question_order>/feedback/', views.question_feedback, name='question_feedback'),
    path('session/<int:session_id>/results/', views.results_view, name='results_view'),
    path('session/<int:session_id>/pdf/', views.download_pdf, name='download_pdf'),
    path('chat/start/', views.chat_start, name='chat_start'),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
    path('chat/<int:chat_id>/send/', views.chat_send, name='chat_send'),
]
