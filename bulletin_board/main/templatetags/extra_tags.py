from django import template
from ..models import Seller, Subscriber
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


register.simple_tag(lambda x: x[::-1], name='reverse_text')   # Created custom template tag reverse_text


@register.filter(name='range')
def get_range(start, end):
    try:
        return range(start, end + 1)
    except TypeError:
        return []


@register.filter(name='get_fields')
def get_fields(obj):
    """Returns obj's list of fields"""
    return [(obj.__class__._meta.get_field(x.name).verbose_name,
             getattr(obj, x.name)) for x in obj.__class__._meta.local_fields]


@register.filter(name='has_seller')
def has_seller(user):
    try:
        res = Seller.objects.get(user_ptr=user.id).id
    except ObjectDoesNotExist:
        res = None
    return user.id == res


@register.filter(name='has_subscription')
def has_subscription(user, value):
    """Checks if :param user: has subscription to :param value:
    :returns: True or False"""
    res = Subscriber.objects.filter(user=user, subscribed_to=value).count()
    return bool(res)
