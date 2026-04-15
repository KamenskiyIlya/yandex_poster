from django.contrib import admin
from django.urls import path
from where_to_go import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
