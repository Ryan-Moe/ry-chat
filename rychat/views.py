from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Thread, Reply

# View for the front page of the site.
# Lists all thread titles stored in the database.
# Based on django's generic list view.
class IndexView(generic.ListView):
    template_name = 'rychat/index.html'
    context_object_name = 'thread_index'

    def get_queryset(self):
        return Thread.objects.order_by('-date')

# View for the individual page of each thread.
# Provides the particular thread's information to the template.
# Based on django's generic detail view.
class ThreadView(generic.DetailView):
    model = Thread
    template_name = 'rychat/topic.html'
    context_object_name = 'thread_topic'

# Handles new replies as posted from the thread view page.
# Takes the author's name as well as the reply's body text,
#creates a Reply object from it, connects it to the thread,
# then finally redirects the user to the thread view.
@login_required
def post_reply(request, thread_id):
    thread_topic = get_object_or_404(Thread, pk=thread_id)
    reply_text = request.POST['message']
    reply_text = reply_text[:1024]

    r = Reply(thread=thread_topic,
        text=reply_text,
        date=timezone.now(),
        author=request.user.username)
    r.save()

    return HttpResponseRedirect(reverse('rychat:topic', args=(thread_id,)))

# Handles new threads as posted from the index view page.
# Takes the author's name as well as the reply's body text,
#creates a Reply object from it, connects it to the thread,
# then finally redirects the user to the thread view.
@login_required
def post_thread(request):
    thread_title = request.POST['title']
    thread_title = thread_title[:256]
    thread_text = request.POST['message']
    thread_text = thread_text[:1024]

    r = Thread(title=thread_title,
        text=thread_text,
        date=timezone.now(),
        author=request.user.username)
    r.save()

    return HttpResponseRedirect(reverse('rychat:topic', args=(r.id,)))
