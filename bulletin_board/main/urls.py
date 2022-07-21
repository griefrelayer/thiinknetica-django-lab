from django.urls import path, re_path, include, register_converter
from .views import IndexView, CarsView, CarDetailView, ThingsView, ThingDetailView, ServicesView, ServiceDetailView, \
    SellerUpdateView, CarCreateView, ThingCreateView, ServiceCreateView, CarUpdateView, ThingUpdateView, \
    ServiceUpdateView, UserProfileUpdate, SubscribeView, PhoneVerifyView, PhoneCodeVerifyView, SearchView
from django.contrib.flatpages import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .utils import UrlToModelConverter, trigger_error
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from .models import Car, Thing, Service
from rest_framework import routers
from .views import CarViewSet, ThingViewSet, ServiceViewSet, CategoryViewSet, SellerViewSet

# DRF
car_list = CarViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
car_detail = CarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

thing_list = ThingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
thing_detail = ThingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

service_list = ServiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
service_detail = ServiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

seller_list = SellerViewSet.as_view({
    'get': 'list'
})
seller_detail = SellerViewSet.as_view({
    'get': 'retrieve'
})

category_list = CategoryViewSet.as_view({
    'get': 'list'
})
category_detail = CategoryViewSet.as_view({
    'get': 'retrieve'
})

router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'things', ThingViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'categories', CategoryViewSet)

# Add custom url converter
register_converter(UrlToModelConverter, 'url_to_model')

# Constants
login_path = '/admin/login/'
cache_minutes_listview = 15
cache_minutes_detailview = 60

car_map = {
    'queryset': Car.objects.all(),
}

thing_map = {
    'queryset': Thing.objects.all(),
}

service_map = {
    'queryset': Service.objects.all(),
}

urlpatterns = [
                  path('api/v1/', include(router.urls)),
                  path('api/v1/cars', car_list, name='car-list'),
                  path('api/v1/cars/add', car_list, name='car-add'),
                  path('api/v1/cars/<int:pk>/', car_detail, name='car-detail'),
                  path('api/v1/cars/<int:pk>/edit', car_detail, name='car-update'),
                  path('api/v1/cars/<int:pk>/delete', car_detail, name='car-delete'),
                  path('api/v1/things', thing_list, name='thing-list'),
                  path('api/v1/things/add', thing_list, name='thing-add'),
                  path('api/v1/things/<int:pk>/', thing_detail, name='thing-detail'),
                  path('api/v1/things/<int:pk>/edit', thing_detail, name='thing-update'),
                  path('api/v1/things/<int:pk>/delete', thing_detail, name='thing-delete'),
                  path('api/v1/services', service_list, name='service-list'),
                  path('api/v1/services/add', service_list, name='service-add'),
                  path('api/v1/services/<int:pk>/', service_detail, name='service-detail'),
                  path('api/v1/services/<int:pk>/edit', service_detail, name='service-update'),
                  path('api/v1/services/<int:pk>/delete', service_detail, name='service-delete'),
                  path('api/v1/sellers/', seller_list, name='seller-list'),
                  path('api/v1/sellers/<int:pk>/', seller_detail, name='seller-detail'),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                  path('sitemap.xml', sitemap, {'sitemaps': {'flatpages': FlatPageSitemap,
                                                             'cars': GenericSitemap(car_map),
                                                             'things': GenericSitemap(thing_map),
                                                             'services': GenericSitemap(service_map),
                                                             }},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('sentry-debug/', trigger_error),
                  path('', IndexView.as_view(), name='index_page'),
                  path('about/', views.flatpage, {'url': '/about/'}, name='about'),
                  path('contact/', views.flatpage, {'url': '/contact/'}, name='contact'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('cars/', CarsView.as_view(), name='cars'),
                  re_path(r'^cars/(?P<pk>\d+)/$', CarDetailView.as_view(), name='car_detail'),
                  path('things/', cache_page(60 * cache_minutes_listview)(ThingsView.as_view()), name='things'),
                  re_path(r'^things/(?P<pk>\d+)/$',
                          cache_page(60 * cache_minutes_detailview)(ThingDetailView.as_view()), name='thing_detail'),
                  path('services/',
                       cache_page(60 * cache_minutes_listview)(ServicesView.as_view()), name='services'),
                  path('accounts/', include('allauth.urls')),
                  path('phone_verify/', PhoneVerifyView.as_view(), name='phone_verify'),
                  path('code_verify/', PhoneCodeVerifyView.as_view(), name='code_verify'),
                  path('accounts/seller/', login_required(SellerUpdateView.as_view(), login_url=login_path),
                       name='seller_update'),
                  path('accounts/user_profile/',
                       login_required(UserProfileUpdate.as_view(), login_url=login_path), name='user_profile_update'),
                  re_path(r'^search/[.]*$',
                          login_required(SearchView.as_view(), login_url=login_path), name='search'),
                  re_path(r'^services/(?P<pk>\d+)/$',
                          cache_page(60 * cache_minutes_detailview)(ServiceDetailView.as_view()),
                          name='service_detail'),
                  path('cars/add/', login_required(CarCreateView.as_view(), login_url=login_path), name='car_create'),
                  path('things/add/', login_required(ThingCreateView.as_view(), login_url=login_path),
                       name='thing_create'),
                  path('services/add/', login_required(ServiceCreateView.as_view(), login_url=login_path),
                       name='service_create'),
                  re_path(r'^cars/(?P<pk>\d+)/edit/$',
                          login_required(CarUpdateView.as_view(), login_url=login_path), name='car_update'),
                  re_path(r'^things/(?P<pk>\d+)/edit/$',
                          login_required(ThingUpdateView.as_view(), login_url=login_path), name='thing_update'),
                  re_path(r'^services/(?P<pk>\d+)/edit/$',
                          login_required(ServiceUpdateView.as_view(), login_url=login_path), name='service_update'),
                  re_path(r'^(?P<url_to_model>[\w-]+)/subscribe/$',
                          login_required(SubscribeView.as_view(), login_url=login_path), name='subscribe')
              ] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
