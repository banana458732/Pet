from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyPageView, complete_contract, RedirectTemporaryPetView, PetSelectionView

app_name = 'accounts'

urlpatterns = [
#   path('signup/',
#          views.SignUpView.as_view(),
#          name='signup'),
     path('signup/', views.SignUpView.as_view(template_name="accounts/signup.html"), name='signup'),
     path('signup_confirm/', views.SignUp_ConfirmView.as_view(template_name="accounts/signup_confirm.html"), name='signup_confirm'),

     path('signup_success/',
          views.SignUpSuccessView.as_view(),
          name='signup_success'),

     path('login/',
          views.LoginView,
          name='login'
          ),

     path('logout/',
          views.LogoutView.as_view(),
          name='logout'
          ),
          
     path('staff_menu/',
          views.Staff_Menu,
          name='staff_menu'),

    #  path('',
    #       views.IndexView.as_view(template_name='accounts/index.html'),
    #       name='index'),
     path('', views.index, name='index'),
     path('mypage/', MyPageView.as_view(), name='my_page'),  # 'mypage'ではなく'my_page'を使用
     path('contract/complete/', complete_contract, name='complete_contract'),
     path('pet-selection/', PetSelectionView.as_view(), name='pet_selection'),
     path('temporary-pet/', RedirectTemporaryPetView.as_view(), name='temporary_pet'),
     path('change_profile_image/', views.change_profile_image, name='change_profile_image'),  # 追加
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
