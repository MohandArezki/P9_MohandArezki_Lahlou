from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import SignInView

urlpatterns = [
    path('signin/', SignInView.as_view(), name="signin"),
    path('', SignInView.as_view(), name="signin"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("reviews/", include("reviews.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
