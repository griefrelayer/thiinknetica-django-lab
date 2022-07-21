# gentestdata.py
from django.db import transaction
from django.core.management.base import BaseCommand

from main.factories import (
    UserFactory,
    CarFactory,
    ServiceFactory,
    ThingFactory,
    CategoryFactory,
    PictureFactory,
)
from main.utils import download_image_from_url

NUM_USERS = 0
NUM_CARS = 5
NUM_THINGS = 0
NUM_SERVICES = 0
NUM_CATEGORIES = 0
NUM_SELLERS = 0


class Command(BaseCommand):
    help = "Generates test data"
    ads = []
    tags = []

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Создаю тестовые данные в базе...")

        for _ in range(NUM_CATEGORIES):
            CategoryFactory()

        for _ in range(NUM_USERS):
            UserFactory()

        for _ in range(NUM_CARS):
            self.ads += [CarFactory()]

        for _ in range(NUM_THINGS):
            self.ads += [ThingFactory()]

        for _ in range(NUM_SERVICES):
            self.ads += [ServiceFactory()]

        for ad in self.ads:
            PictureFactory(ad=ad,
                           pic='uploads/ad_pics/' + download_image_from_url("https://picsum.photos/700/500"))
