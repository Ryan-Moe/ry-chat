from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Thread, Reply

# Create your views here.
def index(request):
    thread_index = Thread.objects.order_by('-date')
    context = {
        'thread_index' : thread_index,
    }
    return render(request, 'rychat/index.html', context)

def thread(request, thread_id):
    thread_topic = get_object_or_404(Thread, pk=thread_id)
    thread_replies = Thread.reply_set.order_by('date')
    context = {
        'thread_topic'      : thread_topic,
        'thread_replies'    : thread_replies,
    }
    return render(request, 'rychat/topic.html', context)
