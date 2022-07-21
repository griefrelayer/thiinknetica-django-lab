import factory
import random
from main.utils import download_image_from_url
from django.conf import settings

from factory.django import DjangoModelFactory

from .models import User, Car, Thing, Service, Category, Seller, Picture, Ad
from .utils import inn_gen


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker("sentence", nb_words=3)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("user_name")
    email = factory.Faker("ascii_safe_email")
    phone_number = "+7" + str(random.randint(1000000000, 9999999999))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False


class SellerFactory(DjangoModelFactory):
    class Meta:
        model = Seller
    username = factory.Faker("user_name")
    inn = inn_gen()
    email = factory.Faker("ascii_safe_email")
    phone_number = "+7" + str(random.randint(1000000000, 9999999999))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car
    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    mileage = random.randint(1, 500000)
    brand = random.choice(['BMW', 'Mercedes', 'Volkswagen', 'Opel', 'Bugatti', 'Лада', 'Hyundai', 'Toyota', 'Kia'])
    color = factory.Faker("color_name")
    seller = factory.SubFactory(SellerFactory)
    is_sold = False
    price = random.randrange(100000, 15000000, 10000)
    tags = factory.Faker("words", nb=random.randint(1, 6))

    '''@factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted)-1)]
                self.tags.add(tag)
'''


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service
    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    area = factory.Faker('city')
    seller = factory.SubFactory(SellerFactory)
    is_sold = False
    tags = factory.Faker("words", nb=random.randint(1, 6))

    '''@factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted) - 1)]
                self.tags.add(tag)'''


class ThingFactory(DjangoModelFactory):
    class Meta:
        model = Thing
    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    weight = random.randrange(0, 1500, 10)
    size = random.choice(['small', 'average', 'big', 'huge'])
    seller = factory.SubFactory(SellerFactory)
    is_sold = False
    tags = factory.Faker("words", nb=random.randint(1, 6))

    '''@factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            rnd = random.randint(1, 4)
            for i in range(min(rnd, len(extracted))):
                tag = extracted[random.randint(0, len(extracted) - 1)]
                self.tags.add(tag)'''


class PictureFactory(DjangoModelFactory):
    class Meta:
        model = Picture

    ad = Ad.objects.last()

    def __init__(self):
        get_pic = download_image_from_url("https://picsum.photos/700/500")
        if get_pic:
            self.pic = 'uploads/ad_pics/' + download_image_from_url("https://picsum.photos/700/500")
        else:
            self.pic = 'uploads/ad_pics/default_ad.jpg'
        super().__init__()



