from django.urls import path, include

from . import views

app_name = 'rychat'
urlpatterns = [
   path('', views.IndexView.as_view(), name='index'),
   path('topic/<int:pk>/', views.ThreadView.as_view(), name='topic'),
   path('topic/<int:thread_id>/post/', views.post_reply, name='post'),
   path('account/', include('django.contrib.auth.urls')),
]
