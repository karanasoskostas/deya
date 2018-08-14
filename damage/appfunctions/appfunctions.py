from damage.models import General, Damage
from django.conf import settings
from django.template import loader
from damage.utils.utils import *


def damage_mail(pk):
    damage = Damage.objects.get(pk=pk)
    general = General.objects.get(pk=1)

    if not damage:
        return

    subject = 'Καταχώρηση Νέας Βλάβης'
    message = 'Here is the message.'
    senderemail = settings.EMAIL_HOST_USER
    receivers = [damage.email, settings.EMAIL_HOST_USER]
    template = 'damage/email/addmail.html'
    args = {
        'damage': damage,
        'general': general
    }
    html_message = loader.render_to_string(template, args)

    email_to_send = (subject, message, senderemail, receivers)


    #send_mass_html_mail(subject, message, html_message, senderemail, receivers)
    send_html_mail(subject, html_message, receivers, senderemail)

    # send_mass_mail((email_to_send,) επειδή argument is a tuple of message tuples !!!!

    # η send_mass_mail δεν εχει html_message ως argument

    #send_mass_mail((email_to_send,), fail_silently=False, html_message=html_message)

    # send_mass_mail() uses a single connection for all of its messages.
    # This makes send_mass_mail() slightly more efficient.

    return