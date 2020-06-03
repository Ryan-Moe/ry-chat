# Generated by Django 3.0.2 on 2020-06-02 05:33

from django.db import migrations

def names_to_ID(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    ryadmin = User.objects.get(username='admin')
    ryadmin.username = 'RyAdmin'
    ryadmin.save()

    Thread = apps.get_model('rychat', 'Thread')
    for thread in Thread.objects.all():
        thread.author = User.objects.get(username=thread.author).id
        thread.save()

    Reply = apps.get_model('rychat', 'Reply')
    for reply in Reply.objects.all():
        if reply.author == 'admin':
            reply.author = 'RyAdmin'
            reply.save()
        reply.author = User.objects.get(username=reply.author).id
        reply.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rychat', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(names_to_ID),
    ]
