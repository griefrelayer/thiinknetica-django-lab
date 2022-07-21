import random
import re
import string
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.apps import apps
from django.conf import settings
import vonage
from datetime import datetime
import os
import requests


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def random_4digit_num_generator():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def send_sms_code(phone, code):
    """Send sms via vonage library"""
    client = vonage.Client(key="some_key", secret="very_secret blah blah blah")
    sms = vonage.Sms(client)
    res = sms.send_message(
        {
            "from": "example.com",
            "to": phone,
            "text": f"Ваш код: {str(code)}",
            "type": "unicode"
        }
    )
    print(res["messages"][0])
    if res["messages"][0]["status"] == "0":
        return 0
    else:
        return f"Message failed with error: {res['messages'][0]['error-text']}"


def unique_slug_generator(instance, new_slug=None) -> str:
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def check_inn(inn) -> bool:
    """Проверка ИНН на подлинность"""
    if len(inn) not in (10, 12):
        return False

    def inn_csum(inn) -> str:
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(inn):], [int(x) for x in inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) == 10:
        return inn[-1] == inn_csum(inn[:-1])
    else:
        return inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])


def validate_inn(inn):
    """INN validator"""
    if not check_inn(inn):
        raise ValidationError(_('ИНН %(inn)s - неправильный! Введите правильный ИНН!'), params={'inn': inn})


class UrlToModelConverter:
    regex = r'[\w-]+'

    def to_python(self, value):
        model_names = [x.__name__ for x in list(apps.get_app_config('main').get_models())]
        model = str(value)[:-1].title()
        if model in model_names:
            return value
        else:
            raise Http404


TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def download_image_from_url(pic_url):
    upload_dir = os.path.join(os.path.join(settings.MEDIA_ROOT, 'uploads'), 'car_pics')
    now_filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + ".jpg"
    image_filename = os.path.join(upload_dir, now_filename)
    with open(image_filename, 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return now_filename


def trigger_error(request):
    return 1/0