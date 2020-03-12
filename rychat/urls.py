from django.urls import path

from . import views

app_name = 'rychat'
urlpatterns = [
   path('', views.index, name='index'),
   path('topic/<int:thread_id>/', views.thread, name='topic')
]
