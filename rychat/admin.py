from django.contrib import admin

from .models import Thread, Reply

# Register your models here.


class ThreadAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'date']

admin.site.register(Thread, ThreadAdmin)
