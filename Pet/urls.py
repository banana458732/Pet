from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views  # accountsアプリケーションのviewsをインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # ここを修正してaccountsアプリのindexに飛ぶようにする
    path('pets/', include('petapp.urls')),
    path('survey/', include('Survey.urls')),
    path('accounts/', include('accounts.urls')),
    path('karikeiyaku/', include('karikeiyaku.urls')),
    path('messaging/', include('messaging.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
