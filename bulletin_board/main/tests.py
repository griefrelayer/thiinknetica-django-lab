from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Seller, Car, Thing, Service, Category, Tag
from django.urls import reverse

User = get_user_model()
# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser136',
            email='testuser1@email.com',
            password='testpass136',
        )

        self.user2 = User.objects.create_user(
            username='testuser257',
            email='testuser2@email.com',
            password='testpass257',
        )

        self.client.force_login(self.user)

        self.seller = Seller.objects.create(username='NewSellerUsername1')

        self.seller2 = Seller.objects.create(username='NewSellerUsername2')

        self.category = Category.objects.create(
            name='TestCategory1'
        )

        self.category2 = Category.objects.create(
            name='TestCategory2'
        )

        self.tag = Tag.objects.create(
            name='TestTag1'
        )

        self.tag2 = Tag.objects.create(
            name='TestTag2'
        )
        self.car_ad = Car.objects.create(
            name='TestAd1',
            description='This is test1 Ad object description',
            category=self.category,
            seller=self.seller,
            mileage=500,
            brand='BMW',
            color='dark green'
        )

        self.car_ad.tags.add(self.tag)

        self.car_ad2 = Car.objects.create(
            name='TestAd2',
            description='This is test2 Ad object description',
            category=self.category2,
            seller=self.seller2,
            mileage=600,
            brand='Volkswagen',
            color='light blue'
        )

        self.car_ad2.tags.add(self.tag2)

        self.thing_ad = Thing.objects.create(
            name='TestThingAd1',
            description='Test',
            category=self.category,
            seller=self.seller,
            weight=15,
            size='100x100'
        )

        self.service_ad = Service.objects.create(
            name='TestThingAd1',
            description='Test',
            category=self.category,
            seller=self.seller,
            area='near'
        )

    def test_views_response_status_codes(self):
        """Test views response status codes"""
        views_names = ['cars', 'things', 'services', 'index_page', 'car_create', 'thing_create', 'service_create']
        for vn in views_names:
            response = self.client.get(reverse(vn), )
            self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(reverse('car_detail', kwargs={'pk': self.car_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('thing_detail', kwargs={'pk': self.thing_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('service_detail', kwargs={'pk': self.service_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('car_update', kwargs={'pk': self.car_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('thing_update', kwargs={'pk': self.thing_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('service_update', kwargs={'pk': self.service_ad.id})).status_code, 200)
        self.assertEqual(self.client.get(reverse('subscribe', kwargs={'url_to_model': 'cars'})).status_code, 302)

    def test_users(self):
        """Test users"""
        self.assertEqual(self.user, User.objects.first(), 'no user!')
        self.assertIn(self.user2, User.objects.all(), 'no user2!')
        self.user2.username = 'testuser2_test_edit'
        self.assertNotEqual(User.objects.get(email='testuser2@email.com').username, 'testuser2_test_edit')
        self.user2.save()
        self.assertEqual(User.objects.get(email='testuser2@email.com').username, 'testuser2_test_edit')

    def test_sellers(self):
        """Test sellers"""
        self.assertIn(self.seller, Seller.objects.all(), 'no seller')
        self.assertIn(self.seller2, Seller.objects.filter(user_ptr__username__startswith='NewSellerUsername'), 'cant find seller2')

    def test_categories(self):
        """Test categories"""
        self.assertEqual(2, Category.objects.filter(name__startswith='TestCategory').count(), 'categories count not equal')

    def test_tags(self):
        """Test tags"""
        t = Tag(name='TestTag3')
        t.save()
        self.assertIn(self.car_ad, Car.objects.filter(id=self.tag.ad_set.first().id), 'tag problem')
        qs = Car.objects.all()
        for ad in qs:
            ad.tags.add(t)
        self.assertEqual(list(qs), list(Car.objects.filter(tags=t)), 'tags not equal')

    def test_ads(self):
        """Test ads"""
        self.test_tags()    # To add TestTag3 to all Ad objects
        ad = Car.objects.get(seller__user_ptr__username='NewSellerUsername1')
        self.assertEqual(ad.category, self.category)
        qs = ad.tags.all().values_list('name', flat=True)
        self.assertIn('TestTag1', qs)
        self.assertIn('TestTag3', qs)
        self.assertEqual(ad.category.name, 'TestCategory1')
        new_ad = Car.objects.create(
            name='TestAd3',
            description='This is test1 Ad object description',
            category=self.category,
            seller=self.seller,
            mileage=12345,
            brand='unitaz',
            color='serburmalin'
        )

        new_ad.tags.add(self.tag)

        new_ad2 = Car(
            name='TestAd4',
            description='This is test1 Ad object description',
            category=self.category2,
            seller=self.seller2,
            mileage=12345,
            brand='unitaz',
            color='serburmalin'
        )
        new_ad2.save()
        new_ad2.tags.add(self.tag2)
        self.assertEqual(['TestAd1', 'TestAd3'],
                         list(Car.objects.filter(category=self.category).values_list('name', flat=True)))
        self.assertEqual(['TestAd2', 'TestAd4'],
                         list(Car.objects.filter(category=self.category2).values_list('name', flat=True)))
