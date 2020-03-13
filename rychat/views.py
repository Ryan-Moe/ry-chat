from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
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
    thread_replies = thread_topic.reply_set.order_by('date')
    context = {
        'thread_topic'      : thread_topic,
        'thread_replies'    : thread_replies,
    }
    return render(request, 'rychat/topic.html', context)

def post_reply(request, thread_id):
    thread_topic = get_object_or_404(Thread, pk=thread_id)
    reply_text = request.POST['message']
    reply_text = reply_text[:1024]

    r = Reply(thread=Thread.objects.get(pk=thread_id),
        text=reply_text,
        date=timezone.now(),
        author="RyAdmin")
    r.save()
    return HttpResponseRedirect(reverse('rychat:topic', args=(thread_id,)))
