from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from .forms import SellerForm, CarForm, ServiceForm, ThingForm, PictureFormset, UserProfileForm
from constance import config
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, View
from .models import Car, Thing, Service, Seller, Picture, Subscriber, SMSLog, Ad, Category
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .utils import random_4digit_num_generator, send_sms_code
import random
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CarSerializer, ThingSerializer, ServiceSerializer, CategorySerializer, SellerSerializer

# API permissions


class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.seller.id == request.user.id or request.user.is_staff:
            return True
        else:
            return False

# API views


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Car ads to be viewed or edited.
    """
    queryset = Car.objects.all().order_by('-datetime_created')
    serializer_class = CarSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned Car object list to a given color, brand or name
        by filtering against a `name`, `color`, `brand` query parameters in the URL.
        """
        queryset = Car.objects.all()
        name = self.request.query_params.get('name')
        color = self.request.query_params.get('color')
        brand = self.request.query_params.get('brand')

        if name:
            queryset = queryset.filter(name=name)
        if color:
            queryset = queryset.filter(color=color)
        if brand:
            queryset = queryset.filter(brand=brand)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsCreatorOrAdmin]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ThingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Thing ads to be viewed or edited.
    """
    queryset = Thing.objects.all().order_by('-datetime_created')
    serializer_class = ThingSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned Thing object list to a given size, weight or name
        by filtering against a `name`, `color`, `brand` query parameters in the URL.
        """
        queryset = Thing.objects.all()
        name = self.request.query_params.get('name')
        size = self.request.query_params.get('size')
        weight = self.request.query_params.get('weight')

        if name:
            queryset = queryset.filter(name=name)
        if size:
            queryset = queryset.filter(size=size)
        if weight:
            queryset = queryset.filter(weight=weight)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsCreatorOrAdmin]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Service ads to be viewed or edited.
    """
    queryset = Service.objects.all().order_by('-datetime_created')
    serializer_class = ServiceSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned Service object list to a given area or name
        by filtering against a `name`, `area` query parameters in the URL.
        """
        queryset = Service.objects.all()
        name = self.request.query_params.get('name')
        area = self.request.query_params.get('area')

        if name:
            queryset = queryset.filter(name=name)
        if area:
            queryset = queryset.filter(area=area)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsCreatorOrAdmin]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Category ads to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Seller accounts to be viewed or edited.
    """
    queryset = Seller.objects.all().order_by('username')
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAdminUser]
# Web views


class CustomCreateView(CreateView):
    """CustomCreateView is for overriding all CreateView classes at once"""

    def form_valid(self, form):
        if self.request.user.groups.filter(name='banned_users').exists():
            raise PermissionDenied(_("Ошибка 403. Вы забанены, поэтому не можете отправлять объявления."))
        else:
            return super().form_valid(form)


class IndexView(TemplateView):
    """Main page view"""
    context_object_name = 'index_page'
    template_name = 'index.html'
    turn_on_block = config.MAINTENANCE_MODE


class AbstractAdListView(ListView):
    """Common ListView parameters and methods"""
    paginate_by = 10

    def get_queryset(self):
        tag_filter = self.request.GET.get('tag', [])
        if tag_filter:
            new_context = self.model.objects.filter(tags__contains=[tag_filter])
        else:
            new_context = self.model.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.request.GET.get('tag', [])
        context['ad_list_name'] = self.model._meta.model_name + 's'
        return context


class SearchView(AbstractAdListView):
    """Name and description search on ads"""
    model = Ad
    template_name = "main/search.html"
    context_object_name = 'ads'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if q:
            vector = SearchVector('name', 'description')
            query = SearchQuery(q)
            context = self.model.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        else:
            context = self.model.objects.all()

        tag_filter = self.request.GET.get('tag', [])
        if tag_filter:
            new_context = context.filter(tags__contains=[tag_filter])
        else:
            new_context = context.all()
        return new_context


class CarsView(AbstractAdListView):
    """Cars root category view"""

    model = Car
    template_name = "main/cars.html"
    context_object_name = 'cars'


class AbstractAdDetailView(DetailView):
    """Common methods and parameters for DetailView classes"""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            pic = Picture.objects.filter(ad=self.get_object()).last()
        except ObjectDoesNotExist:
            pic = None
        data['picture'] = pic
        return data


class CarDetailView(AbstractAdDetailView):
    """Detailed car ad view"""
    model = Car
    template_name = "main/car_detail_view.html"

    def get_object(self):
        self.ad = get_object_or_404(Car, id=self.kwargs['pk'])
        self.ad.price = round(random.randrange(80, 120, 1) / 100 * self.ad.price)  # random price multiply 0.8x to 1.2x
        return self.ad


class ThingsView(AbstractAdListView):
    """Things root category view"""
    model = Thing
    template_name = "main/things.html"


class ThingDetailView(AbstractAdDetailView):
    """Thing detailed view"""
    model = Thing
    template_name = "main/thing_detail_view.html"


class ServicesView(AbstractAdListView):
    """Services root category view"""
    model = Service
    template_name = "main/services.html"


class ServiceDetailView(AbstractAdDetailView):
    """Detailed service view"""
    model = Service
    template_name = "main/service_detail_view.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            pic = Picture.objects.filter(ad=self.get_object()).last()
        except ObjectDoesNotExist:
            pic = None
        data['picture'] = pic
        return data


class SellerUpdateView(UpdateView):
    """Editing seller data form"""
    model = Seller
    form_class = SellerForm
    template_name = "main/seller_update_view.html"

    def get_object(self, queryset=None):
        seller, _ = Seller.objects.get_or_create(user_ptr=self.request.user)
        return seller

    def get_success_url(self):
        return reverse('seller_update')


class UserProfileUpdate(UpdateView):
    """User profile editing view"""
    model = User
    form_class = UserProfileForm
    template_name = 'main/user_profile_update_view.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('user_profile_update')


class CarCreateView(CustomCreateView):
    """Add new Car ads"""
    model = Car
    form_class = CarForm
    template_name = 'main/ad_create.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        context = self.get_context_data()
        picture_forms = context['picture_forms']
        self.object = form.save()
        if picture_forms.is_valid():
            picture_forms.instance = self.object
            picture_forms.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('car_update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['picture_forms'] = PictureFormset(self.request.POST, self.request.FILES)
        else:
            data['picture_forms'] = PictureFormset()
        return data


class ThingCreateView(CustomCreateView):
    """Add new Thing ads"""
    model = Thing
    form_class = ThingForm
    template_name = 'main/ad_create.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('thing_update', kwargs={'pk': self.object.pk})


class ServiceCreateView(CustomCreateView):
    """Add new Service ads"""
    model = Service
    form_class = ServiceForm
    template_name = 'main/ad_create.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('service_update', kwargs={'pk': self.object.pk})


class CarUpdateView(UpdateView):
    """Edit Car ads"""
    model = Car
    form_class = CarForm
    template_name = 'main/ad_update.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        context = self.get_context_data()
        picture_forms = context['picture_forms']
        if picture_forms.is_valid():
            picture_forms.instance = self.object
            picture_forms.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('car_update', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return get_object_or_404(Car, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['picture_forms'] = PictureFormset(self.request.POST, self.request.FILES)
        else:
            data['picture_forms'] = PictureFormset()
        try:
            pic = Picture.objects.filter(car=self.get_object()).last()
        except ObjectDoesNotExist:
            pic = None
        data['picture'] = pic
        return data


class ThingUpdateView(UpdateView):
    """Edit Thing ads"""
    model = Thing
    form_class = ThingForm
    template_name = 'main/ad_update.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('thing_update', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return get_object_or_404(Thing, id=self.kwargs['pk'])


class ServiceUpdateView(UpdateView):
    """Edit Service ads"""
    model = Service
    form_class = ServiceForm
    template_name = 'main/ad_update.html'

    def form_valid(self, form):
        form.instance.seller = Seller.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('service_update', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return get_object_or_404(Service, id=self.kwargs['pk'])


class SubscribeView(View):
    """Subscribe or unsubscribe to new ads"""

    def get(self, request, *args, **kwargs):
        qs = Subscriber.objects.filter(user=request.user, subscribed_to=kwargs['url_to_model'])
        if qs.count():
            qs.delete()
        else:
            Subscriber(user=request.user, subscribed_to=kwargs['url_to_model']).save()

        return HttpResponseRedirect(reverse(self.kwargs['url_to_model']))


@method_decorator(csrf_exempt, name='dispatch')
class PhoneVerifyView(View):
    """Verify user phone number via ajax query at the signup page"""

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')
        if phone_number and 9 < len(phone_number) < 13:
            try:
                phone_number = int(phone_number)
            except ValueError:
                return JsonResponse({"error": "Ошибка! Используйте только цифры!"}, status=400)
        else:
            return JsonResponse({"error": "Ошибка! Нет номера или неверный номер!"}, status=400)
        rand_code = random_4digit_num_generator()
        smslog, created = SMSLog.objects.get_or_create(phone_number=phone_number)
        if not created and smslog.verified:
            return JsonResponse({"error": "Ошибка! Этот номер уже используется!"}, status=400)
        smslog.generated_code = rand_code
        smslog.save()
        if send_sms_code(phone_number, rand_code):
            return JsonResponse({"error": "Ошибка отправки сообщения!"}, status=400)
        else:
            return JsonResponse({"success": ""}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class PhoneCodeVerifyView(View):
    """Verify user phone number sent code via ajax query at the signup page"""

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        phone_number = request.POST.get('phone_number')
        if phone_number and 9 < len(phone_number) < 13:
            try:
                phone_number = int(phone_number)
            except ValueError:
                return JsonResponse({"error": "Ошибка в номере телефона! Используйте только цифры!"}, status=400)
        else:
            return JsonResponse({"error": "Ошибка в номере телефона! Нет номера или неверный номер!"}, status=400)
        smslog = SMSLog.objects.get(phone_number=phone_number)
        if code and len(code) == 4 and code == smslog.generated_code:
            smslog.verified = True
            smslog.save()
            return JsonResponse({"success": ""}, status=200)
        else:
            return JsonResponse({"error": "Ошибка! Код не верный!"}, status=400)
