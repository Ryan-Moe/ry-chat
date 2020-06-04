from django.urls import path, include

from . import views

app_name = 'rychat'
urlpatterns = [
   path('', views.IndexView.as_view(), name='index'),
   path('topic/<int:pk>/', views.ThreadView.as_view(), name='topic'),
   path('topic/<int:thread_id>/post/', views.post_reply, name='post'),
   path('newthread/', views.post_thread, name='newthread'),
   path('deletethread/<int:thread_id>/', views.delete_thread, name="deletethread"),
   path('delete/<int:reply_id>/', views.delete_reply, name="delete"),
]
