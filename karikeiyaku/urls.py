from django.urls import path
from . import views

app_name = 'karikeiyaku'

urlpatterns = [
    path('<int:pet_id>/', views.karikeiyaku_form, name='form'),  # 仮契約フォーム
    path('complete/', views.karikeiyaku_comp, name='complete'),  # 仮契約完了ページ
    path('cancel/<int:pet_id>/', views.karikeiyaku_cancel, name='cancel'),  # キャンセルフォーム
]