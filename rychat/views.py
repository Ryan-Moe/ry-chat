from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.request.user.has_perm('rychat.delete_reply')
        context['can_delete_threads'] = self.request.user.has_perm('rychat.delete_thread')
        return context

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
        author=request.user)
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
        author=request.user)
    r.save()

    return HttpResponseRedirect(reverse('rychat:topic', args=(r.id,)))

# Checks whether user is the same that posted the reply
# and if so deletes it.
@login_required
def delete_reply(request, reply_id):
    theReply = get_object_or_404(Reply, pk=reply_id)
    thread_id = theReply.thread.id
    theUser = request.user

    if theUser == theReply.author or theUser.has_perm('rychat.delete_reply'):
        theReply.delete()

    return HttpResponseRedirect(reverse('rychat:topic', args=(thread_id,)))

# Checks whether user is the same that posted the thread
# and if so deletes it.
@login_required
def delete_thread(request, thread_id):
    theThread = get_object_or_404(Thread, pk=thread_id)
    theUser = request.user

    if theUser == theReply.author or theUser.has_perm('rychat.delete_thread'):
        theReply.delete()

    return HttpResponseRedirect(reverse('rychat:index'))

# A page with a text box for editing post text,
# and handling of the resulting POST action.
@login_required
def edit_reply(request, reply_id):
    theReply = get_object_or_404(Reply, pk=reply_id)
    thread_id = theReply.thread.id
    theUser = request.user

    if theUser == theReply.author:
        if request.method == 'POST':
            reply_text = request.POST['message']
            theReply.text = reply_text[:1024]
            theReply.edited = timezone.now()
            theReply.save()
        else:
            return render(request, 'rychat/edit.html', {'reply': theReply, 'thread_id': thread_id})

    return HttpResponseRedirect(reverse('rychat:topic', args=(thread_id,)))

# A page with a text box for editing thread text and title,
# and handling of the resulting POST action.
@login_required
def edit_thread(request, thread_id):
    theThread = get_object_or_404(Thread, pk=thread_id)
    theUser = request.user

    if theUser == theThread.author:
        if request.method == 'POST':
            thread_title = request.POST['title']
            theThread.title = thread_title[:256]
            thread_text = request.POST['message']
            theThread.text = thread_text[:1024]
            theThread.edited = timezone.now()
            theThread.save()
        else:
            return render(request, 'rychat/edit.html', {'thread': theThread, 'thread_id': theThread.id})

    return HttpResponseRedirect(reverse('rychat:topic', args=(thread_id,)))

# Renders the page for the new user registration form.
# Upon successful registration, logs the user in and
# redirects them back to the site.
def signup(request):
    next = ""
    if request.GET:
        next = request.GET['next']

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('rychat:index'))

    if request.method == 'POST':
        next = request.POST['next']
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if next == "":
                next = reverse('rychat:index')
            return HttpResponseRedirect(next)
    else:
        form = UserCreationForm()

    return render(request, 'rychat/signup.html', {'form': form, 'next': next})
