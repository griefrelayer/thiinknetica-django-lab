from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),   # Include urls from main app
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),   # Flatpages
]
