from django.db import models
from django.contrib.auth.models import User


class Mail(models.Model):
    user = models.ForeignKey(
        User, related_name='mail', on_delete=models.CASCADE
    )
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username}'


class Message(models.Model):
    user = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(null=True, blank=True)
    body = models.TextField()
    attachments = models.ManyToManyField(
        'Attachment', related_name='messages', blank=True
    )

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')

    def __str__(self):
        return self.file.name
