# Create your tasks here

from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def email_subs_on_new_ad(model_name, pk, emails):
    send_mail("Новое объявление на example.com",
              '', 'admin@example.com',
              emails,
              html_message='Ранее вы подписались на новые объявления. Новое объявление было добавлено. \
              <a href="http://example.com' + f'{reverse(model_name + "_detail", args=(pk,))}">Посмотреть объявление</a>'
              )


@shared_task
def mail_about_new_ads(interval_kwargs):
    from .models import Car, Thing, Service, Subscriber
    print('inside mail_about_new_ads task...')
    # Your job processing logic here...
    now_time = now()
    print("Starting mail_about_new_ads scheduled job at:", now_time.time())
    prev_time = now_time - timedelta(**interval_kwargs)
    cars = '<br>\n'.join([f'<a href="http://localhost:8000/cars/{str(c.id)}">{c.name}</a>'
                          for c in Car.objects.filter(datetime_created__range=[prev_time, now_time])])
    things = '<br>\n'.join([f'<a href="http://localhost:8000/things/{str(t.id)}">{t.name}</a>'
                            for t in Thing.objects.filter(datetime_created__range=[prev_time, now_time])])
    services = '<br>\n'.join([f'<a href="http://localhost:8000/services/{str(s.id)}">{s.name}</a>'
                              for s in Service.objects.filter(datetime_created__range=[prev_time, now_time])])

    if cars or things or services:
        subs: dict[str, list[str]] = dict()
        for s in Subscriber.objects.all():
            if not subs.get(s.user.email):
                subs[s.user.email] = [s.subscribed_to]
            else:
                subs[s.user.email] += [s.subscribed_to]
        for email, subs_list in subs.items():
            send_mail("Новые объявления на example.com",
                      '', 'admin@example.com',
                      [email],
                      html_message='Ранее вы подписались на новые объявления. Новые объявления были добавлены:<br>\n'
                                   + eval("<br>".join(subs_list)))
