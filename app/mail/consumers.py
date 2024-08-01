import datetime
import os
import json
import imaplib
import tempfile

from channels.generic.websocket import WebsocketConsumer
from django.core.files import File
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
import email
from email.header import decode_header

from .models import Attachment, Mail, Message


class WSConsumers(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        users = User.objects.all()
        if self.user not in users:
            self.user = users.get(id="1")
        mail_data = Mail.objects.get(user=self.user)
        email_address = mail_data.email
        password = mail_data.password

        if email_address.endswith("gmail.com"):
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
        elif email_address.endswith("yandex.ru"):
            mail = imaplib.IMAP4_SSL("imap.yandex.ru")
        elif email_address.endswith("mail.ru"):
            mail = imaplib.IMAP4_SSL("imap.mail.ru")
        else:
            pass
            # TODO дописать исключение
            # return "Invalid email address"
        mail.login(email_address, password)
        mail.select("inbox")
        result, data = mail.search(None, 'ALL')
        quantity = len(data[0].split())

        for index, num in enumerate(data[0].split()):
            result, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = decode_header(msg.get('Subject'))[0][0]
            date_tuple = email.utils.parsedate_tz(msg.get('Date'))
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple)).strftime('%Y-%m-%d %H:%M:%S')
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                content_type = part.get_content_type()
                try:
                    if content_type == 'text/plain':
                        content = part.get_payload(decode=True).decode('utf-8')
                except UnicodeDecodeError:
                    if content_type == 'text/plain':
                        content = part.get_payload(decode=True).decode('latin-1')
                try:
                    if type(subject) is not str:
                        subject = subject.decode('utf-8')
                except UnicodeDecodeError:
                    if type(subject) is not str:
                        subject = subject.decode('latin-1')

                message = Message(
                    user=self.user,
                    subject=subject,
                    sent_date=local_date,
                    received_date=local_date,
                    body=content
                    )
                message.save()

                if part.get_filename():
                    filename = part.get_filename()
                    filename = smart_str(filename)
                    filename = os.path.basename(filename)
                    with tempfile.TemporaryFile() as temp_file:
                        temp_file.write(part.get_payload(decode=True))
                        temp_file.seek(0)
                        instance = Attachment(file=File(temp_file, name=filename))
                        instance.save()
                        message.attachments.add(instance)
                else:
                    pass
            attachments = [attachment.file.name for attachment in message.attachments.all()]
            data = {
                    "index": index+1,
                    "quantity": quantity,
                    "subject": message.subject,
                    "sent_date": local_date,
                    "received_date": local_date,
                    "body": message.body,
                    "attachments": attachments
                }
            self.send(json.dumps(data))
