from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ValidationError
from django.db import models
from .models import Car, Thing, Service, Ad, Picture
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from sorl.thumbnail.admin import AdminImageMixin

User = get_user_model()

# Register your models here.


@admin.action(description='Переместить объявления в архив(сделать неактивными)')
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Сделать объявления активными')
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Пометить объявления как проданные')
def make_sold(modeladmin, request, queryset):
    queryset.update(is_sold=True)


@admin.action(description='Пометить объявления как не проданные')
def make_not_sold(modeladmin, request, queryset):
    queryset.update(is_sold=False)


class CustomChangeList(ChangeList):
    def url_for_result(self, result) -> str:
        pk = getattr(result, self.pk_attname)
        cls = self.model.objects.get(id=pk).ad_type
        return f'../{cls.model}/%d/change/' % (quote(pk))


class PictureAdminInline(AdminImageMixin, admin.TabularInline):
    model = Picture


class AdSubModelsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'seller', 'is_sold', 'is_active',)
    ordering = ['datetime_created', 'datetime_modified']
    list_filter = ('is_sold', 'is_active', 'datetime_created', 'datetime_modified')
    inlines = [PictureAdminInline]
    search_fields = ['name', 'seller__first_name', 'seller__last_name', 'seller__username']
    actions = [make_inactive, make_active, make_sold, make_not_sold]


class AdAdmin(AdSubModelsAdmin):
    list_display = ('name', 'seller', 'price', 'ad_type',)

    def get_changelist(self, request, **kwargs):
        return CustomChangeList


admin.site.register(Ad, AdAdmin)


class CarAdmin(AdSubModelsAdmin):
    pass


admin.site.register(Car, CarAdmin)


class ServiceAdmin(AdSubModelsAdmin):
    pass


admin.site.register(Service, ServiceAdmin)


class ThingAdmin(AdSubModelsAdmin):
    pass


admin.site.register(Thing, ThingAdmin)


class CustomUserAdmin(UserAdmin):
    """To admin customized user model"""
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    list_display = ('username', 'email', 'phone_number', 'is_staff')


admin.site.register(User, CustomUserAdmin)


# Define a new FlatPageAdmin
class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }

# Re-register FlatPageAdmin


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
