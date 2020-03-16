from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from .models import Thread, Reply

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'rychat/index.html'
    context_object_name = 'thread_index'

    def get_queryset(self):
        return Thread.objects.order_by('-date')


class ThreadView(generic.DetailView):
    model = Thread
    template_name = 'rychat/topic.html'
    context_object_name = 'thread_topic'


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
