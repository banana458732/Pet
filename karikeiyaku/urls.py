from django.urls import path
from . import views

app_name = 'karikeiyaku'

urlpatterns = [
    path('<int:pet_id>/', views.karikeiyaku_form, name='form'),  # 仮契約フォーム
    path('complete/', views.karikeiyaku_comp, name='complete'),  # 仮契約完了ページ
    path('cancel/<int:pet_id>/', views.karikeiyaku_cancel, name='cancel'),  # キャンセルフォーム
    path('cancel/complete/', views.cancel_complete, name='cancel_complete'),  # キャンセル完了ページ
    path('contractor/<int:pet_id>/', views.contractor, name='contractor'),  # ここが正しいURLパターン
    path('com/<int:pet_id>/', views.com, name='com'),  # ここが正しいURLパターン
    path('contractor/completed/<int:pet_id>/', views.completed_contract_detail, name='completed_contract'),
]
